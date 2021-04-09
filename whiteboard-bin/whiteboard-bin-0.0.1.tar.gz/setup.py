from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='whiteboard-bin',
    version='0.0.1',
    description='A lightweight package information utility. ',
    long_description=readme,
    author='Garrett Howard',
    author_email='garrett@mersh.com',
    url='https://github.com/howardjs/whiteboard',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)