# -*- coding:utf-8 -*-

import os
import setuptools

requirements = []

requirements_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
if os.path.isfile(requirements_txt):
    with open(requirements_txt, 'r+') as fo:
        for line in fo.readlines():
            item = line.split('#')[0].strip()
            if len(item):
                requirements.append(item)

setuptools.setup(
    name="quicly-mongo",
    version="0.0.2",
    keywords=["mongo"],
    author="muxiaofei",
    author_email="muxiaofei@gmail.com",
    description="Quicly Mongo",
    long_description="",
    long_description_content_type="text/x-rst",
    url="https://gitee.com/muxiaofei/quicly-mongo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)
