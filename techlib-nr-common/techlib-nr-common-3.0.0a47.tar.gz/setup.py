# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_common',
 'nr_common.alembic',
 'nr_common.jsonschemas',
 'nr_common.jsonschemas.nr_common',
 'nr_common.mapping_includes',
 'nr_common.mapping_includes.v7',
 'nr_common.mappings',
 'nr_common.mappings.v7',
 'nr_common.mappings.v7.nr_common',
 'nr_common.marshmallow']

package_data = \
{'': ['*']}

install_requires = \
['idutils>=1.1.8,<2.0.0',
 'isbnlib>=3.10.3,<4.0.0',
 'oarepo-invenio-model>=2.0.0,<3.0.0',
 'oarepo-search>=1.0.0,<2.0.0',
 'python-stdnum>=1.16,<2.0']

extras_require = \
{'docs': ['sphinx>=1.5.1,<2.0.0']}

entry_points = \
{'invenio_db.alembic': ['nr_common = nr_common:alembic'],
 'invenio_jsonschemas.schemas': ['nr_common = nr_common.jsonschemas'],
 'oarepo_mapping_includes': ['nr_common = nr_common.mapping_includes']}

setup_kwargs = {
    'name': 'techlib-nr-common',
    'version': '3.0.0a47',
    'description': 'NR common data types',
    'long_description': '# nr-common\n\n[![Build Status](https://travis-ci.org/Narodni-repozitar/nr-common.svg?branch=master)](https://travis-ci.org/Narodni-repozitar/nr-common)\n[![Coverage Status](https://coveralls.io/repos/github/Narodni-repozitar/nr-common/badge.svg)](https://coveralls.io/github/Narodni-repozitar/nr-common)\n\nDisclaimer: The library is part of the Czech National Repository, and therefore the README is written in Czech.\nGeneral libraries extending [Invenio](https://github.com/inveniosoftware) are concentrated under the [Oarepo\n namespace](https://github.com/oarepo).\n \n ## Instalace\n \n Nejedná se o samostatně funkční knihovnu, proto potřebuje běžící Invenio a závislosti Oarepo.\n Knihovna se instaluje klasicky přes pip\n \n```bash\npip install techlib-nr-common\n```\n\nPro testování a/nebo samostané fungování knihovny je nutné instalovat tests z extras.\n\n```bash\npip install -e .[tests]\n```\n\n## Účel\n\nKnihovna obsahuje obecný metadatový model Národního repozitáře (Marshmallow, JSON schema a Elastisearch mapping).\nDále se stará o perzistetní identifikátor (PID) a obsahuje Invenio\n[fetcher](https://invenio-pidstore.readthedocs.io/en/latest/usage.html#fetchers) \na&nbsp;[minter](https://invenio-pidstore.readthedocs.io/en/latest/usage.html#minters). Všechny tyto části lze \n"podědit" v dalších metadatových modelech.\n\nKnihovna není samostatný model pro "generic" věci - ten je v nr-generic.',
    'author': 'Daniel Kopecký',
    'author_email': 'Daniel.Kopecky@techlib.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
