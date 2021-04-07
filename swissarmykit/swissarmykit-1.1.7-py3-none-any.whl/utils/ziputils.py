
import os
import shutil

class ZipUtils:

    @staticmethod
    def zip(path, zip_name='archive'):
        base_name = zip_name.rstrip('.zip')
        shutil.make_archive(base_name, 'zip', path)

if __name__ == '__main__':
    z = ZipUtils()
    z.zip('C:/Users/Will/Desktop/code/ai_/sharelib/swissarmykit/text', 'test.zip')