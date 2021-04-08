"""Tools for reading and formatting information from .python-version files."""

import json
import os
import re
from collections import OrderedDict


class PyenvVersionFile:
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
        if not os.path.isfile(file_name):
            raise FileNotFoundError("Expected to find version file '%s'." % file_name)

        self.file_name = file_name
        self.versions = self._parse_version_file(self.file_name)

    def filter_versions(self, exclude=None, floating=False, first=False):
        """Yield digits from the set which match the modifiers.

        :param exclude: A set of tags to exclude
        :param floating: Modify those marked "floating" to have the last digit
            replaced with "x"
        :param first: Return the first item only
        :return: Generator of digit tuples
        :rtype: tuple
        """

        exclude = set(exclude or [])

        for digits, tags in self.versions.items():
            if tags & exclude:
                continue

            if floating and "floating" in tags:
                digits = tuple([digits[0], digits[1], "x"])

            yield digits
            if first:
                return

    def format(self, style, exclude=None, floating=False, first=False):
        """Get the python versions in a variety of styles.

        `plain`: e.g. 3.8.8 3.9.2

        `json`: e.g. ["3.6.12", "3.8.8", "3.9.2"]
            This is valid JSON and can be included in scripts.

        `tox`: e.g. py27,py36,py37
            Which can be used in comprehensions like this:
            tox -e {py27,py36}-tests

        `classifier`: e.g. Programming Language :: Python :: 3.9

        :param style: One of the styles above
        :param exclude: A set of tags to exclude
        :param floating: Modify those marked "floating" to have the last digit
            replaced with "x"
        :param first: Return the first item only
        :return: A string in the chosen format

        :raises ValueError: If a value in the file cannot be parsed
        """

        raw_digits = list(self.filter_versions(exclude, floating, first))

        if style == "plain":
            return " ".join(".".join(digits) for digits in raw_digits)

        if style == "tox":
            return ",".join("py" + "".join(digits[:2]) for digits in raw_digits)

        if style == "json":
            codes = []
            for digits in raw_digits:
                codes.append(".".join(digits))

            return json.dumps(codes)

        if style == "classifier":
            rows = []
            for digits in reversed(raw_digits):
                rows.append(
                    "    Programming Language :: Python :: "
                    + ".".join(digits[:2])
                    + "\n"
                )

            return "".join(rows)

        raise ValueError("Unsupported style '%s'" % style)

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

                versions[match.groups()] = tags

        return versions
