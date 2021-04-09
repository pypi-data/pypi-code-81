"""Anduin: A light python mysql connector.

Copyright (c) 2020-2024 Campanula<campanulamediuml@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""
# <=========>
import codecs
import os
from setuptools import setup

VER = "5.0.3"

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

if __name__ == '__main__':
    setup(
        # 以下为必需参数
        name='anduin',  # 模块名
      "5.0.3"
        description='a lite mysql & sqlite3 connect engine, mapping table into k-v structure',  # 简短描述
        py_modules=["anduin"],  # 单文件模块写法
        # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法
        license='MIT',
        long_description=read("README.rst"),
        author='campanula',
        author_email='421248329@qq.com',
        platforms='any',
        keywords="mysql , sqlite3 , sql engine",
        # packages = find_packages('anduin'),
        # package_dir = {'anduin':'*'},
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
        url='https://github.com/campanulamediuml/Anduin',
        install_requires=[
            'pymysql==0.10.1',
        ],
        include_package_data=True,
        zip_safe=True,
        packages=['anduin', 'anduin/dbserver'],
        python_requires='>=3.2',
    )
