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
        for _ in range (800):
            self.show_patch(self.destroy)

    def show_favorite(self):
        # an indicator to show that we've favourited the image
        self.show_patch(self.favourite, (200,200))

    def show_crop(self):
        # an indicator to show that we've marked the image for crop
        self.show_patch(self.crop_flag, (200,200))

    def show_patch(self, patch, location = None):
        height, width, channels = patch.shape
        if location == None:
            x_pix = random.randint(width//2, self.width - 1 - width//2)
            y_pix = random.randint(height//2, self.height - 1 - height//2)
            location = (x_pix, y_pix)

        self.fb[location[1] - height//2:location[1] + height//2,
                location[0] - width//2:location[0] + width//2, : ] = patch[:,:,0:3]

    def _set_up_emojis(self):
        try:
            self.favourite = np.load('emojis/favourite.npy')
        except FileNotFoundError:
            self.favourite = np.full(
                    shape=(200,200,4), fill_value=[255,0,0,255], dtype = np.uint8)

        try:
            self.crop_flag = np.load('emojis/crop_flag.npy')
        except FileNotFoundError:
            self.crop_flag = np.full(
                    shape=(200,200,4), fill_value=[0,255,0,255], dtype = np.uint8)

        try:
            self.destroy = np.load('emojis/destroy.npy')
        except FileNotFoundError:
            self.destroy = np.full(
                    shape=(200,200,4), fill_value=[0,0,0,255], dtype = np.uint8)



