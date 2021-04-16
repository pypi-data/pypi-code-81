from setuptools import setup, find_packages

setup(
  name='randpass',
  version='1.0.2',
  description='Create a random password that is memorable to humans',
  long_description='Create a random password that is memorable to humans',
  url='http://cct.lsu.edu/~sbrandt/',
  author='Steven R. Brandt',
  author_email='steven@stevenrbrandt.com',
  license='LGPL',
  entry_points = {
    'console_scripts' : ['randpass=randpass:main'],
  },
  packages=['randpass']
)
