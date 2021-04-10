import pathlib
from setuptools import find_packages, setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="spell-checker",
    version="1.6.0",
    description="Python 3+ spell checker, supports English, German, Italian, Spanish, and French!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Harvard90873/data_structures",
    author="Harvard90873",
    author_email="harvard90873@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests", "build")),
    include_package_data=True,
    package_data={
      'speller3x': ['data/*.txt'],
    },
    install_requires=["python-algorithms-3x", "termcolor", "data-structures3x", "and-or-not"],
)
