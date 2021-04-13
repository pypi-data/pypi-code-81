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
  version='1.2.1',
  description='Very easy to use discord.py economy creator',
  long_description="Read our docs at https://docs.simpleco.xyz\nDiscord support server: https://discord.gg/ptC9CaQFRe" + '\n\n' + "Change Log\n===========\n\n1.1.7 (08/04/2021)\n------------------\n- Added leaderboard\n- Added variable adding to database",
  url='',  
  author='MrStretch',
  author_email='mrstretchd@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Ecomomy, Simple, discord.py', 
  packages=find_packages(),
  install_requires=['aiosqlite']
)
