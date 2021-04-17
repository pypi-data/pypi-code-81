"""Extension for Sphinx configuration."""

# Standard library:
import sys
import typing as t
from pathlib import Path

# 3rd party:
import sphinx_rtd_theme  # type: ignore # noqa
import toml  # to read data (e. g. version) from pyproject.toml

# constants:
PROJECT_DIR: Path = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

PYPROJECT_FILE_PATH = PROJECT_DIR / "pyproject.toml"
assert (
    PYPROJECT_FILE_PATH.is_file()
), f'Cannot find pyproject.toml file at "{PYPROJECT_FILE_PATH}"!'

extensions = [
    "sphinx_rtd_theme",  # Read the Docs Sphinx Theme (see https://github.com/readthedocs/sphinx_rtd_theme) # type: ignore # noqa
    "sphinx.ext.autodoc",  # Include documentation from docstrings (see https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) # type: ignore # noqa
    "sphinx.ext.autosummary",  # Generate autodoc summaries (see https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) # type: ignore # noqa
    "sphinx.ext.coverage",  # Collect doc coverage stats (see https://www.sphinx-doc.org/en/master/usage/extensions/coverage.html) # type: ignore # noqa
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings (see https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) # type: ignore # noqa
    "sphinx.ext.todo",  # Support for todo items (see https://www.sphinx-doc.org/en/master/usage/extensions/todo.html) # type: ignore # noqa
    "sphinx.ext.viewcode",  # Add links to highlighted source code (see https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html) # type: ignore # noqa
]

pyproject_code: str = PYPROJECT_FILE_PATH.read_text()
pyproject_data: t.MutableMapping[str, t.Any] = toml.loads(pyproject_code)

author = ", ".join(pyproject_data["tool"]["poetry"]["authors"])

release = pyproject_data["tool"]["poetry"]["version"]

rst_epilog = f".. |Release| replace:: {release}"

html_theme = "sphinx_rtd_theme"


style_path: Path = PROJECT_DIR / "docs/source/_static/style.css"
if not style_path.is_file():
    style_path.write_text(".wy-nav-content {\n    max-width: none;\n}")


def setup(app):  # type: ignore
    app.add_css_file("style.css")
