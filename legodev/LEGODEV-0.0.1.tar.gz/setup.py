from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='LEGODEV',
  version='0.0.1',
  description='Libraries to assist competitors with common tasks or sequence of tasks',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Muhammed Hamzah, Thabeeshan Sarathasegaram, Vinu Venkatesh Muthukumar, Jiafei Lin',
  author_email='wropythonmodule@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='legodev', 
  packages=find_packages(),
  install_requires=['ev3dev2', 'time'] 
)