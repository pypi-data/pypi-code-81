# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import configparser
import pathlib

# Load the details from the setup.cfg
root = pathlib.Path(__file__).parent.parent
parser = configparser.ConfigParser(empty_lines_in_values=True)
parser.read(root / "setup.cfg")

# Make sure the module has been found

# -- Project information -----------------------------------------------------

project = parser.get("build_sphinx", "project")
author = parser.get("metadata", "author")
copyright = "2021, " + author

# The full version, including alpha/beta/rc tags
release = parser.get("metadata", "version")
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.githubpages',
    'sphinx.ext.todo'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# Customizations to demonstrate this theme
html_theme = 'kpruss'
html_theme_options = {
    "author": author,
    "avatar": "https://avatars.githubusercontent.com/kprussing",
    "github": "kprussing",
    "email": "kprussing74@gmail.com",
    "linkedin": "kprussing",
    "stackoverflow": "4249913",
}

# -- Extension configuration -------------------------------------------------

todo_include_todos = True
