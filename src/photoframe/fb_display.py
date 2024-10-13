import numpy as np

# Map the screen as Numpy array
# N.B. Numpy stores in format HEIGHT then WIDTH, not WIDTH then HEIGHT!
# c is the number of channels, 4 because BGRA
class fb_display():
    def __init__(self):
        h, w, c = 1080, 1920, 3
        self.fb = np.memmap('/dev/fb0', dtype='uint8',mode='w+', shape=(h,w,c))

    def show_photo(self, photo):
        # photo = cv2.imread('102D3500_orig_DSC_0317.JPG')
        # Fill entire screen with blue - takes 29 ms on Raspi 4
        self.fb[:] = photo

