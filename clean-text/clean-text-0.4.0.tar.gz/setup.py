# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleantext']

package_data = \
{'': ['*']}

install_requires = \
['emoji', 'ftfy>=6.0,<7.0']

extras_require = \
{'gpl': ['unidecode>=1.1.1,<2.0.0']}

setup_kwargs = {
    'name': 'clean-text',
    'version': '0.4.0',
    'description': 'Functions to preprocess and normalize text.',
    'long_description': '# `clean-text` [![Build Status](https://travis-ci.com/jfilter/clean-text.svg?branch=master)](https://travis-ci.com/jfilter/clean-text) [![PyPI](https://img.shields.io/pypi/v/clean-text.svg)](https://pypi.org/project/clean-text/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clean-text.svg)](https://pypi.org/project/clean-text/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/clean-text)](https://pypistats.org/packages/clean-text)\n\nUser-generated content on the Web and in social media is often dirty. Preprocess your scraped data with `clean-text` to create a normalized text representation. For instance, turn this corrupted input:\n\n```txt\nA bunch of \\\\u2018new\\\\u2019 references, including [Moana](https://en.wikipedia.org/wiki/Moana_%282016_film%29).\n\n\n»Yóù àré     rïght &lt;3!«\n```\n\ninto this clean output:\n\n```txt\nA bunch of \'new\' references, including [moana](<URL>).\n\n"you are right <3!"\n```\n\n`clean-text` uses [ftfy](https://github.com/LuminosoInsight/python-ftfy), [unidecode](https://github.com/takluyver/Unidecode) and numerous hand-crafted rules, i.e., RegEx.\n\n## Installation\n\nTo install the GPL-licensed package [unidecode](https://github.com/takluyver/Unidecode) alongside:\n\n```bash\npip install clean-text[gpl]\n```\n\nYou may want to abstain from GPL:\n\n```bash\npip install clean-text\n```\n\nNB: This package is named `clean-text` and not `cleantext`.\n\nIf [unidecode](https://github.com/takluyver/Unidecode) is not available, `clean-text` will resort to Python\'s [unicodedata.normalize](https://docs.python.org/3.7/library/unicodedata.html#unicodedata.normalize) for [transliteration](https://en.wikipedia.org/wiki/Transliteration).\nTransliteration to closest ASCII symbols involes manually mappings, i.e., `ê` to `e`.\n`unidecode`\'s mapping is superiour but unicodedata\'s are sufficent.\nHowever, you may want to disable this feature altogether depending on your data and use case.\n\nTo make it clear: There are **inconsistencies** between processing text with or without `unidecode`.\n\n## Usage\n\n```python\nfrom cleantext import clean\n\nclean("some input",\n    fix_unicode=True,               # fix various unicode errors\n    to_ascii=True,                  # transliterate to closest ASCII representation\n    lower=True,                     # lowercase text\n    no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them\n    no_urls=False,                  # replace all URLs with a special token\n    no_emails=False,                # replace all email addresses with a special token\n    no_phone_numbers=False,         # replace all phone numbers with a special token\n    no_numbers=False,               # replace all numbers with a special token\n    no_digits=False,                # replace all digits with a special token\n    no_currency_symbols=False,      # replace all currency symbols with a special token\n    no_punct=False,                 # remove punctuations\n    replace_with_punct="",          # instead of removing punctuations you may replace them\n    replace_with_url="<URL>",\n    replace_with_email="<EMAIL>",\n    replace_with_phone_number="<PHONE>",\n    replace_with_number="<NUMBER>",\n    replace_with_digit="0",\n    replace_with_currency_symbol="<CUR>",\n    lang="en"                       # set to \'de\' for German special handling\n)\n```\n\nCarefully choose the arguments that fit your task. The default parameters are listed above.\n\nYou may also only use specific functions for cleaning. For this, take a look at the [source code](https://github.com/jfilter/clean-text/blob/master/cleantext/clean.py).\n\nSo far, only English and German are fully supported. It should work for the majority of western languages. If you need some special handling for your language, feel free to contribute. 🙃\n\n## Development\n\n[Install and use poetry](https://python-poetry.org/).\n\n## Contributing\n\nIf you have a **question**, found a **bug** or want to propose a new **feature**, have a look at the [issues page](https://github.com/jfilter/clean-text/issues).\n\n**Pull requests** are especially welcomed when they fix bugs or improve the code quality.\n\nIf you don\'t like the output of `clean-text`, consider adding a [test](https://github.com/jfilter/clean-text/tree/master/tests) with your specific input and desired output.\n\n## Related Work\n\n-   https://github.com/pudo/normality\n-   https://github.com/davidmogar/cucco\n-   https://github.com/lyeoni/prenlp\n-   https://github.com/chartbeat-labs/textacy\n-   https://github.com/jbesomi/texthero\n-   https://github.com/s/preprocessor\n-   https://github.com/facebookresearch/cc_net\n-   https://github.com/cbaziotis/ekphrasis\n\n## Acknowledgements\n\nBuilt upon the work by [Burton DeWilde](https://github.com/bdewilde) for [Textacy](https://github.com/chartbeat-labs/textacy).\n\n## License\n\nApache\n\n## Sponsoring\n\nThis work was created as part of a [project](https://github.com/jfilter/ptf-kommentare) that was funded by the German [Federal Ministry of Education and Research](https://www.bmbf.de/en/index.html).\n\n<img src="./bmbf_funded.svg">\n',
    'author': 'Johannes Filter',
    'author_email': 'hi@jfilter.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
