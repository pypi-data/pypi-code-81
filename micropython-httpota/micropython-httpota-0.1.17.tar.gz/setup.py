import os
import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup

setup(
    name='micropython-httpota',
    py_modules=['HttpOTA'],
    version=os.environ['VERSION'],
    description='MicroPython library for OTA updates using HTTP',
    long_description='this library lets you periodically ping an HTTP server for a manifest and pointer to a package',
    long_description_content_type='text/x-rst',
    keywords='micropython OTA http',
    url='https://github.com/leprechaun/micropython-http-ota',
    author='Leprechaun',
    author_email='leprechaun@gmail.com',
    maintainer='Leprechaun',
    maintainer_email='leprechaun@gmail.com',
    license='MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'License :: OSI Approved :: MIT License',
    ]
)
