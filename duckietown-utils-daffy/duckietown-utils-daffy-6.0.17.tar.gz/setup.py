from setuptools import find_packages, setup

line = "daffy"
package_name = f"duckietown-utils-{line}"
library_webpage = "http://github.com/duckietown/duckietown-utils"
maintainer = "Mack"
maintainer_email = "admin@duckietown.org"
short_description = "Miscellaneous utilities"
full_description = """
Miscellaneous utilities
"""


# Read version from the __init__ file
def get_version_from_source(filename):
    import ast

    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith("__version__"):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError("No version found in %r." % filename)
    if version is None:
        raise ValueError(filename)
    return version


version = get_version_from_source("src/duckietown_code_utils/__init__.py")

install_requires = [
    "PyGeometry-z6",
    "opencv-python",
    "comptests-z6",
    "ruamel.yaml",
]
tests_require = []

# compile description
underline = "=" * (len(package_name) + len(short_description) + 2)
description = """
{name}: {short}
{underline}

{long}
""".format(
    name=package_name,
    short=short_description,
    long=full_description,
    underline=underline,
)

console_scripts = [
    # "dt-pc-demo = duckietown_pondcleaner:dt_pc_demo",
]
# setup package
setup(
    name=package_name,
    author=maintainer,
    author_email=maintainer_email,
    url=library_webpage,
    tests_require=tests_require,
    install_requires=install_requires,
    package_dir={"": "src"},
    packages=find_packages("./src"),
    long_description=description,
    version=version,
    entry_points={"console_scripts": console_scripts},
)
