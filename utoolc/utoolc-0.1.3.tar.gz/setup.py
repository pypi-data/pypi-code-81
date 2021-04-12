#!/usr/bin/env python
import os
from setuptools import setup, find_packages

from utoolc import __version__ as version
from utoolc import __author__ as author
from utoolc import __email__ as email

maintainer = author
maintainer_email = email
author = maintainer
author_email = maintainer_email
description = "❤PyJustToolc(utoolc) > Python Tools For U (You)❤"

# 代码可用
# 有的将README成为其long_description 这里是读取其内容的代码
# win =>【'C:\\_developSoftKu\\ideaIU-2019.1.3.win\\#CodeKu\\pythonKu\\PyJustToolc'】
# mac =>【'/Volumes/MacOS-SSD-LCKu/DevelopSoftKu/pycharm/codeKu/PyJustToolc'】
here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#     README = f.read()
# with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
#     REQUIREMENTS = f.read()

# 从 docs/README-PYPI.rst 读取出内容 当 LONG_DESCRIPTION
with open(os.path.join(here, 'docs/README-PYPI.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# 赋值给 long_description
long_description = LONG_DESCRIPTION

install_requires = [
    'psutil>=5.8.0',
    'requests>=2.25.1',
    'twine>=3.4.1',
    'wheel>=0.36.2',
]

license = 'LICENSE'

keywords = [
    "utoolc", "PyJustToolc", "Python Tools For U (You)"
]

name = 'utoolc'
platforms = ['Windows', 'MacOS', 'Linux']
# github
# url = 'https://github.com/ahviplc/PyJustToolc'
# gitee
url = 'https://gitee.com/ahviplc/PyJustToolc'
download_url = 'https://pypi.org/project/utoolc/#files'
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
]

test_suite = 'tests.utoolc_test'

setup(author=author,
      author_email=author_email,
      description=description,
      license=license,
      long_description=long_description,
      install_requires=install_requires,
      maintainer=maintainer,
      name=name,
      packages=find_packages(exclude=('tests', 'examples')),  # 打包 排除一些 这里排除【tests】包 和 examples文件夹（其实本来也搜不到） - 它默认在和setup.py同一目录下搜索各个含有 init.py的包
      # package_dir={'': 'lib'},  # 没玩明白呢 - 告诉setuptools哪些目录下的文件被映射到哪个源码包 表示“root package”中的模块都在lib目录中
      package_data={'': ['*.txt', '*.dat']},  # 已测试 可用 将打包时的测试文件删除了 注意 需要带* 打包其包含的所有.txt文件和.dat文件【utoolc路径下所有】 包含utoolc/utils下所有*.txt文件 和 utoolc下所有*.txt文件
      include_package_data=True,  # 默认情况下False 则不包含非python包文件(例如您列出的不在“包中”的测试py文件) 反之包含.
      zip_safe=False,  # 其为False 则出现的不是一个*.egg文件，而是一个文件夹.
      platforms=platforms,
      url=url,
      download_url=download_url,
      version=version,
      test_suite=test_suite,
      classifiers=classifiers)

# 个人对使用packages相关参数的看法，
# 首先告诉程序去哪个目录中找包，因此有了packages参数，【packages=find_packages('utoolc') 带这个'utoolc'的 没玩明白呢 】
# 其次，告诉程序我包的起始路径是怎么样的，因此有了package_dir参数 【没玩明白呢 package_dir={'':'lib'}】
# 最后，找到包以后，我应该把哪些文件(非py文件)打到包里面，因此有了package_data参数
# 【package_data={'': ['*.txt','*.dat']},注意 需要带* 包含所有.txt文件和.dat文件【utoolc路径下所有】】
