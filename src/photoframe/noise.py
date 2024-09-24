# from https://stackoverflow.com/questions/51646185/how-to-generate-a-paper-like-background-with-opencv

import cv2
import numpy as np

MONOCHROME = 3


def add_noise(img, sigma=2):
    """
    Adds noise to the existing image
    """
    width, height, ch = img.shape
    n = noise(width, height, ratio = 4, sigma=sigma)
    img = img - n
    #img = texture(img)
    img = img.clip(0,255)
    cv2.imwrite("noisandmask.png", img)
    return img


def noise(width, height, ratio=1, sigma=100):
    """
    The function generates an image, filled with gaussian nose. If ratio parameter is specified,
    noise will be generated for a lesser image and then it will be upscaled to the original size.
    In that case noise will generate larger square patterns. To avoid multiple lines, the upscale
    uses interpolation.

    :param ratio: the size of generated noise "pixels"
    :param sigma: defines bounds of noise fluctuations
    """
    mean = 0
    assert width % ratio == 0, "Can't scale image with of size {} and ratio {}".format(width, ratio)
    assert height % ratio == 0, "Can't scale image with of size {} and ratio {}".format(height, ratio)

    h = int(height / ratio)
    w = int(width / ratio)

    result = np.random.normal(mean, sigma, (w, h, MONOCHROME))
    if ratio > 1:
        result = cv2.resize(result, dsize=(width, height), interpolation=cv2.INTER_LINEAR)
    result = result.reshape((width, height, MONOCHROME)).astype(np.uint8)
    cv2.imwrite("noisymask.png", result)
    return result


def texture(image, sigma=2, turbulence=2):
    """
    Consequently applies noise patterns to the original image from big to small.

    sigma: defines bounds of noise fluctuations
    turbulence: defines how quickly big patterns will be replaced with the small ones. The lower
    value - the more iterations will be performed during texture generation.
    """
    result = image.astype(float)
    cols, rows, ch = image.shape
    ratio = cols
    while not ratio == 1:
        result += noise(cols, rows, ratio, sigma=sigma)
        ratio = (ratio // turbulence) or 1
    cut = np.clip(result, 0, 255)
    return cut.astype(np.uint8)
