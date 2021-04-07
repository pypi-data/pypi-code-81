import imghdr
import os
from PIL import Image
from swissarmykit.utils.fileutils import FileUtils

class ImageUtils:

    # imghdr_what = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr',]
    imghdr_what = {
        # to_type: format
        'png': 'png',
        'webp': 'webp',
        'jpg': 'jpeg'
    }
    allow_convert = ['jpeg', 'png', 'webp']

    def __init__(self):
        pass

    @staticmethod
    def convert(file, to_type='jpg'):
        ''' https://medium.com/@ajeetham/image-type-conversion-jpg-png-jpg-webp-png-webp-with-python-7d5df09394c9 '''
        if not os.path.exists(file):
            print('ERROR: File not exists', file)
            return False

        new_file, ext = file.rsplit('.', 1)
        file_type = ImageUtils.get_image_type(file)

        if file_type in ImageUtils.allow_convert and to_type in ImageUtils.imghdr_what:
            format = ImageUtils.imghdr_what.get(to_type)

            if file_type == format:
                ImageUtils.rename_to_correct_format(file)
            else:
                im = Image.open(file).convert('RGB')
                im.save(new_file + '.' + to_type, format)
        else:
            print('ERROR: Not support convert from ', file_type, 'to type', to_type)

    @staticmethod
    def rename_to_correct_format(file):
        t = ImageUtils.get_image_type(file)
        ext = file.rsplit('.', 1)[-1]

        if t in ImageUtils.allow_convert:
            if t == 'jpeg':
                t = 'jpg'

            if t == ext:
                return True

            FileUtils.rename_extension(file, t) # png, webp, jpg
        else:
            print('ERROR: Not support convert to this ext', t)

    @staticmethod
    def get_image_type(file):
        return imghdr.what(file)

if __name__ == '__main__':
    print('test convert')
