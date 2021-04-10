from setuptools import setup
from setuptools import find_packages


setup(name='whacc',
      version='0.0.12',
      description='largely automatic and customizable pipeline for creating a CNN to predict whiskers contacting objects',
      packages=find_packages(),
      author_email='phillip.maire@gmail.com',
      zip_safe=False,
      install_requires=[
       # "pyicu",
       "natsort==7.1.1"])
"""
cd /Users/phil/Dropbox/HIRES_LAB/GitHub/whacc
python3 setup.py sdist bdist_wheel
twine upload dist/* -u phillip_maire -p stayCurious9084!
"""
