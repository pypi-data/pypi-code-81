from setuptools import setup, find_packages
 
classifiers = [

      'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
setup(
  name='joecalc',
  version='1.0',
  description='joe calc',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='yahya',
  author_email='mmr168733@gmail.com',
  license='Apache', 
  classifiers=classifiers,
  keywords='calc', 
  packages=find_packages(),
  install_requires=[''] 
)
