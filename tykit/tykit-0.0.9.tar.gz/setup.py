'''
Description: 
version: 
Author: TianyuYuan
Date: 2021-04-02 15:41:57
LastEditors: TianyuYuan
LastEditTime: 2021-04-13 17:08:45
'''
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="tykit",
  version="0.0.9",
  author="tyyuan",
  author_email="1374736649@qq.com",
  description="A tool kit of progress bars and console logs with rich output",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/paperplane110/tykit",
  packages=setuptools.find_packages(),
  install_requires=['rich>=9'],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)