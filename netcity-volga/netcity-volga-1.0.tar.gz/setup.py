from pathlib import Path
from setuptools import setup

setup(
    name="netcity-volga",
    version="1.0",
    author_email="pulsar04040@gmail.com",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/tulen34/netcity-volga",
    packages=["netcity_volga"],
    license="MIT",
    install_requires=["httpx", "pydantic"],
    python_requires=">=3.9",
)
