# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['find_url']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'find-url',
    'version': '1.0.4',
    'description': 'С помощью этой библиотеки, вы сможете парсить информацию с сайта',
    'long_description': 'Пока что эта библиотека в разработке, вот что умеет эта библиотека: С помощью - import find_url вы импортируете библиотеку. Чтоб начать находить информацию, пишите find_url.url.find(url, f, f2). Сдесь url это ссылка которую надо парсить, f это на что начинается то, что вы хотите получить. f2 - На что заканчивается то, что вы хотите получить. Так же если вы получили готовый html код, используйте find.url.html(html, f, f2). Например, я хочу получить с сайта https://pypi.org/project/find-url/ название, то есть в html коде - <title>find-url · PyPI</title>. В этом случие То что мы хотим получить начинается на <title>, и заканчивается на </title>. То есть - find_url.url.find(\'https://pypi.org/project/find-url/\', \'<title>\', \'</title>\'). Всё это выдаст "find-url · PyPI"',
    'author': 'Sergey039',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
