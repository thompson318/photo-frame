import cv2
import numpy as np

def to_display(filename, frame_size, border_size):
    """ 
    Loads an image from disc, resizes it, adds a frame
    """

    image = cv2.imread(filename)
    print (f"Read {filename}", end = " ")
    
    image = _resize_and_crop(image, frame_size, border_size)

    cv2.imwrite(f"{filename}.cropped.jpg", image)


    bevel_size = [10, 10]
    frame = make_frame(frame_size, border_size,bevel_size, [image.shape[1], image.shape[0]])
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

def make_frame(frame_size, border_size, bevel_size, image_size):
    # plan. Make a blank image x by y. Draw four triangles from just beyond the image corners to the middle. Top triangle is slightly darker than the others.
    # fill outside with rectangals. 
    # optional: blurred lines through corners?
    
    blank_image = np.zeros((frame_size[0],frame_size[1],3), np.uint8)
    image_top = (frame_size[0] - image_size[0]) // 2
    image_bottom = frame_size[0] - (frame_size[0] - image_size[0]) // 2
    image_right = (frame_size[1] - image_size[1]) // 2
    image_left = frame_size[1] - (frame_size[1] - image_size[1]) // 2
    
    bevel_top = image_top - bevel_size[0]
    bevel_bottom = image_bottom + bevel_size[0]
    bevel_right = image_right + bevel_size[1]
    bevel_left = image_left - bevel_size[1]

    image_centre = ( frame_size[0]//2, frame_size[1]//2)
    top_bevel = np.array([(bevel_top, bevel_left), image_centre, (bevel_top, bevel_right)])
    print(f"Top bevel = {top_bevel}")

    #cv2.drawContours(blank_image, top_bevel, -1, (0,255,0), 3)
    cv2.drawContours(blank_image,[(0,0),(1000,1000),(1000,0)],0,(0,255,0),3)
    return blank_image
