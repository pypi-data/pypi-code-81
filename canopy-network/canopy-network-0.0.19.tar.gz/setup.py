# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canopy', 'canopy.templates']

package_data = \
{'': ['*'], 'canopy': ['static/*']}

install_requires = \
['understory>=0.0.12,<0.0.13']

entry_points = \
{'console_scripts': ['loveliness = understory.loveliness:main'],
 'web.apps': ['canopy = canopy:app']}

setup_kwargs = {
    'name': 'canopy-network',
    'version': '0.0.19',
    'description': 'A decentralized social network.',
    'long_description': '# canopy\na decentralized social network\n\nStore and display content on your own personal website. Interact richly\nwith other sites.\n\n## Install\n\n[Spawn a host](https://gh.ost.lol), install `canopy-network`, add your\ndomain and mount the canopy app.\n\n## Features\n\n* render profile, pages, media, posts and feeds with semantic markup a la [microformats](https://indieweb.org/microformats)\n  * archive source material for [reply contexts](https://indieweb.org/reply-context)\n  * moderated threaded discussion using Webmentions with Salmention & Vouch\n  * syndicate to third-party aggregators\n* store posts:\n  * as [queryable JSON](https://www.sqlite.org/json1.html) in SQLite database\n    * [full-text search](https://www.sqlite.org/fts5.html)\n  * as JSON flat files inside Git repository for change history\n* follow by subscribing and publish to subscribers using WebSub\n* sign in to third-party applications using IndieAuth\n  * leverage third-party Micropub editors\n  * leverage third-party Microsub readers\n* import/export tools\n  * syndicate/backfeed to/from Twitter/Github/Facebook\n  * backup/restore to/from local/remote storage\n',
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
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
