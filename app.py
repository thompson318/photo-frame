import time
import os
from flask import Flask, jsonify
from multiprocessing import Process, Value
import logging

from src.photoframe.fileio import photolist 
from src.photoframe.image_process import to_display 
from src.photoframe.fb_display import fb_display 


def create_app(photo_instance, display_instance):
    app = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
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
        open('/dev/shm/photo_update.flag', 'w').close()
        return "Next image"
   
    return app


def record_loop(photolist, display):   
   frame_size = [1920, 1080]
   border_size = [74, 60]
   while True:
      photo = photolist.random_photo()
      image_to_display = to_display(photo, frame_size, border_size)
      if image_to_display is not None:
          display.show_photo(image_to_display)
      for _ in range (360):
          if os.path.isfile('/dev/shm/photo_update.flag'):
              os.remove('/dev/shm/photo_update.flag')
              break
          time.sleep(1)


if __name__ == "__main__":
   photos = photolist()
   display = fb_display()
   p = Process(target=record_loop, args=(photos,display))
   p.start()  
   app = create_app(photos, display)
   app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
   p.join()
