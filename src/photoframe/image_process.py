import cv2

def to_display(filename):
    """ 
    Loads an image from disc, resizes it, adds a frame
    """

    image = cv2.imread(filename)
    print (f"Read {filename}", end = " ")
    
    image = _resize_and_crop(image)


def _resize_and_crop(image, frame_size = [1920, 1080], 
        border_size = [100, 100]):
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

    #if it's landscape scale to fit width then crop top and bottom if required
    #if it's portrait scale to fit height, no need to crop.

    return image
