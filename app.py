import time
from flask import Flask, jsonify
from multiprocessing import Process, Value
from pyautogui import press

from src.photoframe.fileio import photolist 
from src.photoframe.image_process import to_display 
from src.photoframe.display import display 


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


def record_loop(photolist, display):
   
   frame_size = [1920, 1080]
   border_size = [48, 40]
   while True:
      photo = photolist.random_photo()
#      photo = ('./photos/DSC_0359.JPG', {"show":True, "roi":[2100,1600,3900,2560]})
      print(f"got {photo[0]}")
      image_to_display = to_display(photo, frame_size, border_size)
      if image_to_display is not None:
        display.show(image_to_display)
        time.sleep(1)


if __name__ == "__main__":
   photos = photolist()
   display = display(1.0)
   p = Process(target=record_loop, args=(photos,display))
   p.start()  
   app = create_app(photos, display)
   app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
   p.join()
