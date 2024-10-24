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
        self._set_up_emojis()

    def show_photo(self, photo):
        # photo = cv2.imread('102D3500_orig_DSC_0317.JPG')
        # Fill entire screen with blue - takes 29 ms on Raspi 4
        self.fb[:] = photo

    def destroy_image(self):
        # destroy the image, preferably in an entertaining way
        patch_size = 100
        for _ in range (800):
           
            x_pix = random.randint(patch_size, self.width - 1 - patch_size)
            y_pix = random.randint(patch_size, self.height - 1 - patch_size)
            self.fb[y_pix - patch_size:y_pix + patch_size,
                    x_pix - patch_size:x_pix + patch_size, : ] = [0,0,0]

    def show_favorite(self):
        # an indicator to show that we've favourited the image
        self.fb[200:400, 300:500, :] = [255,0,0]

    def show_crop(self):
        # an indicator to show that we've marked the image for crop
        self.fb[200:400, 300:500, :] = [0,255,0]

    def show_patch(self, patch):
        return

    def _set_up_emojis(self):
        try:
            self.favourite = np.load('emojis/favourite.npy')
        except FileNotFoundError:
            self.favourite = np.full(
                    shape=(200,200,4), fill_value=[255,0,0,255], dtype = np.uint8)

        try:
            self.crop_flag = np.load('crop_flag.npy')
        except FileNotFoundError:
            self.crop_flag = np.full(
                    shape=(200,200,4), fill_value=[0,255,0,255], dtype = np.uint8)

        try:
            self.destroy = np.load('destroy.npy')
        except FileNotFoundError:
            self.destroy = np.full(
                    shape=(200,200,4), fill_value=[0,0,0,255], dtype = np.uint8)



