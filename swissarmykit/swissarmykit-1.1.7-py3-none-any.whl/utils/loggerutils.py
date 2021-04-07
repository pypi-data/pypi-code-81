import sys
import os
import time
import tailer
import logging

from datetime import datetime

from swissarmykit.conf import *
from swissarmykit.db.mongodb import BaseDocument
from swissarmykit.lib.core import Singleton

@Singleton
class LoggerUtils:

    def __init__(self, file_name='log_', gui=None, datefmt='%d-%b %H:%M:%S'):
        self.logger = logging.getLogger() # root
        self.db_log = None
        self.db_log_file = None

        if 'swissarmykit_conf' in globals():
            self.db_log = BaseDocument.get_class('logger', db_name='meta')
            self.db_log_file = BaseDocument.get_class('logger_file', db_name='meta')

        self.gui = gui

        self._file_name_db_log = file_name

        if not self.logger.hasHandlers():
            time.strftime("%Y-%m-%d")

            if '/' not in file_name:
                try:
                    from swissarmykit.utils.fileutils import PathUtils
                    file_name = PathUtils.get_log_path() + '/' + file_name
                except Exception as e:
                    file_name = '/tmp/dist/log/' + file_name

            log_file = file_name + '_' + time.strftime("%Y-%m-%d") + '.log'
            self.log_file = log_file
            self.log_name = log_file.rsplit('/', 1)[-1]

            logFormatter = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s", datefmt=datefmt)

            self.logger.setLevel(level=logging.INFO)

            fileHandler = logging.FileHandler(log_file, encoding='UTF-8')
            fileHandler.setFormatter(logFormatter)
            self.logger.addHandler(fileHandler)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            self.logger.addHandler(consoleHandler)

            print('\n\nINFO: Logger file: ', self.log_name)
            if self.db_log_file:
                self.db_log_file.save_url(self.log_name, attr={'name': str(os.getpid())}, update_modified_date=True)

        if not self.gui:
            self.gui = gui

    def _log_db(self, err_type='INFO', message=''):
        if self.db_log:
            url = err_type + '_' + self._file_name_db_log + '_' + str(datetime.now())
            self.db_log.save_url(url, attr={'name': err_type, 'description': message}, update_modified_date=True)


    def log_stdout(self):
        sys.stdout = LogFile(self.log_file)

    def _get_text(self, text, *args):
        if args:
            return str(text) + ' ' + ' '.join([str(arg) for arg in args])
        return str(text)

    def inf(self, text, *args):
        self.info(text, *args)

    def info(self, text, *args):
        text = self._get_text(text, *args)
        self.logger.info(text)
        self._log_db('INFO', text)

        if self.gui:
            self.gui.send_text_info(text)

    def debug(self, text, *args):
        text = self._get_text(text, *args)
        self._log_db('DEBUG', text)

        self.logger.debug(text)
        if self.gui:
            self.gui.send_error_info(text)

    def error(self, text, *args):
        text = self._get_text(text, *args)
        self._log_db('ERROR', text)

        self.logger.error(text)
        if self.gui:
            self.gui.send_error_info(text)

    def warn(self, text, *args):
        text = self._get_text(text, *args)
        self._log_db('WARN', text)

        self.warning(text)

    def warning(self, text, *args):
        text = self._get_text(text, *args)
        self._log_db('WARN', text)

        self.logger.warning(text)
        if self.gui:
            self.gui.send_error_info(text)

    def get_log_file(self):
        return self.log_file

    def get_log_name(self):
        return self.log_name

    def get_tail_log(self, lines=15):
        if os.path.exists(self.get_log_file()):
            return '\n'.join(tailer.tail(open(self.get_log_file(), encoding="utf8"), lines))
        return ''

class LogFile(object):
    # https://stackoverflow.com/questions/14906764/how-to-redirect-stdout-to-both-file-and-console-with-scripting

    # Lumberjack class - duplicates sys.stdout to a log file and it's okay
    # source: https://stackoverflow.com/q/616645
    # https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file/2216517#2216517

    def __init__(self, filename, name='stdout', mode="a"):
        self.logger = logging.getLogger(name)
        self.stdout = sys.stdout
        self.file = open(filename, mode)
        sys.stdout = self

    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

if __name__ == '__main__':
    log = LoggerUtils.instance()
    log.log_stdout()

    print('test')
    log.info('test', 'testd')
    log.error('test', 'testd')
    log.warn('test', 'testd')

