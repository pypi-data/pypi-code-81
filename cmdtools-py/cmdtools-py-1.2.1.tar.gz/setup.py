import setuptools
import re

def getversion(file='cmdtools.py'):
	for line in open(file,'r').readlines():
		res = re.findall(r'^\s*__version__\s*=(.*)',line.strip())
		if res:
			return res[0].strip().replace("'",'')

setuptools.setup(
name='cmdtools-py',
description='a module for parsing and processing commands.',
version=getversion(),
author='HugeBrain16',
author_email='joshtuck373@gmail.com',
license='MIT',
keywords='command-parser command-processor command cmd cmd-parser',
url='https://github.com/HugeBrain16/cmdtools',
py_modules=['cmdtools'],
long_description=open('README.md','r').read(),
long_description_content_type='text/markdown',
classifiers=[
		"Development Status :: 4 - Beta",
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Developers'
	]
)