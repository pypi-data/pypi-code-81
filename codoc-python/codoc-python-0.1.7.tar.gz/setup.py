from setuptools import setup, find_packages

try:
    with open("../README.md") as f:
        readme = f.read()
except FileNotFoundError:
    # If run by docs, it will not use the correct path
    with open("README.md") as f:
        readme = f.read()

setup(
    name="codoc-python",
    version="0.1.7",
    author="Casper Weiss Bang",
    author_email="casper@svadilfare.dev",
    description="Tool for generating architectural views for the codoc system",
    long_description_content_type="text/markdown",
    long_description=readme,
    url="https://codoc.org/",
    packages=find_packages(),
    install_requires=["requests==2.25.1", "fire==0.4.0", "sentry-sdk==1.0.0"],
    python_requires="!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
    ],
    entry_points={
        # Install a script as "codocpy"
        "console_scripts": [
            "codocpy = codoc.entrypoints.cli:_main",
        ],
    },
)
