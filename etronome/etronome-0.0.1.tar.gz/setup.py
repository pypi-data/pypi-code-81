import pathlib

from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='etronome',
    version='0.0.1',
    description='Keep track of a rythm',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/wpbindt/metronome',
    author='Wessel Bindt',
    author_email='wesselbindt@gmail.com',
    license='GNU',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.8'
    ],
    packages=['etronome'],
    include_package_data=True,
)

