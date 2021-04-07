import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="boastlabs-cloud-functions",
    version="1.0.1",
    description="Boastlabs cloud function template",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/musatdragosro/boastlabs-cloud-functions",
    author="Musat Dragos",
    author_email="musat.dragos.ro@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["firebase-admin", "semantic_version"],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)
