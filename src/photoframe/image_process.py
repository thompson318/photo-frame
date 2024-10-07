import cv2
import numpy as np

from src.photoframe.noise import add_noise

def _crop(image, roi):
    """
    Internal function to crop an image and return a cropped
    copy of the image. 
    :param image: the image to crop
    :param region_of_interest: a list containing [x0, y0, x1, y2]
    :returns: a cropped image
    """
    new_image = image[roi[1]:roi[3],roi[0]:roi[2],:]
    return new_image

def to_display(photo, frame_size, border_size):
    """ 
    Loads an image from disc, resizes it, adds a frame
    photo is a tuple photo[0] is a filename photo [1] is a dictionary of 
    options
    """
    options = photo[1]
    if not options.get("show", True):
        return None

    filename = photo[0]
    image = cv2.imread(filename)
    print (f"Read {filename}", end = "\n")
    
    region_of_interest = options.get("roi", None)
    if region_of_interest is not None:
        image = _crop(image, region_of_interest)
    
    crop_to_frame = options.get("crop", False)
    print (f"Cropping to frame = {crop_to_frame}")
    image = _resize_and_crop(image, frame_size, border_size, crop_to_frame)

    height, width, channels = image.shape
    full_border = [ ( frame_size[0] - width ) // 2, ( frame_size[1] - height ) // 2 ]
    print(f"We need a border this big {full_border}")

    bevel_size = [4, 4]
    image_size = [image.shape[1], image.shape[0]]
    image_top = frame_size[1] // 2 - image_size[1] // 2
    image_bottom = image_top + image_size[1]
    #image_bottom = frame_size[1] // 2 + image_size[1] // 2
    image_left = frame_size[0] //2 - image_size[0] // 2
    #image_right = frame_size[0] // 2 + image_size[0] // 2
    image_right = image_left + image_size[0]
    print (f"{image_top}, {image_bottom}, {image_left}, {image_right}")
    frame = make_frame(frame_size, bevel_size, image_top, image_bottom, image_left, image_right)
    print(f"Image size = {frame.shape} type {frame.dtype}")
    frame = add_noise(frame, sigma = 5)
    print(f"Image size = {image.shape} type {frame.dtype}")
    full_border = [ image_left, image_top ]
    #frame[full_border[1]:frame_size[1]-full_border[1], full_border[0]:frame_size[0]-full_border[0]] = image
    frame[image_top:image_bottom, image_left:image_right] = image
    return frame

def _crop_to_aspect_ratio(image, target_aspect_ratio):
    """
    uses image crop to get the right aspect ratio
    """
    height, width, channels = image.shape
    image_aspect_ratio = width/height
    
    aspect_ration_delta = abs(image_aspect_ratio - target_aspect_ratio)
    if aspect_ration_delta > 0.6: # if the aspect ratio difference is really big don't crop
        print(f"Difference in aspect ratio {aspect_ration_delta} too big, not cropping")
        return image

    if image_aspect_ratio > target_aspect_ratio:
        finished_image_width = target_aspect_ratio * height
        amount_to_crop = int((width - finished_image_width) // 2)
        print(f"We need to make it taller.  cropping {amount_to_crop} from {width}")
        image = image[:,amount_to_crop:width-amount_to_crop//2,:]
    elif image_aspect_ratio < target_aspect_ratio:
        finished_image_height = width / target_aspect_ratio
        amount_to_crop = int((height - finished_image_height) // 2) 
        print(f"We need to make it wider.  cropping {amount_to_crop} from {height}")
        image = image[amount_to_crop:height-amount_to_crop//2,:,:]
    else:
        print("Aspect ratio good")
    return image


def _resize(image, target_width, target_height):
    """ 
    resizes to fit the frame. If the image aspect ratio (width/height) is 
    greater than the target, we resize to width. Else to height
    """
    height, width, channels = image.shape
    scale_factor = 1.0
    if width / height > target_width / target_height:
        scale_factor = target_width / width
    else: 
        scale_factor = target_height / height
        
    scaled_image = cv2.resize(image, dsize=(0,0), fx = scale_factor, fy = scale_factor, 
        interpolation = cv2.INTER_AREA)
    return scaled_image
    

def _resize_and_crop(image, frame_size, 
        border_size, crop_to_frame):
    """
    We're aimin to create an image that fit's nicely within the frame
    Maybe don't think landscape or portrait but rather aspect ratio
    If it's landscape AND crop_to_frame -> we scale to the frame width, then 
        if required crop to height
    If it's lansscape AND NOT crop_to_frame -> we do the smallest scale -> height or width
    etc.
    Possibilities:
    """
    target_width = frame_size[0] - 2 * border_size[0]
    target_height = frame_size[1] - 2 * border_size[1] 
    target_aspect_ratio = target_width / target_height
    print (f"target width = {target_width}, target_height = {target_height} , target_aspect_ratio = {target_aspect_ratio}")
    
    if crop_to_frame:
        image = _crop_to_aspect_ratio(image, target_aspect_ratio)
    
    scaled_image = _resize(image, target_width, target_height)

    print(f"Scaled to {scaled_image.shape}")

    height, width, channels = scaled_image.shape
    assert height <= target_height
    assert width <= target_width
    return scaled_image

def make_frame(frame_size, bevel_size, image_top, image_bottom, image_left, image_right):
    # plan. Make a blank image x by y. Draw four triangles from just beyond the image corners to the middle. Top triangle is slightly darker than the others.
    # fill outside with rectangals. 
    # optional: blurred lines through corners?
    
    blank_image = np.zeros((frame_size[1],frame_size[0],3), np.uint8)
    
    bevel_top = image_top - bevel_size[1]
    bevel_bottom = image_bottom + bevel_size[1]
    bevel_right = image_right + bevel_size[0]
    bevel_left = image_left - bevel_size[0]
    

    image_centre = ( frame_size[0]//2, frame_size[1]//2)
    top_bevel = np.array([(bevel_top, bevel_left), image_centre, (bevel_top, bevel_right)])
    cv2.putText(blank_image,'ct', org = image_centre, fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 5, color=(0,0,255), thickness = 5)
    cv2.putText(blank_image,'bl', org = (bevel_left, bevel_top), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 5, color=(0,0,255), thickness = 5)
    cv2.putText(blank_image,'br', org = (bevel_right, bevel_top), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 5, color=(0,0,255), thickness = 5)
    print(f"Top bevel = {top_bevel}")
    print(f"centre = {image_centre}")

    base_colour = (160, 120, 120)
    # these bevels aren't quite right. We need to draw trapeziums to get 45 degree corners, not triangles.
    top_bev_corners = np.array([
        (bevel_left, bevel_top),(bevel_right, bevel_top),
        (image_right, image_top),(image_left, image_top)
        ])
    cv2.drawContours(blank_image,[top_bev_corners],0,(170, 170, 170),-1)
   
    bot_bev_corners = np.array([
        (bevel_left, bevel_bottom), (bevel_right, bevel_bottom),
        (image_right, image_bottom),(image_left, image_bottom)
        ])
    cv2.drawContours(blank_image,[bot_bev_corners],0, (240,240,240),-1)

    left_bev_corners = np.array([
        (bevel_left, bevel_top), (bevel_left, bevel_bottom),
        (image_left, image_bottom), (image_left, image_top)
        ])
    cv2.drawContours(blank_image,[left_bev_corners],0,(200, 200, 200),-1)
    
    right_bev_corners = np.array([
        (bevel_right, bevel_top), (bevel_right, bevel_bottom),
        (image_right, image_bottom), (image_right, image_top)
        ])
    cv2.drawContours(blank_image,[right_bev_corners],0,(200,200,200),-1)

    blank_image[0:bevel_top,:] = base_colour 
    blank_image[bevel_bottom:frame_size[1],:] = base_colour 
    blank_image[:,0:bevel_left] = base_colour 
    blank_image[:,bevel_right: frame_size[0]] = base_colour 
    return blank_image
