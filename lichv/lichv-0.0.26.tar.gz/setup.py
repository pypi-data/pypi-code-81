from distutils.core import setup
from setuptools import find_packages

setup(
	name = 'lichv',
	version = '0.0.26',
	description = 'Utility tools with mysqldb,postgresql,utils',
	long_description = 'Utility tools with mysqldb,postgresql,utils', 
	author = 'lichv',
	author_email = 'lichvy@126.com',
	url = 'https://github.com/lichv/python',
	license = '',
	install_requires = [
		'requests>=2.25.1',
		'pymysql>=0.9.3',
		'psycopg2>=2.8.6',
		'bs4>=0.0.1',
	],
	python_requires='>=3.6',
	keywords = '',
	packages = find_packages('src'),
	package_dir = {'':'src'},
	include_package_data = True,
)
