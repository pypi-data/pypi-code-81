from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="BetterString",
    version="2.0.0",
    # Major version 1
    # Minor version 0
    # Maintenance version 1

    author="DerSchinken (aka DrBumm)",
    description="Like a normal string but with more functionality",
    long_description=long_description,
    packages=find_packages(),
)
