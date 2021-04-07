#
# Copyright (c) 2018-2021 T. {Benz,Kramer}.
#
# This file is part of verilog-parser 
# (see https://codeberg.org/tok/py-verilog-parser).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from setuptools import setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(name='verilog-parser',
      version='0.0.1',
      description='Parser for structural verilog.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='verilog parser',
      classifiers=[
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Development Status :: 3 - Alpha',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
          'Programming Language :: Python :: 3'
      ],
      url='https://codeberg.org/tok/py-verilog-parser',
      author='T. (Benz|Kramer)',
      author_email='dont@spam.me',
      license='AGPL',
      install_requires=[
          'lark-parser',
      ],
      packages=['verilog_parser'],
      zip_safe=False)
