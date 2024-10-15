import numpy as np
import random

# Map the screen as Numpy array
# N.B. Numpy stores in format HEIGHT then WIDTH, not WIDTH then HEIGHT!
# c is the number of channels, 4 because BGRA
class fb_display():
    def __init__(self):
        self.height = 1080
        self.width = 1920
        self.channels = 3
        self.fb = np.memmap('/dev/fb0', dtype='uint8',mode='w+', 
                shape=(self.height, self.width, self.channels))

    def show_photo(self, photo):
        # photo = cv2.imread('102D3500_orig_DSC_0317.JPG')
        # Fill entire screen with blue - takes 29 ms on Raspi 4
        self.fb[:] = photo

    def destroy_image(self):
        # destroy the image, preferably in an entertaining way
        for _ in range self.height * self.channels * 2:
            x_pix = random.randint(0, width - 1)
            y_pix = random.randint(0, height - 1)
            self.fb[y_pix, x_pix, : ] = [0,0,0]
