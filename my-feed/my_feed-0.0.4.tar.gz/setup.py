from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

packages = find_packages(exclude=['tests*'])

setup(
    name='my_feed',
    version='0.0.4',
    license='LGPLv3',

    author='SimoneABNto',
    description='A single service to get all your feed',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SimoneABNto/My-Feed',

    packages=packages,
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],

    python_requires='>=3.7',
    install_requires=[
        'requests',
        'bs4'
    ],
)
