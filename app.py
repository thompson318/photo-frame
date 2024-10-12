import sys
import time
from flask import Flask, jsonify
from multiprocessing import Process, Value
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtCore import QTimer

from src.photoframe.fileio import photolist 
from src.photoframe.image_process import to_display 
from src.photoframe.display import display 
from src.photoframe.qdisplay import MainWindow


def create_app(photo_instance, display_instance):
    app = Flask(__name__)
    app.config['PHOTOS'] = photo_instance
    app.config['DISPLAY'] = display_instance
 
    @app.route('/photos', methods=['GET'])
    def list_photos():
        return app.config['PHOTOS'].photos

    @app.route('/', methods=['GET'])
    def index():
        return "photo-server"
    
    @app.route('/scan', methods=['GET'])
    def scan():

        return app.config['PHOTOS'].scan_for_photos()

    @app.route('/next')
    def next():
        press('n') # we can press any key and the cv2.waitkey function should respond
        return "Next image"
   
    return app


def update_image():
    print ("Time to update the image")


def record_loop(photolist, window):
  
   qapp = QApplication()
   window = MainWindow()
   window.show()

   frame_size = [1920, 1080]
   border_size = [48, 40]
  # while True:
   photo = photolist.random_photo()
#      photo = ('./photos/DSC_0359.JPG', {"show":True, "roi":[2100,1600,3900,2560]})
   print(f"got {photo[0]}")
   image_to_display = to_display(photo, frame_size, border_size)
   if image_to_display is not None:
       window.show_image(image_to_display)

      #  time.sleep(1)
   updatetimer = QTimer()
   updatetimer.timeout.connect(update_image)
   updatetimer.start(1000)
   sys.exit(qapp.exec())

if __name__ == "__main__":
   photos = photolist()
   display=display(1.0)
   p = Process(target=record_loop, args=(photos,display))
   print(f"Starting {p.start()}")  
   app = create_app(photos, display)
   app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
   p.join()
