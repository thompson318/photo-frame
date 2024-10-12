import sys
from PySide6.QtGui import QPixmap, QImage
from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        #self.resize(pixmap.width(), pixmap.height())
        #self.resize(960, 540)

    def show_image(self, cvImg):
        #pixmap = QPixmap('photos/DSC_0359.JPG')
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)
