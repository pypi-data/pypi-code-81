# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_theses',
 'nr_theses.jsonschemas',
 'nr_theses.jsonschemas.nr_theses',
 'nr_theses.mapping_includes',
 'nr_theses.mapping_includes.v7',
 'nr_theses.mappings',
 'nr_theses.mappings.v7',
 'nr_theses.marshmallow']

package_data = \
{'': ['*'], 'nr_theses.mappings.v7': ['nr_theses/*']}

install_requires = \
['oarepo>=3.3.59,<4.0.0', 'techlib-nr-common>=3.0.0a45,<4.0.0']

entry_points = \
{'invenio_base.api_apps': ['theses = nr_theses:NRTheses'],
 'invenio_base.apps': ['theses = nr_theses:NRTheses'],
 'invenio_jsonschemas.schemas': ['nr_theses = nr_theses.jsonschemas'],
 'invenio_pidstore.fetchers': ['nr_theses = '
                               'nr_theses.fetchers:nr_theses_id_fetcher'],
 'invenio_pidstore.minters': ['nr_theses = '
                              'nr_theses.minters:nr_theses_id_minter'],
 'invenio_search.mappings': ['nr_theses = nr_theses.mappings'],
 'oarepo_mapping_includes': ['nr_theses = nr_theses.mapping_includes']}

setup_kwargs = {
    'name': 'techlib-nr-theses',
    'version': '1.0.0a7',
    'description': 'Czech National Repository theses data model.',
    'long_description': '# NR-Theses\n\n[![Build Status](https://travis-ci.org/Narodni-repozitar/nr-theses.svg?branch=master)](https://travis-ci.org/Narodni-repozitar/nr-theses)\n[![Coverage Status](https://coveralls.io/repos/github/Narodni-repozitar/nr-theses/badge.svg?branch=master)](https://coveralls.io/github/Narodni-repozitar/nr-theses?branch=master)\n\n\nDisclaimer: The library is part of the Czech National Repository, and therefore the README is written in Czech.\nGeneral libraries extending [Invenio](https://github.com/inveniosoftware) are concentrated under the [Oarepo\n namespace](https://github.com/oarepo).\n\n  ## Instalace\n\n Nejedná se o samostatně funkční knihovnu, proto potřebuje běžící Invenio a závislosti Oarepo.\n Knihovna se instaluje ze zdroje.\n\n ```bash\ngit clone git@github.com:Narodni-repozitar/nr-theses.git\ncd nr-common\npip install poetry\npoetry install\n```\n\nPro testování a/nebo samostané fungování knihovny je nutné instalovat tests z extras.\n\n```bash\npoetry install --extras tests\n```\n\n:warning: Pro instalaci se používá Manažer závilostí **Poetry** více infromací lze naleznout v\n[dokumentaci](https://python-poetry.org/docs/)\n\n## Účel\n\nKnihovna rozšiřuje [obecný metadatový model](https://github.com/Narodni-repozitar/nr-common)\no pole pro vysokoškolské závěrečné práce. Vysokoškolským pracím je přiřazen endpoint **/api/theses**. Knihovna\nposkytuje API pro CRUD operace pod proxy **nr_these**.\n\n## Použití\n\nBude dopsáno.\n',
    'author': 'Daniel Kopecký',
    'author_email': 'Daniel.Kopecky@techlib.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
