# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subtitlecore']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'pip>=21.0.1,<22.0.0',
 'spacy>=3.0.5,<4.0.0',
 'webvtt-py>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['subtitlecore_content = '
                     'subtitlecore.entry:get_subtitle_content',
                     'subtitlecore_parse2sens = subtitlecore.entry:parse2sens',
                     'subtitlecore_parse2text = subtitlecore.entry:parse2text']}

setup_kwargs = {
    'name': 'subtitlecore',
    'version': '0.1.10',
    'description': 'Parse srt file content into well-formed structures',
    'long_description': '# Installation from pip3\n\n```shell\npip3 install --verbose subtitlecore\npython -m spacy download en_core_web_trf\npython -m spacy download es_dep_news_trf\n```\n\n# Usage\n\nPlease refer to [api docs](https://qishe-nlp.github.io/subtitlecore/).\n\n### Excutable usage\n\n* Get subtitle content\n\n```shell\nsubtitlecore_content --srtfile test.srt --lang en\n``` \n\n* Parse srtfile into sentences with timestamp\n\n```shell\nsubtitlecore_parse2sens --srtfile test.srt --lang en\n```\n\n* Parse srtfile into plain text\n```shell\nsubtitlecore_parse2text --srtfile test.srt --lang en\n```\n\n### Package usage\n```\nfrom subtitlecore import Subtitle\n\ndef get_subtitle_content(srtfile, lang):\n  st = Subtitle(srtfile, lang)\n  for line_info in st.content:\n    print(line_info)\n\ndef parse2sens(srtfile, lang):\n  st = Subtitle(srtfile, lang)\n  content_sens = st.sentenize()\n  for e in content_sens:\n    print(e)\n\ndef parse2text(srtfile, lang):\n  st = Subtitle(srtfile, lang)\n  text = st.plaintext()\n  print(text)\n```\n\n# Development\n\n### Clone project\n```\ngit clone https://github.com/qishe-nlp/subtitlecore.git\n```\n\n### Install [poetry](https://python-poetry.org/docs/)\n\n### Install dependencies\n```\npoetry update\n```\n\n### Test\n```\npoetry run pytest -rP\n```\nwhich run tests under `tests/*`\n\n### Execute\n```\npoetry run subtitlecore_content --help\npoetry run subtitlecore_parse2sens --help\npoetry run subtitlecore_parse2text --help\n```\n\n### Create sphinx docs\n```\npoetry shell\ncd apidocs\nsphinx-apidoc -f -o source ../subtitlecore\nmake html\npython -m http.server -d build/html\n```\n\n### Hose docs on github pages\n```\ncp -rf apidocs/build/html/* docs/\n```\n\n### Build\n* Change `version` in `pyproject.toml` and `subtitlecore/__init__.py`\n* Build python package by `poetry build`\n\n### Git commit and push\n\n### Publish from local dev env\n* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)\n* Publish to pypi test by `poetry publish -r test`\n\n### Publish through CI \n\n* Github action build and publish package to [test pypi repo](https://test.pypi.org/)\n\n```\ngit tag [x.x.x]\ngit push origin master\n```\n\n* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/subtitlecore/actions/workflows/pypi.yml)\n\n',
    'author': 'Phoenix.Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qishe-nlp/subtitlecore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
