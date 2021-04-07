# -*- coding: utf-8 -*-
import glob
import imghdr
import re
import os
import traceback
import pickle
import csv
import shutil
import string
import tailer
import platform
import sys
from pprint import pprint
from pathlib import Path
from shutil import copyfile
from skimage import io
from PIL import Image

from swissarmykit.conf import *
from swissarmykit.utils.timer import Timer

class FileUtils:

    conf: AppConfig = swissarmykit_conf

    @staticmethod
    def get_all_files_recursive(path, endswith='.txt', file_name_only=False):
        files = []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if endswith:
                    if isinstance(endswith, str) and file.endswith(endswith):
                        files.append(os.path.join(r, file))
                    else:
                        for e in endswith:
                            if file.endswith(e):
                                files.append(os.path.join(r, file))
                else:
                    files.append(os.path.join(r, file))

        if file_name_only:
            return [f.replace(path,'') for f in files]
        return files

    @staticmethod
    def get_all_files(path, file_name_only=False, recursive=False, endswith=None, regex=None):
        ''' https://www.mkyong.com/python/python-how-to-list-all-files-in-a-directory/
        Note: glob not work with some special char []
        '''
        path = path[:-1] if path.endswith('/') else path
        pattern = "/*.*"

        if endswith and isinstance(endswith, str):
            if '.' == endswith[0]: endswith = endswith[1:]
            pattern = "/*.%s" % endswith

        if recursive:
            pattern =  "/**" + pattern

        # Multiple matches
        if endswith and isinstance(endswith, list):
            files = []
            for end in endswith:
                end = ('/**' if recursive else '') + '/*.' + end.split('.')[-1]
                files.extend(glob.glob(path + end, recursive=recursive))
        else:
            files = glob.glob(path + pattern, recursive=recursive)

        if file_name_only:
            return [f.rsplit(os.sep, 1)[-1] for f in files]

        return [f for f in files]

    @staticmethod
    def remove_text_in(content, remove_texts=None, remove_callback=None):
        lines = [l.strip() for l in content.split('\n')]
        re = []
        for line in lines:
            if line:
                remove = False

                for remove_text in remove_texts:
                    if remove_text in line:
                        remove = True
                        break

                if not remove and remove_callback:
                    remove = remove_callback(line)

                if not remove: re.append(line)
            else:
                re.append(line)
        return '\n'.join(re)


    @staticmethod
    def remove_empty_line(text):
        return '\n'.join([line for line in text.split('\n') if line.strip()])

    @staticmethod
    def get_all_folders(path):
        lst = []
        for f in os.listdir(path):
            p =  PathUtils.join(path, f)
            if os.path.isdir(p):
                lst.append(p)
        return lst

    @staticmethod
    def copy_recursive_overwrite(src, dest, ignore=None):
        ''' https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all '''
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(src)
            if ignore is not None:
                ignored = ignore(src, files)
            else:
                ignored = set()
            for f in files:
                if f not in ignored:
                    FileUtils.copy_recursive_overwrite(os.path.join(src, f), os.path.join(dest, f), ignore)
        else:
            shutil.copyfile(src, dest)
            print('INFO: Copy %s -> %s' % (src, dest))

    @staticmethod
    def cp_flatten_only_format(root, format='.mobi'):
        dst = FileUtils.mkdir(root + '/flatten_folder')
        files_stage = {}
        for path, subdirs, files in os.walk(root):
            for name in files:
                if name.endswith(format):
                    src = os.path.join(path, name)
                    files_stage[src] = path

        for src, path in files_stage.items():
            shutil.copy(src, dst)  # file -> dir
            print('INFO: cp: %s -> %s' % (src, dst))

    @staticmethod
    def mv(src, dst, info=True):
        os.rename(src, dst)


    def cp_lst(self, files, dst, info=True):
        lst = []
        for src in files:
            dst = FileUtils.cp(src, dst, info=info)
            if dst: lst.append(dst)
        return lst

    @staticmethod
    def cp(src, dst, info=True):
        ''' Note: Be careful with create dir.
            src: Must be file
            dst: File or Dir
        '''
        try:
            if os.path.isfile(src):
                if '\\' in dst: dst = dst.replace('\\', '/')
                if dst.endswith('/'): dst = dst[:-1]

                path_dst, file_dst = dst.rsplit('/', 1)
                if '.' in file_dst: # is file
                    FileUtils.mkdir(path_dst)  # Make folder parent.
                else:
                    FileUtils.mkdir(dst)  # Make folder parent.
                    dst += '/' + src.rsplit('/', 1)[-1]

                copyfile(src, dst)  # file -> dir
                # shutil.copyfile(src, dst) # file -> file
                # shutil.copy(src, dst)   # file -> dir
                if info:
                    print('INFO: cp: %s -> %s' % (src, dst))
                return dst
        except Exception as e:
            print('error', e)
        return ''

    @staticmethod
    def rename_extension(file_path, new_ext):
        pre, ext = os.path.splitext(file_path)
        os.rename(file_path, pre + '.' + new_ext)
        print('INFO: rename %s -> %s' % (file_path, (pre + '.' +  new_ext)))

    @staticmethod
    def get_file_extension(file_path):
        ''' file.tar.gz '''
        return os.path.splitext(file_path)[1]

    @staticmethod
    def cp_all(src_path, dst):
        if not os.path.exists(dst):
            FileUtils.mkdir(dst)

        if os.path.isdir(src_path) and os.path.isdir(dst):
            for file in os.listdir(src_path):
                file_path = src_path + '/' + file
                FileUtils.cp(file_path, dst + '/' + file)
        else:
            raise Exception('ai_: src_path and dst must be directory')

    @staticmethod
    def flatten_all_file(destination, depth=None):
        if not depth:
            depth = []
        path = [destination] + depth
        path = os.path.join(*path)

        for file_or_dir in os.listdir(path):
            file = path + os.sep + file_or_dir
            file_exists = destination + os.sep + file_or_dir
            if os.path.isfile(file):
                if os.path.exists(file_exists):
                    print('Warn: file exist %s at destination' % (file))
                else:
                    shutil.move(file, destination)
                    print('Info: move %s -> %s' % (file, destination))
            else:
                path_2 = depth + [file_or_dir]
                FileUtils.flatten_all_file(destination, [os.path.join(*path_2)])

    @staticmethod
    def delete_empty_folder(destination):
        for file_or_dir in os.listdir(destination):
            dir = destination + os.sep + file_or_dir
            if os.path.isdir(dir) and not os.listdir(dir):
                print('empty folder')

    @staticmethod
    def mkdir(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
            return dir
        return dir

    @staticmethod
    def get_file_size(path):
        return os.path.getsize(path)

    @staticmethod
    def cache(key=None, data=None):
        path = FileUtils.conf.DIST_PATH + os.sep + key
        FileUtils.to_html_file(path=path, data=data)
        print('INFO: Cache %s' % path)
        return data

    @staticmethod
    def get_cache(key=None, data=None):
        path = FileUtils.conf.DIST_PATH + os.sep + key
        if data:
            return FileUtils.cache(key=key, data=data)
        print('INFO: Get cache %s' % path)
        return FileUtils.load_html_file(path=path)

    @staticmethod
    def read_file(path=None):
        if not path:
            path = FileUtils.conf.DIST_PATH + os.sep + 'text.txt'
        return FileUtils.load_html_file(path=path)

    @staticmethod
    def write_binary_file(path=None, data=None):
        if not path:
            path = FileUtils.conf.DIST_PATH + os.sep + 'text.txt'

        output_file = open(path, 'wb')
        output_file.write(data)
        output_file.close()
        print('Write binary file %s ' % path)

    @staticmethod
    def get_valid_file_path(filename):
        return FileUtils.remove_disallowed_filename_chars(filename)

    @staticmethod
    def remove_disallowed_filename_chars(filename):
        validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join(c for c in filename if c in validFilenameChars)

    @staticmethod
    def append_file(path=None, data=None):
        if not path:
            path = FileUtils.conf.DIST_PATH + os.sep + 'text.txt'

        FileUtils.conf.create_if_not_exist(path)
        with open(path, 'a', encoding='utf-8') as file:
            file.write(data)

    @staticmethod
    def write_file(path=None, data=None):
        if not path:
            path = FileUtils.conf.DIST_PATH + os.sep + 'text.txt'
        return FileUtils.to_html_file(path=path, data=data)

    @staticmethod
    def to_html_file(path=None, data=None, log=True):
        if not path:
            path = FileUtils.conf.DIST_PATH + os.sep + 'to_html.html'

        path, file = path.rsplit('/', 1)
        FileUtils.mkdir(path)
        output = path + '/' + FileUtils.get_valid_file_path(file)
        Path(output).write_text(data, encoding='utf-8')
        if log:
            print('INFO: Output file', output)

    @staticmethod
    def output_html_to_desktop(data, file_name=None):
        path = FileUtils.conf.USER_DESKTOP + '/' + (file_name if file_name else 'test_.html')
        FileUtils.to_html_file(path, data)
        print('INFO: Output html to desktop', path)

    @staticmethod
    def load_html_file(path=None, as_bytes=False):
        try:
            if not path:
                path = FileUtils.conf.DIST_PATH + os.sep + 'to_html.html'

            if as_bytes:
                with open(path, 'rb') as f:
                    contents = f.read()
                return str(contents)

            return Path(path).read_text(encoding='utf-8')
        except Exception as e:
            ''' https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in '''
            print('ERROR:  ', e, ' ::  will read as bytes, then convert to str')
            with open(path, 'rb') as f:
                contents = f.read()
            return str(contents)

    @staticmethod
    def to_csv_file(data, path):
        with open(path, 'w', encoding="utf-8", newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for row in data:
                spamwriter.writerow(row)

    @staticmethod
    def get_dir_of_file(file):
        if '\\' in file:
            file = file.replace('\\', '/')
        if '/' not in file:
            raise Exception('Cannot find directory')
        return file.rsplit('/', 1)[0]

    @staticmethod
    def _get_file_path(path, extension='pickle'):
        ext = '.' + extension
        if not path:
            path = PathUtils.join(FileUtils.conf.DIST_PATH, extension, 'tmps' + ext)
        if '/' not in path:
            path = PathUtils.join(FileUtils.conf.DIST_PATH, extension,  path)
        if not path.endswith(ext):
            path += ext
        return path

    @staticmethod
    def _get_pickle_path(path):
        return FileUtils._get_file_path(path, extension='pickle')

    @staticmethod
    def dump_object_to_file(data=None, path=None): # type: (any, str) -> None
        ''' Dump pickle '''
        file = FileUtils._get_pickle_path(path)
        FileUtils.mkdir(FileUtils.get_dir_of_file(file))
        pickle.dump(data, open(file, 'wb'))
        print('INFO: Dump object at:', file, '. Size: ', os.path.getsize(file))

    @staticmethod
    def load_object_from_file(path=None, default=None):
        ''' Load pickle '''
        file = FileUtils._get_pickle_path(path)

        if os.path.exists(file):
            print('INFO: Load object at: ', file)
            return pickle.load(open(file, 'rb'))

        print('ERROR: Pickle file not exists at: ', file)
        return default

    @staticmethod
    def is_exists_pickle(path):
        return os.path.exists(FileUtils._get_pickle_path(path))
    
    # Print object
    @staticmethod
    def print_dumps_file(path=None):
        if path and os.path.exists(path):
            value = pickle.load(open(path, 'rb'))
        else:
            path = FileUtils.conf.PICKLE_PATH + os.sep + 'tmps.pickle'
            value = pickle.load(open(path, 'rb'))

        print(value)

    @staticmethod
    def rename_file(path, old, new):
        if path.endswith('/') or path.endswith('\\'):
            path = path[:-1]

        src = path + os.sep + old
        dst = path + os.sep + new

        if os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
            print('INFO: Rename', src, '   ->    ', dst)

    @staticmethod
    def get_path_of_file(__file__):
        return os.path.dirname(os.path.abspath(__file__))


    @staticmethod
    def set_sys_path(__file__=None, root=None, if_run_in_tty=None): # type: (str, str, bool) -> None
        ''' Ex: root='..' '''
        __file__ = __file__ if __file__ else os.getcwd() + '/'
        if '\\' in __file__: __file__ = __file__.replace('\\', '/')

        # if if_run_in_tty != None: # todo: fix fail
        #     if if_run_in_tty == True and sys.stdin.isatty():
        #         FileUtils.set_sys_path(__file__, root)
        #     return

        if root:
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), root))
            sys.path.insert(0, path)
        else:
            # FileUtils.conf not define yet
            root = '..'
            for i, dir in enumerate(PathUtils._get_combination_path_from_file(__file__)):
                if 'definitions_prod.py' in [f for f in os.listdir(dir)]:
                    root = ('../' * i)[:-1]
                    break
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), root))
            sys.path.insert(0, path)

        print('INFO: sys.path.insert(0, "%s")' % path.replace('\\', '/') )

    @staticmethod
    def get_size_info(start_path='.'):
        total_size = 0
        files = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                files += 1

        return total_size, files

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def delete_file(file):
        if os.path.exists(file):
            os.remove(file)
            print('INFO: delete file: ' , file)

    @staticmethod
    def verify_image(img, debug=False, use_skimage=False):
        try:
            if not os.path.exists(img):
                return False

            if not os.path.getsize(img):
                return False

            if not imghdr.what(img):
                return False

            Image.open(img).verify()
            if use_skimage:
                io.imread(img, plugin='matplotlib') # https://medium.com/joelthchao/programmatically-detect-corrupted-image-8c1b2006c3d3 - check truncate
            return True
        except Exception as e:
            if debug:
                print(e)
            return False

    @staticmethod
    def get_folder_size(start_path='.'):
        if not os.path.exists(start_path):
            return 0, 0

        total_size = 0
        total_file = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if os.path.exists(fp) and not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
                    total_file += 1

        return total_size, total_file

    @staticmethod
    def calculate_file_system(path=None):
        from swissarmykit.utils.timer import Timer

        if FileUtils.conf.config['use_mongo_db'].value:
            from swissarmykit.db.mongodb import BaseDocument
            _file_system = BaseDocument.get_class('_file_system')
        else:
            from swissarmykit.db.mysql.record import BaseModel
            _file_system = BaseModel.get_class('_file_system')

        _file_system.drop_collection()
        should_del_empty = []
        if path:
            dir_lst = path if isinstance(path, list) else [path]
        else:
            dir_lst = FileUtils.get_all_folders(FileUtils.conf.HTML_PATH) + FileUtils.get_all_folders(FileUtils.conf.IMAGES_PATH)

        timer = Timer.instance(len(dir_lst), check_point=10)
        for dir in dir_lst:
            timer.check()
            size, no = FileUtils.get_folder_size(dir)
            if not size:
                should_del_empty.append(dir)
            _file_system.save_url(dir, name='file system', data={'size': size, 'no. files': str(no)})

            print('.', end='', flush=True)

        print('WARN: should delete empty folder', should_del_empty)

    @staticmethod
    def show_treemap_file_system(html_only=False):
        ''' https://janakiev.com/blog/python-filesystem-analysis/ '''

        import matplotlib.pyplot as plt
        import squarify
        plt.style.context('ggplot')
        plt.rc('font', size=8)
        fig = plt.gcf()
        fig.set_size_inches(20, 20)

        if FileUtils.conf.config['use_mongo_db'].value:
            from swissarmykit.db.mongodb import BaseDocument
            _file_system = BaseDocument.get_class('_file_system')
        else:
            from swissarmykit.db.mysql.record import BaseModel
            _file_system = BaseModel.get_class('_file_system')

        name = []
        size = []
        if html_only:
            files = _file_system.get_one(-1, desc=True).where(_file_system.url.contains(FileUtils.conf.HTML_PATH))
        else:
            files = _file_system.get_one(-1, desc=True)

        for f in files:
            data = f.get_data()
            if not data.get('no. files'): continue

            prefix = ''
            if FileUtils.conf.IMAGES_PATH in f.url:
                prefix = 'im_'

            name.append(prefix + f.url.split('/')[-1])
            size.append(data.get('size'))

        squarify.plot(sizes=size, label=name)
        plt.title('Extension Treemap by Size')
        plt.axis('off')
        plt.show()


    @staticmethod
    def datasets_to_csv(data, file_name=None):
        import pandas as pd
        df = pd.DataFrame(data=data['data'], columns=data['feature_names'])

        if file_name:
            f = FileUtils._get_file_path(file_name, extension='csv')
        else:
            f = PathUtils.join(FileUtils.conf.DIST_PATH, 'csv', data['filename'].rsplit(os.sep, 1)[-1])

        FileUtils.mkdir(FileUtils.get_dir_of_file(f))
        df.to_csv(f, sep=',', index=False)
        print('INFO: Output to ', f)

    @staticmethod
    def info_template():
        from swissarmykit.utils.fileutils import FileUtils
        file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')) + os.sep + 'definitions.py'
        content = FileUtils.read_file(file)
        output = FileUtils.conf.ROOT_DIR + os.sep + file.rsplit(os.sep, 1)[-1].replace('.py', '_prod.py')
        # FileUtils.write_file(FileUtils.conf.ROOT_DIR + os.sep + file.replace('.py', '_prod.py'), content)
        print('ERROR: Must create this file to determine the ROOT_DIR\n%s \n\n%s' % (output, content))



    @staticmethod
    def zip_dir(zip_dir=None, zip_name=None, lst=None):
        '''
        :param zip_name zip name
        :param zip_dir  path of folder
        Ref: https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/
        '''
        if zip_dir and lst or (not zip_dir and not lst):
            raise Exception('Please choose one of (zip dir or zip files) only')

        if lst:
            from zipfile import ZipFile
            if not zip_name: raise Exception('Must specify zip_name for list of files')
            sep = '/' if '/' in lst[0] else '\\'
            file_name = zip_name

            if '/' not in file_name:
                file_name = lst[0].rsplit(sep, 1)[0]

            if not file_name.endswith('.zip'):
                file_name += '.zip'

            timer = Timer.instance(len(lst))
            print('INFO: Start zip data ... Total: ', len(lst))

            with ZipFile(file_name, 'w') as zipObj2:
                for i, file in enumerate(lst):
                    if os.path.exists(file):
                        zipObj2.write(file, file.rsplit(sep)[-1])
                    timer.check(idx=i)

            print('INFO: Output to: ', file_name, ' From len(lst): ', len(lst), '\nExample: ', lst[0], '...')

        elif zip_dir:
            import shutil
            if zip_name:
                if '/' not in zip_name:
                    file_name = zip_dir.rsplit('/', 1)[0] + '/' + zip_name
                else:
                    file_name = zip_name
            else:
                file_name = zip_dir

            file_name = file_name.rstrip('.zip')
            print('INFO: Starting... zip dir: ', zip_dir)
            shutil.make_archive(file_name, 'zip', zip_dir)

            file_name += '.zip'
            print('INFO: Output to: ', file_name)

        return file_name

    @staticmethod
    def tail(file_name, lines):
        if os.path.exists(file_name):
            return '\n'.join(tailer.tail(open(file_name), lines))
        return ''

class PathUtils:

    @staticmethod
    def _get_combination_path_from_file(__file__):
        lst = __file__.split('/')
        lst_dir = []
        for _ in range(__file__.count('/'), 0, -1):
            lst_dir.append('/'.join(lst[:_]))
        return lst_dir

    @staticmethod
    def _get_root_dir(__file__):
        lst = __file__.split('/')
        for _ in range(__file__.count('/'), 0, -1):
            dir = '/'.join(lst[:_])
            if 'definitions_prod.py' in [f for f in os.listdir(dir)]:
                return dir
        return None

    @staticmethod
    def join(*paths):
        path = os.path.join(*paths)
        if os.sep == '\\':
            path = path.replace('\\', '/')
        return path

    @staticmethod
    def get_log_path():
        try:
            try:
                return FileUtils.conf.LOG_PATH
            except Exception as e1:
                # print(e1)
                pass

            print('WARN: Use inspect to get LOG_PATH')
            return 'C:/tmp' if platform.system() == 'Windows' else '/tmp'
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            exit()

    def __str__(self):
        return 'Path utils'


if __name__ == '__main__':
    # f = FileUtils()
    # print(f.get_all_files('C:/Users/Will/Desktop/deli/school/private'))

    # FileUtils.calculate_file_system()
    # FileUtils.show_treemap_file_system()
    # print(FileUtils.load_from_clipboard())
    # FileUtils.datasets_to_csv(data)

    print(FileUtils.tail('C:/Users/Will/Desktop/code/_ml/ztest/test.py', 10))

    # FileUtils.zip_dir(['C:/Users/Will/Desktop/tmp/STEP 5 _ 6 - Specific Condo page to collect information 1-3.jpg'], zip_name='1100-12000')