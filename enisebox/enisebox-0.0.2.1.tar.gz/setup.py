# import setuptools
# from distutils.core import setup

from setuptools import setup
setup(
      name = 'enisebox',
      packages = ['enisebox'],
      package_data = {},
      version = '0.0.2.1',
      description = 'A lib for making video games',
      author = 'BagEddy42',
      author_email = 'Info@enise.fr',
      keywords = ['game', 'physics'], # arbitrary keywords
      install_requires=[
          'box2d',
          'guizero',
      ],
      classifiers = [],
)
