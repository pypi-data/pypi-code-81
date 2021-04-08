import pathlib
import pkg_resources

import setuptools


with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setuptools.setup(
    name="simplejwt_session",
    version="0.0.4",
    author="Ali Akhtari",
    author_email="hi@aliakh.me",
    description="Generates an authenticated requests `Session` into a Django API authenticated w/ `django-rest-framework-simplejwt`",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akhtariali/agron_session",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires='>=3.7',
)
