import os
import sys
import platform


class SysUtils:

    @staticmethod
    def is_win():
        return platform.system() == 'Windows'

    @staticmethod
    def set_sys_path(__file__=None, root=None):
        f = __file__ if __file__ else os.getcwd()
        if '\\' in f: f = f.replace('\\', '/') + '/'

        if root:
            path = os.path.abspath(os.path.join(os.path.dirname(f), root))
            sys.path.insert(0, path)
        else:
            root = '..'

            lst = f.split('/')
            lst_dir = []
            for _ in range(f.count('/'), 0, -1):
                lst_dir.append('/'.join(lst[:_]))

            for i, dir in enumerate(lst_dir):
                if 'definitions_prod.py' in [f for f in os.listdir(dir)]:
                    root = ('../' * i)[:-1]
                    break
            path = os.path.abspath(os.path.join(os.path.dirname(f), root))
            sys.path.insert(0, path)

        print('INFO: sys.path.insert(0, "%s")' % path.replace('\\', '/'))



if __name__ == '__main__':
    s = SysUtils()
    s.set_sys_path()
