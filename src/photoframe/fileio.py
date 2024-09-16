import glob
import random

class photolist():
    def __init__(self):
        self.find_photos()

    def find_photos(self):
        self.files = glob.glob('./photos/**/*.jpg') + glob.glob('./photos/**/*.JPG') + glob.glob('./photos/**/*.png') + glob.glob('./photos/**/photos/*.PNG')
        self.photocount = len(self.files)
    
    def random_photo(self):
        return random.choice(self.files)
