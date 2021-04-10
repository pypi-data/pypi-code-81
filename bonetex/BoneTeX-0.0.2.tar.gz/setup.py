#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/18 21:43
# @Author : 詹荣瑞
# @File : setup.py
# @desc : 本代码未经授权禁止商用
from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()
extras = {
    'docs': ['sphinx'],
    'matrices': ['numpy'],
    'matplotlib': ['matplotlib'],
    'quantities': ['quantities', 'numpy'],
    'testing': ['flake8<3.0.0', 'pep8-naming==0.8.2',
                'flake8_docstrings==1.3.0', 'pycodestyle==2.0.0',
                'pydocstyle==3.0.0', 'pyflakes==1.2.3', 'nose', 'flake8-putty',
                'coverage'],
    'convert_to_py2': ['3to2', 'future>=0.15.2'],
}
setup(
    name="BoneTeX",
    version="0.0.2",
    author="六个骨头",
    author_email="2742392377@qq.com",
    description="""BoneTeX Core是一个自动生成LaTeX代码的辅助库，
    你也可以使用Python高效的完成LaTeX文档的编写，
    同时支持将MarkDown、Excel等文件转换成LaTeX代码。""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/zrr1999/bonetex",
    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(),
    package_data={
        '': ['*.txt'],
        # 包含demo包data文件夹中的 *.dat文件
        'demo': ['data/*.dat'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    platforms="any",
    install_requires=[],
    extras_require=extras,
    entry_points={
        'console_scripts': [
            'bonetex=bonetex.bonetex_command:main',
            'bonetex-server=bonetex.server.server:app.run',
        ]
    }
)
