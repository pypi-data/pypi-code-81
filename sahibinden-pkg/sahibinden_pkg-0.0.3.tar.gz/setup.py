from setuptools import setup

setup(
    name='sahibinden_pkg',
    version='0.0.3',
    packages=['sahibinden'],
    url='',
    license='MIT',
    author='Servet Guney',
    author_email='servetguney@gmail.com',
    description='Non-Profit Data Processing of Sahibinden',
    install_requires=[
        "setuptools>=42",
        "requests",
        "beautifulsoup4",
        "statistics",
        "soupsieve",
        "lxml",
        "wheel"
    ]
)
