import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="strictly-metric",
    version="1.0.13",
    description="Custom Metric Created for the NBA by Strictly By The Numbers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Strictly-by-the-Numbers/player_metric",
    author="Strictly By The Numbers",
    author_email="jayce@strictlybythenumbers.com",
    license="Strictly By The Numbers",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["pandas", "numpy"],
)