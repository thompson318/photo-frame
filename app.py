import sys
import time
from flask import Flask, jsonify
from multiprocessing import Process, Value
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel

from src.photoframe.fileio import photolist 
from src.photoframe.qdisplay import MainWindow


def create_app(photo_instance):
    app = Flask(__name__)
    app.config['PHOTOS'] = photo_instance
 
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

        app.config['PHOTOS'].random_photo()
        return "Skipping image"
   
    return app


def record_loop(photolist, something):
  
   qapp = QApplication()
   window = MainWindow(photolist)
   window.show()
   sys.exit(qapp.exec())

if __name__ == "__main__":
   photos = photolist()
   p = Process(target=record_loop, args=(photos, None))
   p.start()  
   app = create_app(photos)
   app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
   p.join()
