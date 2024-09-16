import time
from flask import Flask, jsonify
from multiprocessing import Process, Value

from src.photoframe.fileio import photolist 
from src.photoframe.image_process import to_display 

app = Flask(__name__)


tasks = [
   {
      'id': 1,
      'title': u'Buy groceries',
      'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
      'done': False
   },
   {
      'id': 2,
      'title': u'Learn Python',
      'description': u'Need to find a good Python tutorial on the web', 
      'done': False
   }
]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
   return jsonify({'tasks': tasks})


def record_loop(photolist):
   while True:
      photo = photolist.random_photo()
      print(f"got {photo}")
      image_to_display = to_display(photo)
      time.sleep(1)


if __name__ == "__main__":
   photos = photolist()
   p = Process(target=record_loop, args=(photos,))
   p.start()  
   app.run(debug=True, use_reloader=False)
   p.join()
