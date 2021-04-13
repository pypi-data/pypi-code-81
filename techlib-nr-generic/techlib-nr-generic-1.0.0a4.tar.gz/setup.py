# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_generic', 'nr_generic.mappings', 'nr_generic.mappings.v7']

package_data = \
{'': ['*'], 'nr_generic.mappings.v7': ['nr_common/*']}

install_requires = \
['idutils>=1.1.8,<2.0.0',
 'isbnlib>=3.10.3,<4.0.0',
 'oarepo-invenio-model>=2.0.0,<3.0.0',
 'python-stdnum>=1.16,<2.0',
 'techlib-nr-common>=3.0.0a45,<4.0.0']

extras_require = \
{'docs': ['sphinx>=1.5.1,<2.0.0']}

entry_points = \
{'invenio_base.api_apps': ['nr_generic = nr_generic:NRCommon'],
 'invenio_base.apps': ['nr_generic = nr_generic:NRCommon'],
 'invenio_pidstore.fetchers': ['nr_generic = '
                               'nr_generic.fetchers:nr_id_generic_fetcher'],
 'invenio_pidstore.minters': ['nr_generic = '
                              'nr_generic.minters:nr_id_generic_minter'],
 'invenio_search.mappings': ['nr_common = nr_generic.mappings']}

setup_kwargs = {
    'name': 'techlib-nr-generic',
    'version': '1.0.0a4',
    'description': 'NR generic model REST API',
    'long_description': '# nr-common\n\n[![Build Status](https://travis-ci.org/Narodni-repozitar/nr-common.svg?branch=master)](https://travis-ci.org/Narodni-repozitar/nr-common)\n[![Coverage Status](https://coveralls.io/repos/github/Narodni-repozitar/nr-common/badge.svg)](https://coveralls.io/github/Narodni-repozitar/nr-common)\n\nDisclaimer: The library is part of the Czech National Repository, and therefore the README is written in Czech.\nGeneral libraries extending [Invenio](https://github.com/inveniosoftware) are concentrated under the [Oarepo\n namespace](https://github.com/oarepo).\n \n ## Instalace\n \n Nejedná se o samostatně funkční knihovnu, proto potřebuje běžící Invenio a závislosti Oarepo.\n Knihovna se instaluje klasicky přes pip\n \n```bash\npip install techlib-nr-common\n```\n\nPro testování a/nebo samostané fungování knihovny je nutné instalovat tests z extras.\n\n```bash\npip install -e .[tests]\n```\n\n## Účel\n\nKnihovna obsahuje REST api pro obecný metadatový model definovaný v nr-generic.',
    'author': 'Mirek Simek',
    'author_email': 'simeki@vscht.cz',
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
