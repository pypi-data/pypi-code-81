from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyHPump',
  version='2.0.4',
  description='basic pump application',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Camil Milos',
  author_email='mcamil16@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='psd',
  packages=find_packages(),
  install_requires=['pyserial']
)