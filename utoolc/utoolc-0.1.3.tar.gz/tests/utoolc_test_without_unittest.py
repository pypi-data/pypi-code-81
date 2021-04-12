import os
import utoolc


# # 如果utoolc/__init__.py:23中__all__去掉 get_random 则不会找到Ta【NameError: name 'get_random' is not defined】
# from utoolc import *
# def test():
#     utils.print_a_line()
#     print(__version__)
#     print(get_random.get_random_str_with_counts(5))
#     utils.print_a_line()

def test2():
    # 使用相对路径 无不同系统下的路径拼接问题
    utoolc.do.do_cverter('markdown', 'rst', '../README.md', '../README_ok.rst')
    utoolc.do.do_cverter("rst", "markdown", '../docs/README-PYPI.rst', '../README_ok.md')


def test3():
    project_path = os.path.abspath('..')
    # project_path 不同系统路径是不一样的【win \】【mac /】故要使用【os.path.join()】来拼接路径
    # win =>【C:\_developSoftKu\ideaIU-2019.1.3.win\#CodeKu\pythonKu\PyJustToolc】
    # mac =>【/Volumes/MacOS-SSD-LCKu/DevelopSoftKu/pycharm/codeKu/PyJustToolc】
    print(project_path)
    # 使用绝对路径
    utoolc.do.do_cverter('markdown', 'rst', os.path.join(project_path, 'README.md'), os.path.join(project_path, 'README_ok2.rst'))
    utoolc.do.do_cverter("rst", "markdown", os.path.join(project_path, 'docs', 'README-PYPI.rst'), os.path.join(project_path, 'README_ok2.md'))


def test4():
    # 使用 utoolc.do 统一使用入口 当然其他入口也开放 自由发挥
    utoolc.do.utils.print_a_line()
    print(utoolc.do.get_num_cpu())
    print(utoolc.do.get_random.get_random_str_with_counts(3))
    print(utoolc.do.get_os())
    print(utoolc.do.is_mac_os())
    print(utoolc.do.is_win_os())
    print(utoolc.do.is_linux_os())
    print(utoolc.do.get_num_cpu())
    utoolc.do.utils.print_a_line()


if __name__ == '__main__':
    # test()
    # test2()
    # test3()
    test4()
    pass
