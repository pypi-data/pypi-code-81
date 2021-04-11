import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().split("\n")


setup(
    name="clsp",
    description="CLSP short for Command Line Selection Prompt, is a minimalistic and fast to navigate single choice interface.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Taguar258",
    license="MIT",
    version="1.2",
    keywords=["python", "cli", "console", "terminal", "input", "prompt", "tty", "ncurses", "curses"],
    url="https://github.com/Taguar258/clsp",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements("requirements.txt"),
    classifiers=["License :: OSI Approved :: MIT License",
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Software Development :: User Interfaces',
                 'Topic :: Terminals'],
)
