import cv2

class display():
    def __init__(self):
        return

    def show(self, image):
        cv2.imshow('window',image)
        cv2.waitKey(10*1000)
        return
