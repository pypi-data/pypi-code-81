import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="zkan",
    version="1.0.0",
    description="Kan's Business Card",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zkan/py-business-card",
    author="Kan Ouivirach",
    author_email="zkan.cs@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["zkan"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "zkan=zkan.__main__:main",
        ]
    },
)
