from __future__ import division, print_function

import io
import os
import re
import sys

try:
    from setuptools import find_packages, setup
except ImportError:
    print('Package setuptools is missing from your Python installation. Please see the installation section of '
          'the README for instructions on how to install it.')
    exit(1)


# Example code to pull version from esptool.py with regex, taken from
# http://python-packaging-user-guide.readthedocs.org/en/latest/single_source_version/
def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = """
==========
lfstool.py
==========
A command line utility to sync local folder with a remote LittleFS partition. It communicates with the ROM bootloader in Espressif ESP8266 & ESP32 microcontrollers only. 

Internally lfstool.py uses esptool when communicating with microcontrollers.

The lfstool.py project is hosted on github: https://github.com/iotctl/lfstool

Installation
------------

lfstool can be installed via pip:

  $ pip install lfstool -U

lfstool supports Python 3.5 or newer.

lfstool supports both ESP8266 & ESP32.

Usage
-----

Please see the `Usage section of the README.md file <https://github.com/iotctl/lfstool#usage>`_.

You can also get help information by running `lfstool.py --help`.

Contributing
------------
Please see the `CONTRIBUTING.md file on github <https://github.com/iotctl/lfstool/blob/master/CONTRIBUTING.md>`_.
"""

# For Windows, we want to install esptool.py.exe, etc. so that normal Windows command line can run them
# For Linux/macOS, we can't use console_scripts with extension .py as their names will clash with the modules' names.
if os.name == "nt":
    scripts = None
    entry_points = {
        'console_scripts': [
            'esptool.py=esptool:_main',
            'espsecure.py=espsecure:_main',
            'espefuse.py=espefuse:_main',
        ],
    }
else:
    scripts = ['lfstool.py']
    entry_points = None

setup(
    name='lfstool',
    py_modules=['lfstool'],
    version=find_version('lfstool.py'),
    description='A serial utility to sync local folder to Espressif ESP8266 & ESP32 chips.',
    long_description=long_description,
    url='https://github.com/iotctl/lfstool',
    author='Pavel Sklenar (pajikos)',
    author_email='sklenar.pav@gmail.com',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        # 'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Embedded Systems',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    setup_requires=['wheel'] if sys.version_info[0:2] not in [(3, 4), (3, 5)] else [],
    install_requires=[
        'esptool==3.0',
        'Cython==0.29.21',
        'littlefs-python==0.2.0'
        
    ],
    packages=find_packages(),
    scripts=scripts,
    entry_points=entry_points,
)
