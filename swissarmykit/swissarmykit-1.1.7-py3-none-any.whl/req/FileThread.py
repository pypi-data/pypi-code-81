import shutil
from pathlib import Path

from swissarmykit.conf import *
from swissarmykit.utils.fileutils import FileUtils

class FileTask:

    SAVE = 'save'
    LOAD = 'load'

    def __init__(self, id, table, html='', type=SAVE, html_path=None, encoding='utf-8'):
        self.id = str(id)
        self.table = table
        self.html = html
        self.type = type
        self.encoding = encoding
        self.html_path = html_path if html_path else FileUtils.conf.get_html_path()

    def get_file_path(self, level):
        return '%s/%s/%s_%d.html' % (self.html_path, self.table, self.id, level)

    def get_path(self):
        return '%s/%s' % (self.html_path, self.table)

    def run(self):
        if self.type == FileTask.SAVE:
            return self.save()
        elif self.type == FileTask.LOAD:
            return self.load()

    def save(self, level=1):
        file_path = self.get_file_path(level)
        FileUtils.conf.create_path_if_not_exist(file_path)
        Path(file_path).write_text(self.html, encoding='utf-8')
        return os.path.exists(file_path)

    def load(self, level=1):
        if self.encoding:
            return Path(self.get_file_path(level)).read_text(encoding=self.encoding)
        else:
            return Path(self.get_file_path(level)).read_text()

    def exists(self, level=1):
        return os.path.exists(self.get_file_path(level))

    def size(self, level=1):
        return os.path.getsize(self.get_file_path(level))

    def delete(self, level=1):
        file_path = self.get_file_path(level)
        if os.path.exists(file_path):
            os.remove(file_path)

    def delete_all(self):
        path = self.get_path()
        if os.path.exists(path):
            shutil.rmtree(self.get_path())

    def get_info(self):
        '''
        :return: size, files
        '''
        return FileUtils.get_size_info(self.get_path())

if __name__ == '__main__':

    _stack = []
    print(_stack.pop())