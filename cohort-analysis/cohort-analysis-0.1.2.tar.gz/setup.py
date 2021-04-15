import os
from os import path
from re import match
from setuptools import setup

MODULE_NAME = "cohort-analysis"
PACKAGE_NAME = "cohort_analysis"

def format_requirement(requirement_string):
    """
    Format a [packages] line from the Pipfile as needed for the
    install requires list
    """
    # remove the first "=" sign:
    pkg_name = requirement_string.split("=")[0]
    version_info = "=".join(requirement_string.split("=")[1:])

    rs = pkg_name + version_info
    rs = "".join(rs.split('"')) # remove quotation marks
    rs = "".join(rs.split(" ")) # strip out whitespace

    return rs

def get_requirements():
    """
    Read [packages] from the Pipfile and convert to a requirements list
    """

    with open("Pipfile") as pipfile:
        pip_contents = pipfile.read()

    requirements_body = pip_contents.split("[packages]")[-1]
    requirements = [x for x in requirements_body.split("\n") if len(x) > 0]

    return [format_requirement(req) for req in requirements]

def get_version():
    """
    Returns the version of the package. 

    If the commit is SemVer tagged,(and hence is being uploaded to PyPI) 
    then returns the value of the CI_COMMIT_TAG. 

    If the commit is not SemVer tagged, (and hence is being uploaded to 
    TestPyPI) then returns the GitLab CI_JOB_ID.
    """

    tag = os.environ.get("CI_COMMIT_TAG", "missing")

    semver = "^v\d+\.\d+\.\d+$"

    is_semver = match(semver, tag) is not None

    if is_semver:
        return tag  # return tag as package version

    test_pkg_version = os.environ['CI_JOB_ID']

    return test_pkg_version

def get_download_url(module_name, package_name):
    """
    Returns the download URL with the correct version
    """
    return "https://github.com/apolitical/{m}/archive/v{v}.tar.gz".format(
        m = module_name,
        v = get_version()
    )

def get_long_description_from_README():
    """
    Returns the contents of README.md as a character string
    """

    with open("README.md") as file_object:
        long_description = file_object.read()
    return long_description

setup(
    name = MODULE_NAME,
    version = get_version(),
    author = "PaddyAlton",
    author_email = "paddy.alton@apolitical.co",
    license = "MIT",
    install_requires = get_requirements(),
    download_url = get_download_url(MODULE_NAME, PACKAGE_NAME),
    packages = [PACKAGE_NAME],
    description = "A package for calculating cohort metrics from an activity stream and cohorts data table.",
    long_description = get_long_description_from_README(),
    long_description_content_type="text/markdown",
    keywords = ["cohort", "activity", "retention"],
    classifiers=[
    'Development Status :: 2 - Pre-Alpha', 
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)

# TO DO: 
# - mirror to github so download_url works
# - update development status as necessary
