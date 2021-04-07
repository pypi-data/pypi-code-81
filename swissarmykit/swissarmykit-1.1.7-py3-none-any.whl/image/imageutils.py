

import os
import cv2 # opencv-python

from PIL import Image

from swissarmykit.utils.fileutils import FileUtils
from swissarmykit.utils.timer import Timer

class ImageUtils:

    @staticmethod
    def create_thumbnail(dst, new_path=None, max_size=(400, 225)): # full HD

        dst = dst.replace('\\', '/').rstrip('/')
        new_path = new_path.replace('\\', '/').rstrip('/') if new_path else None

        if new_path == dst:
            raise Exception(f'new_path: {new_path} == des: {dst}')

        output = new_path if new_path else os.path.join(dst, 'thumbnails')
        FileUtils.mkdir(output)

        files = FileUtils.get_all_files(dst)
        timer = Timer.instance(len(files))
        for idx, infile in enumerate(files):
            im = Image.open(infile)
            im.thumbnail(max_size, Image.ANTIALIAS)
            file = os.path.join(output, infile.rsplit(os.sep, 1)[-1])
            im.save(file)

            timer.check(idx=idx)

    @staticmethod
    def convert_to_square(path, dest, width, height):
        img_list = os.listdir(path)
        for file_name in img_list:
            try:
                img = path + '/' + file_name
                im = Image.open(img)
                im_resize = im.resize((width, height))
                im_resize.save(dest + '/' + file_name)
            except Exception as e:
                # https://github.com/python-pillow/Pillow/issues/1380
                img = path + '/' + file_name
                im = Image.open(img)
                im_resize = im.resize((width, height))
                im_resize.convert('RGB').save(dest + '/' + file_name, "PNG", optimize=True)

                print('Fail file %s ' % file_name)

    @staticmethod
    def crop_im(path, dest, x=0, y=0, h=10, w=10):
        img_list = FileUtils.get_all_files(path, file_name_only=True)
        for file_name in img_list:
            # Crop image
            input = path + '/' + file_name
            output = dest + '/' + file_name
            img = cv2.imread(input)
            crop_img = img[y:y + h, x:x + w]
            cv2.imshow("cropped", crop_img)
            cv2.waitKey(0)


if __name__ == '__main__':
    i = ImageUtils

    # ImageUtils.convert_to_square(path_id, dest_id, 70, 50)
