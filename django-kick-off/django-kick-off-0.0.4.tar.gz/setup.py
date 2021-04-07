from setuptools import setup, find_packages


with open('readme.md', 'r') as fh:
	long_description = fh.read()
	fh.close()

setup(
    name='django-kick-off',
    version='0.0.4',
	url="https://github.com/ignacio-nava/django-kick-off",
	author="Ignacio Nava",
	author_email="nava_ignacio@outlook.com",
	description='Start a virtual environment and a fully configurated Django project with an app',
	py_modules='kick_off',
	package_dir={'': 'src'},
	packages=find_packages(where="src"),
	include_package_data=True,
	python_requires=">=3.6",
	classifiers=[
		'Environment :: Console',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'License :: OSI Approved :: MIT License',
		'Operating System :: MacOS',
		'Topic :: Software Development',
	],
	long_description=long_description,
	long_description_content_type="text/markdown",
	extras_require={
		"dev": [
			"pytest>=3.6",
			"check-manifest",
		],
	},
)
