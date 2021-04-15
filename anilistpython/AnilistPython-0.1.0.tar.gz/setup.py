from setuptools import setup, find_packages
import codecs
import os
import pathlib

VERSION = '0.1.0'
DESCRIPTION = 'Anilist Python module that allows you to search up and retrieve anime/manga/characters/etc info. (No login required)'
LONG_DESCRIPTION = "Anilist Python library that allows you to easily search up and retrieve anime, manga, animation studio, and character \
                    information. This library is both beginner-friendly and offers the freedom for more experienced developers to interact \
                    with the retrieved information. The code base can be found at \
                    https://github.com/ReZeroE/AnilistPython"


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Setting up
setup(
    name="AnilistPython",
    version=VERSION,
    author="Kevin L. (ReZeroK)",
    author_email="kevinliu@vt.edu",
    license_files = "LICENSE.txt",
    license="MIT Licence (MIT)",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ReZeroE/AnilistPython",
    packages=find_packages(),
    install_requires=['requests', 'pytest'],
    keywords=['python', 'anime', 'anilist', 'manga', 'characters', 'alpha testing', 'Milim', 'ReZeroK'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)