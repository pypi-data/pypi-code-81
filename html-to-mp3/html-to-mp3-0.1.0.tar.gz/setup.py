# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['html_to_mp3']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['html2mp3 = html_to_mp3.html_to_mp3:html2mp3']}

setup_kwargs = {
    'name': 'html-to-mp3',
    'version': '0.1.0',
    'description': 'Convert HTML and text to mp3s',
    'long_description': None,
    'author': 'Michael Wooley',
    'author_email': 'wm.wooley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
