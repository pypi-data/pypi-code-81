import io
from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


def read(*filenames, **kwargs):
    """ Read contents of multiple files and join them together """
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


pkg_info = {}
exec(read("gada_pyrunner/__version__.py"), pkg_info)


setup(
    name="gada-pyrunner",
    version=pkg_info["__version__"],
    author=pkg_info["__author__"],
    author_email=pkg_info["__author_email__"],
    url=pkg_info["__url__"],
    project_urls={
        "Bug Tracker": "https://github.com/gadalang/gada-pyrunner/issues",
        "Source Code": "https://github.com/gadalang/gada-pyrunner/",
    },
    description="Python runner for gada",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    install_requires=["gada"],
    entry_points={
        "gada.runners": [
            "pymodule = gada_pyrunner.pymodule",
            "python = gada_pyrunner.python",
        ]
    },
    include_package_data=True,
    zip_safe=True,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
