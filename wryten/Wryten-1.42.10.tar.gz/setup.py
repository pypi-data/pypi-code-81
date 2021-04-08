#!/usr/bin/env python
import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"([^"]*)"',
    open("suplemon/main.py").read(),
    re.M
    ).group(1)

files = ["config/*.json", "themes/*", "modules/*.py", "linelight/*.py"]

#
# Linage:
#
#      url="https://github.com/bagage/suplemon/"
#
#      url="https://github.com/richrd/suplemon/",
#      author_email="richrd.lewis@gmail.com",
#      author="Richard Lewis",
#

setup(name="Wryten",
      version=version,
      description="Programable Console IDE",
      author="Scott McCallum",
      author_email="sm@intermine.com",
      url="https://github.com/streamcoders/wryten/",
      packages=["suplemon"],
      package_data={"": files},
      include_package_data=True,
      install_requires=[
          "pyperclip",
          "pygments",
          "wcwidth",
          "windows-curses; platform_system=='Windows'"
      ],
      entry_points={
          "console_scripts": ["e=suplemon.cli:main","wryten=suplemon.cli:main"]
      },
      classifiers=[]
      )
