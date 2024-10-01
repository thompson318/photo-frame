import glob
import random
import json

class photolist():
    def __init__(self):
        self.photos = {}
        self.load_from_file("./photo_list.json")

    def load_from_file(self, filename = "./photo_list.json"):
        """Reads the file list from a file"""
        try: 
            with open(filename, 'r') as filein:
                self.photos = json.load(filein)
        except FileNotFoundError:
            print(f"Failed to find {filename}, rescanning")
            self.scan_for_photos()

    def _save_to_file(self, filename = "./photo_list.json"):
        """Saves the photolist to a file"""
        with open(filename, 'w') as fileout:
            json.dump(self.photos, fileout, indent=2)


    def scan_for_photos(self):
        files = glob.glob('./photos/**/*.jpg') + glob.glob('./photos/**/*.JPG') + \
                glob.glob('./photos/**/*.png') + glob.glob('./photos/**/*.PNG') +  \
                glob.glob('./photos/*.jpg') + glob.glob('./photos/*.JPG') + \
                glob.glob('./photos/*.png') + glob.glob('./photos/*.PNG')

        for file in files:
            if file not in self.photos:
                options = { 'show' : True, 
                            'crop': True,
                            'roi': None, 
                            'frame_colours': None }
                # options we can have 
                # showit: to show or not to show
                # a roi
                # a list of preferred frame colours
                # option to crop: if false we just make the frame bigger to fit
                # 
                self.photos[file] = options

        self.photocount = len(self.photos)
        self._save_to_file()
        print (f"Found {self.photocount} photos")
    
    def random_photo(self):
        # this will return a tuple of file name and options
        return random.choice(list(self.photos.items()))
