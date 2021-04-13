# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['html_table_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-table-parser-python3',
    'version': '0.2.0',
    'description': 'A small and simple HTML table parser not requiring any external dependency.',
    'long_description': '# html-table-parser-python3.5+\n\nThis module consists of just one small class. Its purpose is to parse HTML\ntables without help of external modules. Everything used is part of python 3.\n\n## Installation\n\n    pip install html-table-parser-python3\n\n## How to use\n\nExample Usage:\n\n    import urllib.request\n    from pprint import pprint\n    from html_table_parser.parser import HTMLTableParser\n    \n    \n    def url_get_contents(url):\n        """ Opens a website and read its binary contents (HTTP Response Body) """\n        req = urllib.request.Request(url=url)\n        f = urllib.request.urlopen(req)\n        return f.read()\n\n\n    def main():\n        url = \'http://www.twitter.com\'\n        xhtml = url_get_contents(url).decode(\'utf-8\')\n\n        p = HTMLTableParser()\n        p.feed(xhtml)\n        pprint(p.tables)\n\n\n    if __name__ == \'__main__\':\n        main()\n\nThe parser returns a nested lists of tables containing rows containing cells\nas strings. Tags in cells are stripped and the tags text content is joined.\nThe console output for parsing all tables on the twitter home page looks\nlike this:\n\n```\n>>>\n[[[\'\', \'Anmelden\']],\n [[\'Land\', \'Code\', \'Für Kunden von\'],\n  [\'Vereinigte Staaten\', \'40404\', \'(beliebig)\'],\n  [\'Kanada\', \'21212\', \'(beliebig)\'],\n  ...\n  [\'3424486444\', \'Vodafone\'],\n  [\'Zeige SMS-Kurzwahlen für andere Länder\']]]\n```\n\n## CLI\n\nThere is also a command line interface which you can use directly to\ngenerate a CSV:\n\n    ./html_table_converter -u http://web.archive.org/web/20180524092138/http://metal-train.de/index.php/fahrplan.html -o metaltrain\n\n## Credit\n\nAll Credit goes to Josua Schmid (schmijos). This is all his work, I just uploaded it to PyPi. Original repository can be found at:\n\nhttps://github.com/schmijos/html-table-parser-python3\n\n## License\n\nGNU GPL v3\n',
    'author': 'Arran Hobson Sayers',
    'author_email': 'ahobsonsayers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ahobsonsayers/html-table-parser-python3',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
