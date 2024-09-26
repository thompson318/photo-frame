import glob
import random

class photolist():
    def __init__(self):
        self.photos = {}
        self.find_photos()

    def load_from_file(self, filename = "./photo_list.json"):
        """Reads the file list from a file"""
        with open(filename, 'w') as filein:
            self.photos = json.load(filein)

    def save_to_file(self, filename = "./photo_list.json"):
        """Saves the photolist to a file"""
        with open(filename, 'w') as fileout:
            json.dump(self.photos, fileout)


    def find_photos(self):
        files = glob.glob('./photos/**/*.jpg') + glob.glob('./photos/**/*.JPG') + \
                glob.glob('./photos/**/*.png') + glob.glob('./photos/**/*.PNG') +  \
                glob.glob('./photos/*.jpg') + glob.glob('./photos/*.JPG') + \
                glob.glob('./photos/*.png') + glob.glob('./photos/*.PNG')

        for file in files:
            if file not in self.photos:
                options = { 'show' : True, 'crop': True }
                self.photos[file] = options

        self.photocount = len(self.files)
        print (f"Found {self.photocount} photos")
    
    def random_photo(self):
        return random.choice(self.files)
