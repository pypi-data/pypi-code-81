from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SimpleEconomy',
  version='1.1.5',
  description='Very easy to use discord.py economy creator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='MrStretch',
  author_email='mrstretchd@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Ecomomy, Simple, discord.py', 
  packages=find_packages(),
  install_requires=['aiosqlite']
)
