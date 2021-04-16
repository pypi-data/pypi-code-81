import os
import sys
from xyw_utils.errors import NoFileError


def get_filepath():
    """
    获取当前运行文件的绝对地址
    :return:
    """
    # 此处排除了命令行和pycharm中console这两种情况
    if sys.argv[0] == '' \
            or os.path.split(sys.argv[0])[-1] == 'pydevconsole.py':
        raise NoFileError('must be used in file')
    return os.path.abspath(sys.argv[0])


def get_filedir():
    """
    获取当前运行文件所在文件夹的绝对地址
    :return:
    """
    return os.path.dirname(get_filepath())


def change_to_maindir():
    """
    切换工作目录为当前运行文件所在文件夹，通常用在main函数开头
    :return:
    """
    os.chdir(get_filedir())


class FileName:
    """
    文件名类，将完整地文件路径拆分为路径、文件名、文件后缀三部分存储
    """
    def __init__(self, fullpath):
        self.path, filename = os.path.split(fullpath)
        self.name, ext = os.path.splitext(filename)
        self.__ext = ext.lower()

    @property
    def ext(self):
        return self.__ext

    @ext.setter
    def ext(self, ext):
        if not(ext == '' or (len(ext) > 1 and ext[0] == '.')):
            raise ValueError('param ext must be \'\' or \'.*\'')
        self.__ext = ext.lower()

    def is_ext(self, ext):
        """
        判断后缀是否相同
        :param ext:
        :return:
        """
        if isinstance(ext, str):
            return self.ext == ext
        elif isinstance(ext, list):
            return self.ext in ext
        else:
            raise TypeError('param ext must be string or list')

    def is_image(self):
        """
        判断是否为图片文件
        :return:
        """
        return self.is_ext(['.jpg', '.jpeg', '.png', '.gif'])

    def is_file_exist(self):
        """
        判断文件是否存在
        :return:
        """
        if os.path.isdir(self.fullpath):
            raise RuntimeError('the path is a dir')
        return os.path.exists(self.fullpath)

    def is_dir_exist(self):
        """
        判断文件所在文件夹是否存在
        :return:
        """
        if os.path.isfile(self.path):
            raise RuntimeError('the path is a file')
        return os.path.exists(self.path) if self.path != '' else True

    def make_dir(self):
        """
        创建文件所在文件夹
        :return:
        """
        if not self.is_dir_exist():
            os.makedirs(self.path)

    def set_fullpath(self, fullpath):
        """
        设置完整路径名
        :param fullpath:
        :return:
        """
        self.path, filename = os.path.split(fullpath)
        self.name, self.ext = os.path.splitext(filename)

    def get_filename(self):
        """
        获取文件名
        :return:
        """
        return ''.join([self.name, self.ext])

    def set_filename(self, filename):
        """
        设置文件名
        :param filename:
        :return:
        """
        self.name, self.ext = os.path.splitext(filename)

    def get_fullpath(self):
        """
        设置完整路径名
        :return:
        """
        return os.path.join(self.path, self.get_filename())

    def __eq__(self, other):
        return self.path == other.path and self.name == other.name and self.ext == other.ext

    def __repr__(self):
        return 'FileName(r\'%s\')' % self.fullpath

    filename = property(get_filename, set_filename)
    fullpath = property(get_fullpath, set_fullpath)


if __name__ == '__main__':
    f = FileName(r'C:\Users\Administrator\Desktop\xyw\xyw_test\d.py\xue.JPG')
    print(f.ext)
    print(f.filename)
    print(f.is_file_exist())
    f.filename = 'xue.jpg'
    print(f.fullpath)
    print(f.is_file_exist())
    # f.make_dir()
    print(f)
    # print(eval(r"FileName(r'C:\Users\Administrator\Desktop\xyw\xyw_test\d.py\xue.jpg')"))
    print(f == eval(repr(f)))
    f.ext = '.PnG'
    print(f)
