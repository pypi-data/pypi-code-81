from setuptools import setup, find_packages
from os.path import abspath, dirname, join
import io
import re

with io.open("thanetwffapi/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

# Fetches the content from README.md
# This will be used for the "long_description" field.
README_MD = open(join(dirname(abspath(__file__)), "README.md")).read()

setup(
    # Name of your project, what users will type when they install package.
    # pip install thanetwffapi
    # This field is REQUIRED
    name="thanetwffapi",

    # Version of project, in the form of: major.minor.patch
    # eg: 1.0.0, 1.0.1, 3.0.2, 5.0-beta, etc.
    # CANNOT upload two versions of package with the same version number
    # This field is REQUIRED
    #version="0.0.1",
    version=version,

    # To include data files to the package
    include_package_data=True,

    # The packages that constitute the project.
    # Write name of package, or use setuptools.findpackages()
    # If one file, instead of a package, use the py_modules field instead.
    # EITHER py_modules OR packages should be present.
    packages=find_packages(exclude="tests"),

    # The description that will be shown on PyPI.
    # Keep it short and concise
    # This field is OPTIONAL
    description="API for Thanet offshore wind farm foundation data",

    # The content that will be shown on project page.
    # E.g. Displaying README.md file
    # This field is OPTIONAL
    long_description=README_MD,

    # Tell PyPI what language README file is in.
    # This field is OPTIONAL
    long_description_content_type="text/markdown",

    # The url field should contain a link to a git repository, the project's website
    # or the project's documentation.
    # This field is OPTIONAL
    # url="https://github.com/Sagmo/thanet-wff-api",

    # The author name and email fields are self explanatory.
    # These fields are OPTIONAL
    # author_name="Sagmo",
    # author_email="sivert.sag@gmail.com",

    # Classifiers help categorize project.
    # For a complete list of classifiers, visit:
    # https://pypi.org/classifiers
    # This is OPTIONAL
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],

    # Keywords are tags that identify your project and help searching for it
    # This field is OPTIONAL
    #keywords="API, ",

    # For additional fields, check:
    # https://github.com/pypa/sampleproject/blob/master/setup.py
)
