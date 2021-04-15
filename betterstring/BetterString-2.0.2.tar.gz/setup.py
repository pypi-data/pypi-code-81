from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="BetterString",
    version="2.0.2",
    # Major version 2
    # Minor version 0
    # Maintenance version 1

    author="DerSchinken (aka DrBumm)",
    description="Like a normal string but with more functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
