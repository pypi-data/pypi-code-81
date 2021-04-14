import os

from setuptools import find_packages, setup

the_lib_folder = os.path.dirname(os.path.realpath(__file__))
requirementPath = the_lib_folder + "/requirements.txt"

install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md") as f:
    readme = f.read()

version_contents = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "paretos", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)
VERSION = version_contents["VERSION"]

setup(
    name="paretos",
    version=VERSION,
    description="Package to get started optimizing",
    python_requires=">=3.7",
    author="Paretos",
    author_email="support@paretos.ai",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    packages=find_packages(exclude=("test", "test.*", "scripts", "scripts.*")),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
