from setuptools import setup, find_packages
import sys

PYTHON_VERSION = sys.version_info[:2]
if PYTHON_VERSION < (3, 7):
    print("Python version must be greater than or equal to 3.7")
    sys.exit()

try:
    LONG_DESCRIPTION = open("README.md").read()
except:
    LONG_DESCRIPTION = ""

import fungit

setup(
    name="fungit",
    version=fungit.__version__,
    author=fungit.__author__,
    author_email=fungit.__email__,
    description="Simple terminal tool of Git.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/zlj-zz/fungit.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    entry_points="""
        [console_scripts]
        fungit=fungit.main:main
        g=fungit.terminal_git.main:g
    """,
    python_requires=">=3.7",
)
