from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Gask',
    version='0.4',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RyanVanDijck/Gask',
    license='GNU General Public License v3',
    author='ryan',
    author_email='rvandijck02@outlook.com',
    entry_points={
        'console_scripts': [
            'gask = gask.gask:main',
        ],
    },
    install_requires=['gitpython',
                      'terminaltables',
                      'pick'],
    extras_require={
        'burndown': ['matplotlib'],
    },
    description='A git backed task management system'

)
