from setuptools import setup, find_packages

setup(name='decoder',
	version='0.2',
	description='A simple script to try and decode a string in various encoding mechanisms regardless of it\'s (original) type.',
	url='https://github.com/Anon-Exploiter/decoder',
	author='Syed Umar Arfeen',
	author_email='umar.arfeen@outlook.com',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'pycipher',
		'termcolor',
	],
	entry_points={
		'console_scripts': [
			'decoder = decoder.decoder:main'
		],
	},
	zip_safe=False
)
