from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='statementhelper',
  version='0.0.1',
  description='Definitions and examples for common Python statements.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ryan Chou',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='help', 
  packages=find_packages(),
  install_requires=[''] 
)