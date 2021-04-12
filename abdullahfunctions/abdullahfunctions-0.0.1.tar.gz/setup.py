from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='abdullahfunctions',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An example python package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    author='Abdullah Tatlisumak',
    author_email='matatlisumak@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
