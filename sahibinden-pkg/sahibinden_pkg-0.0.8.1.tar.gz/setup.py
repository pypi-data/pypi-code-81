from setuptools import setup

setup(
    name = 'sahibinden_pkg',
    version = '0.0.8.1',
    packages = ['sahibinden'],
    url = 'https://pypi.org/project/sahibinden-pkg/',
    license = 'MIT',
    author = 'Servet Guney',
    author_email='servetguney@gmail.com',
    description = 'Sample Data Processing of Sahibinden',
    long_description = " In this package, it is being used for sample processing of "
                      "sahibinden.com live data for different categories.",
    install_requires = [
        "setuptools>=42",
        "requests",
        "beautifulsoup4",
        "statistics",
        "soupsieve",
        "lxml",
        "wheel",
        "numpy"
    ]
)
