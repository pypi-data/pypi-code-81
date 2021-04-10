from setuptools import setup, find_packages
 
classifiers = [
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.9'
]
 
setup(
  name='jwringcentral',
  version='0.0.1',
  description='Some methods on importing/exporting data and DF manipulation',
  include_package_data=True,
  author='Jiayi(Mike) Wang',
  author_email='jiayiwang08@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  packages=find_packages(),
  install_requires=[''] 
)