from setuptools import setup
from rawautoparams import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rawautoparams",
    version=__version__,
    author="Jan Zelenka",
    author_email="3yanyanyan@gmail.com",
    description="Thermo/Finnigan .raw file format parameters reader",
    long_description=long_description,
    url="https://gitlab.science.ru.nl/jzelenka/rawautoparams",
    packages=['rawautoparams'],
    license="",
    platforms=["OS Independent"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        ],
    install_requires=['numpy',
                      'rawprasslib']
    )
