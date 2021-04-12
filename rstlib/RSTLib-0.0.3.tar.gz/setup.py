from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='RSTLib',
  version='0.0.2',
  description='An implementation of Rough Set Theory that can work with inconsistent data',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Prasad,Shikhar,Sumedh',
  author_email=' deepakmd17.extc@coep.ac.in, manojbm17.extc@coep.ac.in, sumedhms17.extc@coep.ac.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='RST', 
  packages=find_packages(),
  install_requires=['pandas']
)