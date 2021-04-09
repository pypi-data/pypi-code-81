# This file is part of Flatplan.
#
# Flatplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flatplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flatplan.  If not, see <https://www.gnu.org/licenses/>.

# Default encoding used to read or write files

from setuptools import setup, find_packages
from pathlib import Path


here = Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="flatplan",
    version="1.2.1",
    description="Flatplan is a tool that groups all resources and providers specified in a Terraform plan or state file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egonbraun/python-project-template",
    author="Egon Braun",
    author_email="egon@mundoalem.io",
    keywords="terraform, plan, state, tools, cli",
    packages=find_packages(where=".", exclude=("docs", "tests")),
    package_dir={"flatplan": "flatplan"},
    python_requires=">=3.7, <4",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=[
        "colorama",
        "coloredlogs",
        "fire",
    ],
    extras_require={
        "dev": ["black", "coverage", "pytest", "sphinx", "tox", "twine"],
    },
    package_data={},
    data_files=[],
    entry_points={
        "console_scripts": [
            "flatplan=flatplan:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/egonbraun/flatplan/issues",
        "Source": "https://github.com/egonbraun/flatplan",
    },
)
