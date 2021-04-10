from setuptools import setup
from pathlib import Path

def get_version():
    with (Path('.')/'VERSION').open() as fp:
        return fp.read()

def get_long_description():
    with (Path('.')/'README.md').open() as fp:
        return fp.read()

setup(
    name="tzc",
    description="copies input to output, converting timezone in any lines beginning with an ISO-8601 timestamp",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Matt Krueger",
    url="https://github.com/rstms/tzc",
    project_urls={
        "Issues": "https://github.com/rstms/tzc/issues",
        "CI": "https://github.com/rstms/tzc/actions",
        "Changelog": "https://github.com/rstms/tzc/releases",
    },
    license="MIT License",
    version=get_version(),
    packages=["tzc"],
    entry_points="""
        [console_scripts]
        tzc=tzc.main:cli
    """,
    install_requires=["click", "arrow"],
    extras_require={
        "test": ["pytest", 'pytest-datadir']
    },
    tests_require=["tzc[test]"],
    python_requires=">=3.6",
)
