from setuptools import setup, find_packages

with open('README.md') as readme_file:
	README = readme_file.read()

setup_args = dict(
	name='chorecore',
	version='1.1.0',
	description='Utilities to simplify many commonly used pieces of code',
	long_description_content_type="text/markdown",
	long_description=README,
	license='ISCL',
	packages=find_packages(),
	author='Jacob Schwartz',
	author_email='support@chorecore.com',
	keywords=['ChoreCore', 'Chore', 'Core'],
	url='https://github.com/JTSchwartz/chorecore-py',
	download_url='https://pypi.org/project/chorecore/',
	project_urls={
		"Bug Tracker": "https://github.com/JTSchwartz/chorecore-py/issues",
	},
	classifiers=[
		"License :: OSI Approved :: ISC License (ISCL)",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3.8",
		"Topic :: Utilities"
	],
	python_requires=">=3.8",
)

if __name__ == '__main__':
	setup(**setup_args)
