#!/usr/bin/env python
from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="pwbus-http",
    version="0.1.13",
    author="Fabio Szostak",
    author_email="fszostak@gmail.com",
    description="HTTP Server for PWBUS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fszostak/pwbus-http",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    entry_points={
        'console_scripts': ['pwbus_http=pwbus_http.server:main'],
    },
    install_requires=requirements,
    setup_requires=['flake8'],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
