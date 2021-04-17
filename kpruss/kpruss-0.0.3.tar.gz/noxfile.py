import configparser
import keyring
import os
import pathlib
import re
import shutil

import nox

parser = configparser.ConfigParser(empty_lines_in_values=True)
parser.read(pathlib.Path(__file__).parent / "setup.cfg")

# Grab the supported Pythons
pythons = [v.split(":")[-1].strip()
           for v in parser.get("metadata",
                               "classifiers",
                               fallback="").splitlines()
           if re.search(r"Python\s*::\s*\d+[.]\d+\s*$", v)]

# Grab the dependencies
dependencies = [d for d in parser.get("options",
                                      "install_requires",
                                      fallback="").splitlines()
                if d]

# Set the default sessions
nox.options.sessions = [
    "flake8",
    *["check-" + v for v in pythons],
    "docs"
]


@nox.session
def flake8(session):
    """Run flake 8 on any sources"""
    session.install("flake8")
    session.run("flake8", "kpruss", "noxfile.py", "doc")


@nox.session(python=pythons)
def check(session):
    """Check installing and building works"""
    if dependencies:
        session.install(*dependencies)

    session.install(".")
    build = pathlib.Path(session.bin).parent / "html"
    session.run("sphinx-build",
                "-b", "html",
                "-W",  # Warnings are errors
                str(pathlib.Path(__file__).parent / "doc"),
                str(build.resolve()),
                )


@nox.session
def docs(session):
    """Build the documentation"""
    if dependencies:
        session.install(*dependencies)

    session.install(".")
    root = pathlib.Path(__file__).parent.resolve()
    session.run("sphinx-build",
                "-b", "html",
                "-W",  # Warnings are errors
                str(root / "doc"),
                str(root / "docs"),
                )


@nox.session
def dist(session):
    """Build the distribution"""
    session.install("build", "twine")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    session.run("python", "-m", "build")
    session.run(
        "python", "-m", "twine", "check", os.path.join("dist", "*")
    )
    session.run(
        "python", "-m", "twine", "upload", "--user", "__token__",
        "--password", keyring.get_password("kpruss", "kprussing"),
        os.path.join("dist", "*")
    )
