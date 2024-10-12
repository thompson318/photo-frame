import sys
from PySide6.QtGui import QPixmap, QImage
from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtCore import QTimer

from src.photoframe.image_process import to_display
class MainWindow(QMainWindow):

    def __init__(self, photolist):
        super(MainWindow, self).__init__()
        self.title = "Photo Frame"
        self.setWindowTitle(self.title)
        self.photolist = photolist
        self.image_to_display = None

        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)

        self.updatetimer = QTimer()
        self.updatetimer.timeout.connect(self.update_image)
        self.updatetimer.start(10*1000)
        
        self.checkupdatetimer = QTimer()
        self.checkupdatetimer.timeout.connect(self.check_for_new_image)
        self.checkupdatetimer.start(1000)

        self.update_image()
        self.current_image = self.photolist.get_current_photo_name()
        self.show_image()

    def show_image(self):
        #pixmap = QPixmap('photos/DSC_0359.JPG')
        height, width, channel = self.image_to_display.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.image_to_display.data, width, height, bytesPerLine, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)

    def update_image(self):
        frame_size = [1920, 1080]
        border_size = [48, 40]
        print ("Time to update the image")
        photo = self.photolist.random_photo()
        self.current_image = photo[0]
        print(f"got {photo[0]}")
        self.image_to_display = to_display(photo, frame_size, border_size)
        self.show_image()

    def check_for_new_image(self):
        if self.current_image == self.photolist.get_current_photo_name():
            print (f"No change {self.current_image} == {self.photolist.get_current_photo_name()} ")
        else:
            frame_size = [1920, 1080]
            border_size = [48, 40]
            print ("Time to update the image")
            photo = self.photolist.get_current_photo()
            self.current_image = self.photolist.get_current_photo_name()
            print (f"got {photo}")
            self.image_to_display = to_display(photo, frame_size, border_size)
            self.show_image()


