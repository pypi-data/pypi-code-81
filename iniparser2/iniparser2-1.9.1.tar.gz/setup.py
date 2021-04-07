import setuptools

def read(fname):
	with open(fname,'r') as f:
		return f.read()

setuptools.setup(
name='iniparser2',
version='1.9.1',
author='HugeBrain16',
author_email='joshtuck373@gmail.com',
description='An INI parser or config parser',
license='MIT',
keywords='iniparser configparser ini config parser file',
url='https://github.com/HugeBrain16/iniparser2',
project_url= {
		"Bug Tracker": 'https://github.com/HugeBrain16/iniparser2/issues'	
	},
packages=setuptools.find_packages(),
long_description=read('README.md'),
long_description_content_type='text/markdown',
classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
	]
)