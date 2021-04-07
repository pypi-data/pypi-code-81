import os
import sys

class PathUtils:

    @staticmethod
    def set_sys_path(file_path=None, root=None): # type: (str, str) -> None
        ''' Ex: root='..'
            find definitions_prod.py recursive to import swissarmykit_conf
        '''
        file_path = file_path if file_path else os.getcwd() + '/'
        file_path = file_path.replace('\\', '/')

        if root:
            path = os.path.abspath(os.path.join(os.path.dirname(file_path), root))
            sys.path.insert(0, path)
            print('INFO: sys.path.insert(0, "%s")' % path.replace('\\', '/'))
            return True
        else:
            # swissarmykit_conf not define yet
            root = '..'
            found = False
            for i, dir in enumerate(PathUtils._get_combination_path_from_file(file_path)):
                if 'definitions_prod.py' in [f for f in os.listdir(dir)]:
                    root = ('../' * i)[:-1]
                    found = True
                    break
            if found:
                path = os.path.abspath(os.path.join(os.path.dirname(file_path), root))
                sys.path.insert(0, path)
                print('INFO: sys.path.insert(0, "%s")' % path.replace('\\', '/') )
                return True
            else:
                print('WARN: set_sys_path: definitions_prod.py not found')

        return False

    @staticmethod
    def _get_combination_path_from_file(file_path):
        ''' List all path from current file_path '''
        lst = file_path.split('/')
        lst_dir = []
        for _ in range(file_path.count('/'), 0, -1):
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
    def get_cwd():
        return os.getcwd()

    @staticmethod
    def join(*paths):
        path = os.path.join(*paths)
        if os.sep == '\\':
            path = path.replace('\\', '/')
        return path

    def __str__(self):
        return 'Path utils'

if __name__ == '__main__':
    print(PathUtils._get_combination_path_from_file(__file__))

    root = '..'
    for i, dir in enumerate(PathUtils._get_combination_path_from_file(__file__)):
        if 'definitions_prod.py' in [f for f in os.listdir(dir)]:
            root = ('../' * i)[:-1]
            break
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), root))
    print(path)
