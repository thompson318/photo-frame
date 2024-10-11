import cv2

class display():
    def __init__(self, scale = 1.0):
        self.scale = scale
        return

    def show(self, image):
        window = cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)

        cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('image',cv2.resize(image, dsize=(0,0), fx = self.scale, fy = self.scale, interpolation = cv2.INTER_LANCZOS4))
        cv2.waitKey(600*1000)
        return
