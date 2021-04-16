from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="idf_updater",
    version="1.0.0",
    description="A library for updating IDF files to newer versions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ralph Evins",
    author_email="revins@uvic.ca",
    url="https://gitlab.com/energyincities/idf_updater",
    packages=["idf_updater"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    extras_require={},
)
