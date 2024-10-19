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
        """
        returns the main page, template/index.html
        """
        return render_template('index.html')

    
    @app.route('/scan', methods=['POST'])
    def scan():

        return app.config['PHOTOS'].scan_for_photos()

    @app.route('/next', methods=['POST']))
    def next():
        open('/dev/shm/photo_update.flag', 'w').close()
        return "Next image"
   
    @app.route('/noshow', methods=['POST'])
    def remove():
        open('/dev/shm/remove_photo.flag', 'w').close()
        return "Image removed"
   
    return app


def record_loop(photolist, display):   
   frame_size = [1920, 1080]
   border_size = [74, 60]
   display_time = 360 #in seconds
   while True:
      photo = photolist.random_photo()
      image_to_display = to_display(photo, frame_size, border_size)
      if image_to_display is not None:
          display.show_photo(image_to_display)
          with open('/dev/shm/current_photo.txt', 'w') as fileout:
              fileout.write(photo[0])
          for i in range (display_time):
              if os.path.isfile('/dev/shm/photo_update.flag'):
                  os.remove('/dev/shm/photo_update.flag')
                  break
              if os.path.isfile('/dev/shm/remove_photo.flag'):
                  os.remove('/dev/shm/remove_photo.flag')
                  if i > 5 and i < display_time - 5:
                      # we add a 5 second safety buffer to try and minimise the 
                      # risk that the signal comes in late and we remove the 
                      # wrong photo
                      display.destroy_image()
                      #then need to actually remove it 
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
