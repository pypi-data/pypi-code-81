"""Tools for reading and formatting information from .python-version files."""

import json
import re
from collections import OrderedDict
from pathlib import PosixPath


class PyenvVersionFile(PosixPath):
    """A pyenv version file.

    This pyenv version file can accept tags in the form of comments like this:

        3.8.8 # future floating

    Currently accepted tags (format dependent) are:

     * future - Included in local testing but not required to pass CI
     * floating - Use a wild build version where supported
    """

    def __init__(self, file_name):
        """Initialise the version file.

        :param file_name: Path to the file to parse
        :raises FileNotFoundError: If the provided file is missing
        """
        # The path is read by the parent class in __new__ as PosixPaths are
        # immutable. So no need to pass it to the constructor.
        super().__init__()

        if not self.exists():
            raise FileNotFoundError("Expected to find version file '%s'." % file_name)

        self.tagged_versions = self._parse_version_file(file_name)

    def versions(self, exclude=None, floating=False, first=False):
        """Yield digits from the set which match the modifiers.

        :param exclude: A set of tags to exclude
        :param floating: Modify those marked "floating" to have the last digit
            replaced with "x"
        :param first: Return the first item only
        :return: A PythonVersions object
        :rtype: PythonVersions
        """

        exclude = set(exclude or [])

        versions = PythonVersions()

        for digits, tags in self.tagged_versions.items():
            if tags & exclude:
                continue

            if floating and "floating" in tags:
                digits = tuple([digits[0], digits[1], "x"])

            versions.append(digits)
            if first:
                break

        return versions

    _PYTHON_VERSION = re.compile(r"^(\d+).(\d+).(\d+)$")

    @classmethod
    def _parse_version_file(cls, file_name):
        # Add support for older versions of Python to guarantee ordering
        versions = OrderedDict()

        with open(file_name) as handle:
            for line in handle:
                comment = ""

                if "#" in line:
                    comment = line[line.index("#") + 1 :]
                    line = line[: line.index("#")]

                line = line.strip()
                if not line:
                    continue

                match = cls._PYTHON_VERSION.match(line)
                if not match:
                    raise ValueError(f"Could not parse python version: '{line}'")

                tags = set(part.strip() for part in comment.strip().split(" "))
                tags.discard("")  # Drop anything caused by repeated spaces

                digits = tuple(int(digit) for digit in match.groups())
                versions[digits] = tags

        return versions


class PythonVersions(list):
    """A list which supports getting python versions in multiple styles.

    Supported styles are:

        `plain`: e.g. 3.8.8 3.9.2

        `json`: e.g. ["3.6.12", "3.8.8", "3.9.2"]
            This is valid JSON and can be included in scripts.

        `tox`: e.g. py27,py36,py37
            Which can be used in comprehensions like this:
            tox -e {py27,py36}-tests

        `classifier`: e.g. Programming Language :: Python :: 3.9

    For all methods which accept style

    :raises ValueError: For an unrecognised style
    """

    def format(self, style):
        """Get the python versions as a list in a variety of styles.

        :param style: One of the styles above
        :return: A generator of values in the chosen format
        :rtype: str
        """
        return (self._format(value, style) for value in self)

    def as_string(self, style):
        """Get the python versions as a string in a variety of styles.

        :param style: One of the styles above
        :return: A string representing all of the versions

        :raises ValueError: For an unrecognised style
        """

        if style == "classifier":
            # Classifiers should be sorted by version descending
            sorted_versions = PythonVersions(self.copy())
            sorted_versions.sort(reverse=True)

            return "".join(sorted_versions.format(style))

        values = self.format(style)

        if style == "plain":
            return " ".join(values)

        if style == "tox":
            return ",".join(values)

        if style == "json":
            return json.dumps(list(values))

        raise ValueError("Unsupported style '%s'" % style)

    @classmethod
    def _format(cls, digits, style):
        if style in ("plain", "json"):
            return f"{digits[0]}.{digits[1]}.{digits[2]}"

        if style == "tox":
            return f"py{digits[0]}{digits[1]}"

        if style == "classifier":
            return f"    Programming Language :: Python :: {digits[0]}.{digits[1]}\n"

        raise ValueError("Unsupported style '%s'" % style)
