import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
name="color-detect"
version="0.0.1"
author="Korede Bashir"
author_email="bashirkorede@gmail.com"
description="A mini package to work with detecting colors from images"
long_description=(HERE / "README.md").read_text()
long_description_content_type="text/markdown"
url="https://github.com/bashirk/color-detect"
license="MIT"
INSTALL_REQUIRES = [
      'opencv-python',
      'numpy',
      'pandas'
]

'''
with open("README.md", "r") as f:
    long_description = f.read()
'''


setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=url,
    license=license,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
