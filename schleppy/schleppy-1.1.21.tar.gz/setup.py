from setuptools import setup, find_packages
from m2r import convert

with open("README.md", "r") as fh:
    long_description = convert(fh.read())

setup(name='schleppy',
      version='1.1.21',
      description='Utilities for traversing and transforming data structures',
      long_description=long_description,
      description_content_type="text/markdown",
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],
      keywords='dict list path dot notation',
      url='http://github.com/bradodarb/schleppy',
      author='Brad Murry',
      author_email="bradodarb@hotmail.com",
      license='MIT',
      packages=find_packages(exclude=['test*']),
      include_package_data=True,
      zip_safe=False)
