from setuptools import setup, find_packages
from pathlib import Path
from codecs import open
from os import path

with open(path.join(
        Path(__file__).resolve().parent, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ninja-snake-lib",
    version="0.0.1",
    description="Ninja Snake Lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carlos Sá",
    author_email="carlos.sa@getninjas.com.br",
    maintainer="Carlos Sá",
    maintainer_email="carlos.sa@getninjas.com.br",
    platforms=["Linux", "Mac OS-X", "Unix"],
    license="",
    url="https://github.com/getninjas/ninja-snake-lib",
    project_urls={
        "Bug Tracker": "https://github.com/getninjas/ninja-snake-lib/issues",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(
        where='src',
        include=['ninja_snake_lib', 'ninja_snake_lib.*'],
        exclude=['tests.py', '.env', 'settings.py', 'requirements.txt']),
    package_dir={"": "src"},
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=["django>=3"],
)
