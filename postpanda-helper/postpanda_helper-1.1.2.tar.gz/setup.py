# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postpanda_helper']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3,<6.0',
 'SQLAlchemy>=1.3,<2.0',
 'logger-mixin>=1.1.0,<2.0.0',
 'numpy>=1.15,<2.0',
 'pandas>=1.1,<2.0',
 'pathvalidate>=2.3.2,<3.0.0',
 'psycopg2>=2.8,<3.0']

extras_require = \
{'geo': ['GeoAlchemy2>=0.8.4,<0.9.0', 'geopandas>=0.9.0,<0.10.0']}

setup_kwargs = {
    'name': 'postpanda-helper',
    'version': '1.1.2',
    'description': 'Various helpers for Postgres and Pandas, including SelectSert',
    'long_description': '# PostPanda Helper\n[![PyPI](https://img.shields.io/pypi/v/postpanda-helper?style=flat)](https://pypi.org/project/postpanda-helper/)\n[![PyPI - License](https://img.shields.io/pypi/l/postpanda-helper?style=flat)](https://pypi.org/project/postpanda-helper/)\n\nVarious helpers for PostgreSQL and Pandas \n\n[![Documentation](https://img.shields.io/static/v1?label=&message=Documentation&color=blue&style=for-the-badge&logo=Read+the+Docs&logoColor=white)](https://ds-mn.github.io/postpanda_helper/)',
    'author': 'Daniel Sullivan',
    'author_email': '57496265+ds-mn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ds-mn/postpanda_helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
