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
    print (f"new image size {new_image.shape}")
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
    print (f"Read {filename}", end = " ")
    
    region_of_interest = options.get("roi", None)
    if region_of_interest is not None:
        image = _crop(image, region_of_interest)

    image = _resize_and_crop(image, frame_size, border_size)

    height, width, channels = image.shape
    full_border = [ ( frame_size[0] - width ) // 2, ( frame_size[1] - height ) // 2 ]
    print(f"We need a border this big {full_border}")

    bevel_size = [4, 4]
    frame = make_frame(frame_size, bevel_size, [image.shape[1], image.shape[0]])
    print(f"Image size = {frame.shape} type {frame.dtype}")
    frame = add_noise(frame, sigma = 5)
    print(f"Image size = {frame.shape} type {frame.dtype}")
    frame[full_border[1]:frame_size[1]-full_border[1], full_border[0]:frame_size[0]-full_border[0]] = image
    return frame

def _resize_and_crop(image, frame_size, 
        border_size):
    height, width, channels = image.shape

    print (f"{height} {width} {channels}")

    target_size = [frame_size[0] - 2 * border_size[0], 
            frame_size[1] - 2 * border_size[1]]

    print (f"Scale and crop to {target_size}")

    portrait = False
    if height > width:
        portrait = True

    if portrait:
        scale_factor = target_size[1]/height
        scaled_image = cv2.resize(image, dsize=(0,0), fx = scale_factor, fy = scale_factor, 
                interpolation = cv2.INTER_LANCZOS4)
    else:
        scale_factor = target_size[0]/width
        scaled_image = cv2.resize(image, dsize=(0,0), fx = scale_factor, fy = scale_factor, 
                interpolation = cv2.INTER_LANCZOS4)

    print(f"Scaled to {scaled_image.shape}")

    height, width, channels = scaled_image.shape
    #if it's landscape scale to fit width then crop top and bottom if required
    #if it's portrait scale to fit height, no need to crop.
    oversize = height - target_size[1] 
    if oversize%2 != 0:
        oversize = oversize+1
    cropped_image = scaled_image[oversize//2:height-oversize//2,:,:]

    height, width, channels = cropped_image.shape
    assert height == target_size[1]
    assert width <= target_size[0]
    return cropped_image

def make_frame(frame_size, bevel_size, image_size):
    # plan. Make a blank image x by y. Draw four triangles from just beyond the image corners to the middle. Top triangle is slightly darker than the others.
    # fill outside with rectangals. 
    # optional: blurred lines through corners?
    
    blank_image = np.zeros((frame_size[1],frame_size[0],3), np.uint8)
    image_top = (frame_size[1] - image_size[1]) // 2
    image_bottom = frame_size[1] - (frame_size[1] - image_size[1]) // 2
    image_left = (frame_size[0] - image_size[0]) // 2
    image_right = frame_size[0] - (frame_size[0] - image_size[0]) // 2
    
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
