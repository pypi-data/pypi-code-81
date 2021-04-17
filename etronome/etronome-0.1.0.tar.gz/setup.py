import pathlib

from setuptools import find_packages, setup


here = pathlib.Path(__file__).parent

readme = (here / 'README.md').read_text()

packages = find_packages(exclude=('tests',))

setup(
    name='etronome',
    version='0.1.0',
    description='Keep track of a rythm',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/wpbindt/metronome',
    author='Wessel Bindt',
    author_email='wesselbindt@gmail.com',
    license='GNU',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.8'
    ],
    packages=packages,
    include_package_data=True,
)

