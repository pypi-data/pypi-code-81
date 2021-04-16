# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['simplematch']
setup_kwargs = {
    'name': 'simplematch',
    'version': '1.1',
    'description': 'Minimal, super readable string pattern matching.',
    'long_description': '<img width="500" src="https://raw.githubusercontent.com/tfeldmann/simplematch/main/docs/simplematch.svg" alt="logo">\n\n# simplematch\n\n> Minimal, super readable string pattern matching for python.\n\n[![PyPI Version][pypi-image]][pypi-url]\n[![tests](https://github.com/tfeldmann/simplematch/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/tfeldmann/simplematch/actions/workflows/tests.yml)\n\n```python\nimport simplematch\n\nsimplematch.match("He* {planet}!", "Hello World!")\n>>> {"planet": "World"}\n\nsimplematch.match("It* {temp:float}°C *", "It\'s -10.2°C outside!")\n>>> {"temp": -10.2}\n```\n\n## Installation\n\n`pip install simplematch`\n\n## Syntax\n\n`simplematch` has only two syntax elements:\n\n- wildcard `*`\n- capture group `{name}`\n\nCapture groups can be named (`{name}`), unnamed (`{}`) and typed (`{name:float}`).\n\nThe following types are available:\n\n- `int`\n- `float`\n- `email`\n- `url`\n- `ipv4`\n- `ipv6`\n- `bitcoin`\n- `ssn` (social security number)\n- `ccard` (matches Visa, MasterCard, American Express, Diners Club, Discover, JCB)\n\nFor now, only named capture groups can be typed.\n\nThen use one of these functions:\n\n```python\nimport simplematch\n\nsimplematch.match(pattern, string) # -> returns a dict\nsimplematch.test(pattern, string)  # -> return True / False\n```\n\nOr use a `Matcher` object:\n\n```python\nimport simplematch as sm\n\nmatcher = sm.Matcher(pattern)\n\nmatcher.match(string) # -> returns a dict\nmatcher.test(string)  # -> returns True / False\nmatcher.regex         # -> shows the generated regex\n```\n\n## Basic usage\n\n```python\nimport simplematch as sm\n\n# extracting data\nsm.match(\n    pattern="Invoice_*_{year}_{month}_{day}.pdf",\n    string="Invoice_RE2321_2021_01_15.pdf")\n>>> {"year": "2021", "month": "01", "day": "15"}\n\n# test match only\nsm.test("ABC-{value:int}", "ABC-13")\n>>> True\n```\n\n## Type hints\n\n```python\nimport simplematch as sm\n\nmatcher = sm.Matcher("{year:int}-{month:int}: {value:float}")\n\n# extracting data\nmatcher.match("2021-01: -12.786")\n>>> {"year": 2021, "month": 1, "value": -12.786}\n\n# month is no integer, no match\nmatcher.match("2021-AB: Hello")\n>>> {}\n\n# no extraction, only test for match\nmatcher.test("1234-01: 123.123")\n>>> True\n\n# show generated regular expression\nmatcher.regex\n>>> \'^(?P<year>[+-]?[0-9]+)\\\\-(?P<month>[+-]?[0-9]+):\\\\ (?P<value>[+-]?(?:[0-9]*[.])?[0-9]+)$\'\n```\n\n## Background\n\n`simplematch` aims to fill a gap between parsing with `str.split()` and regular\nexpressions. It should be as simple as possible, fast and stable.\n\nThe `simplematch` syntax is transpiled to regular expressions under the hood, so\nmatching performance should be just as good.\n\nI hope you get some good use out of this!\n\n## Contributions\n\nContributions are welcome! Just submit a PR and maybe get in touch with me via email\nbefore big changes.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n<!-- Badges -->\n\n[pypi-image]: https://img.shields.io/pypi/v/simplematch\n[pypi-url]: https://pypi.org/project/simplematch/\n',
    'author': 'Thomas Feldmann',
    'author_email': 'mail@tfeldmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tfeldmann/simplematch',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
