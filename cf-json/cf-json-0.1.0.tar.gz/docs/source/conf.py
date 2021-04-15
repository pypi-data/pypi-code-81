# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sphinx_rtd_theme

import os
import sys
import re
import datetime


# -- Path setup information -----------------------------------------------------

def get_project_root():
    source_folder = os.path.dirname(__file__)
    doc_folder = os.path.dirname(source_folder)
    return os.path.dirname(doc_folder)


def add_source_to_path():
    project_root = get_project_root()
    src = project_root + '/src'
    sys.path.insert(0, os.path.abspath(src))


def get_version_file():
    project_root = get_project_root()
    src = project_root + '/src'
    init_file = src + '/cfjson/__init__.py'
    return init_file


def get_version():
    """Pull the version out of the module."""
    init_file = get_version_file()
    REGEX = r"^__version__ = ['\"]([^'\"]*)['\"]"
    with open(init_file, 'r') as fh:
        for line in fh.readlines():
            if line.startswith('__version__'):
                mo = re.search(REGEX, line, re.M)
                if mo:
                    print(mo.group(1))
                    return str(mo.group(1))
                else:
                    raise RuntimeError("Unable to find version string in %s." % (init_file,))
    raise RuntimeError("Unable to find version.")


add_source_to_path()

# -- Project information -----------------------------------------------------

project = 'cf-json'
author = 'Keir Rice'
copyright = f'{datetime.datetime.now().date().year}, {author}'

# The full version, including alpha/beta/rc tags
release = get_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	"sphinx.ext.intersphinx",
	"sphinx.ext.autodoc",
	'sphinx.ext.autosummary',  # Create neat summary tables
	"sphinx.ext.mathjax",
	"sphinx.ext.viewcode",
	'sphinx_tabs.tabs',
	'sphinx_copybutton',
	'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

intersphinx_mapping = {
  'python': ('https://docs.python.org/3', None),
  }

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: |C:\\> "
copybutton_prompt_is_regexp = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_path = ["_themes", ]

html_theme_options = {
    'style_external_links': False,
    'footer_logo': 'clayfox-sig.png',
    'footer_logo_link': 'https://www.clayfox.co.nz',
    # 'style_nav_header_background': '#b97c29',  # TODO: Need to update the search border as well
    'vcs_pageview_mode': 'blob',
	'collapse_navigation': False,
	'theme_index_in_nav': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_js_files = [
    'js/custom.js'
]