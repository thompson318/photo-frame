import glob

def find_photos():
    files = glob.glob('./photos/**/*.jpg') + glob.glob('./photos/**/*.JPG') + glob.glob('./photos/**/*.png') + glob.glob('./photos/**/photos/*.PNG')
    return files
