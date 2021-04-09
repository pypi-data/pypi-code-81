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
exec(read("gadalang_lang/__version__.py"), pkg_info)


setup(
    name="gadalang_lang",
    version=pkg_info["__version__"],
    author=pkg_info["__author__"],
    author_email=pkg_info["__author_email__"],
    url=pkg_info["__url__"],
    project_urls={
        "Bug Tracker": "https://github.com/gadalang/gadalang-lang/issues",
        "Source Code": "https://github.com/gadalang/gadalang-lang/",
    },
    description="Collection of lang nodes for gada",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    package_data={"gadalang_lang": ["config.yml"]},
    entry_points={
        "gadalang.nodes": [
            "lang = gadalang_lang._plugin",
        ]
    },
    zip_safe=False,
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
