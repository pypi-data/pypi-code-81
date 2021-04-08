#!/usr/bin/env python
# coding: utf-8

""" doc
  see
    https://zhuanlan.zhihu.com/p/26159930
    https://pypi.org/project/twine/

  # 执行下列命令前, 需要先更新版本号
  1. python setup.py sdist
  2. twine upload dist/tangUtils-0.2.0.tar.gz
"""

from setuptools import setup

with open("README.md", mode="r", encoding="UTF-8") as f:
  readme = f.read()

setup(
  name="tangUtils",
  version="0.2.0",
  author="xiaomingtang",
  author_email="1038761793@qq.com",
  url="https://github.com/xiaomingTang/python-utils",
  description=u"文件/目录相关utils",
  long_description=readme,
  long_description_content_type="text/markdown",
  requires_python=">=3.5",
  packages=["tangUtils"],
  install_requires=[
    "pillow"
  ],
  entry_points={
    "console_scripts": []
  }
)