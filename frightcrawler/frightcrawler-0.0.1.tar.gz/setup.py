import frightcrawler
from setuptools import setup, find_packages

with open('README.md', 'r') as readmefile:
    readme = readmefile.read()

setup(
    name='frightcrawler',
    version='0.0.1',
    author='charlesrocket',
    license='MIT',
    description='MtG deck legality checker',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/charlesrocket/frightcrawler',
    install_requires=[
        'dictor>=0.1.6',
        'requests>=2.25.0',
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    entry_points={
        'console_scripts':['frightcrawler=frightcrawler.frightcrawler:main'],
    },
)
