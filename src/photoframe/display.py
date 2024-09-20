import cv2

class display():
    def __init__(self, scale = 1.0):
        self.scale = scale
        return

    def show(self, image):
        cv2.imshow('window',cv2.resize(image, dsize=(0,0), fx = self.scale, fy = self.scale, interpolation = cv2.INTER_LANCZOS4))
        cv2.waitKey(10*1000)
        return
