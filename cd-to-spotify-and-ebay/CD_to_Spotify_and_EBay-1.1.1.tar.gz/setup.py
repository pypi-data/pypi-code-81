from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '1.1.1'
DESCRIPTION = 'Transfer the songs from your old CDs to a Spotify Playlist and list the CDs on eBay'

# Setting up
setup(
    name="CD_to_Spotify_and_EBay",
    version=VERSION,
    author="Alexander Halpern",
    author_email="<halperna22@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['spotipy', 'PyYAML','ebaysdk', 'pyserial'],
    keywords=['python', 'spotify', 'ebay'],
    classifiers=[
	"Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)