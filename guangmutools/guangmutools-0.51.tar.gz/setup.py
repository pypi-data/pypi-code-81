# -*- encoding: utf-8 -*-
'''
@文件    :setup.py
@说明    :
@时间    :2021/02/22 17:52:41
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

from setuptools import setup, find_packages
from guangmutools import __version__

setup(
    name="guangmutools",
    version=__version__,
    keywords=["helpers", "tools", "widgets"],
    description="collection of some tools for guangmu system",
    long_description="collection of tools",
    license="MIT Licence",

    url="https://gitlab.xsjcs.cn/kefu/guangmu/commonutils.git",
    author="caimiao",
    author_email="caimiao@kingsoft.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pika", "requests", "redis", "pymysql"]
)