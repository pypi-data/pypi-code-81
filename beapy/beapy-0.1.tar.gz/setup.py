import pathlib
from setuptools import setup


cwd = pathlib.Path(__file__).parent
long_description = (cwd / 'README.md').read_text()

setup(
	name = 'beapy',
	packages = ['beapy'],
	description = (
		'A pandas-based python package for requesting data from the U.S. '
		'Bureau of Economic Analysis'
	),
	version = '0.1',
	license = 'MIT',
	long_description_content_type = 'text/markdown',
	long_description = long_description,
	author = 'hotzsauce',
	author_email = 'githotz@gmail.com',
	url = 'https://www.github.com/hotzsauce/bea-dev',
	keywords = ['economics', 'bea', 'bureau of economic analysis', 'nipa'],
	install_requires = [
		'numpy',
		'pandas',
		'requests'
	],
	include_package_data = True,
	classifiers = [
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.7'
	]
)