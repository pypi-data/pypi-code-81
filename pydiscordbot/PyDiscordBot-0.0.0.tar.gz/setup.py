from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='PyDiscordBot',
  version='0.0.0',
  description='A very basic discord bot for begginer',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='LeftandRight',
  author_email='wempaleft@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='BOT', 
  packages=find_packages(),
  install_requires=['discord'] 
)
