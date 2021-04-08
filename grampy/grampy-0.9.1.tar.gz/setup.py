from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="grampy", # Replace with your own username
    version="0.9.1",
    author="Alex G",
    author_email="alex.g@gmail.com",
    description="A small package to work with prime numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clement-bonnet/medium-first-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)