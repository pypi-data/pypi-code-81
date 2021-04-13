import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="fastrlapi",
    version="0.0.1",
    description="reinforcement learning high-level API.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Rohit Gangupantulu",
    author_email="rgangupantulu@deloitte.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["fastrlapi", "fastrlapi.callbacks", "fastrlapi.backends"],
    install_requires=[
        "tensorflow==2.0.1",
        "tensorflow-probability==0.8.0",
        "tf-agents==0.3.0",
        "tensorforce==0.5.3",
        "gym==0.15.4",
        "imageio==2.6.1",
        "imageio-ffmpeg==0.3.0",
        "matplotlib==3.1.2"
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "drlapi=drlapi.__main__:main",
        ]
    },
)
