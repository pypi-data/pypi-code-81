from frightcrawler import __version__
from setuptools import setup, find_packages

with open('README.md', 'r') as readmefile:
    readme = readmefile.read()

setup(
    name='frightcrawler',
    version=__version__,
    author='charlesrocket',
    license='MIT',
    description='MtG deck legality checker',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/charlesrocket/frightcrawler',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Natural Language :: English',
    ],
    install_requires=[
        'dictor>=0.1.6',
        'requests-cache>=0.6.0',
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':['frightcrawler=frightcrawler.frightcrawler:main'],
    },
)
