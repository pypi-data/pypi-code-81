from setuptools import setup


def get_version(filename):
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


install_requires = [
    "scipy",
    "PyGeometry-z6",
    "PyYAML",
    "matplotlib",
]

module = "gokartpy"
package = "gokartpy"
src = "src"

version = get_version(filename=f"src/{module}/__init__.py")

setup(
    name=package,
    package_dir={"": src},
    packages=[module],
    version=version,
    author="Alessandro Zanardi",
    author_email="azanardi@ethz.ch",
    url="https://github.com/idsc-frazzoli/gokart-gokartpy",
    zip_safe=False,
    install_requires=install_requires,
)
