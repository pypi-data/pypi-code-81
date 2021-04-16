# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_reconcile_geo']

package_data = \
{'': ['*']}

install_requires = \
['geopy>=2.1.0,<3.0.0']

entry_points = \
{'csv_reconcile.scorers': ['geo = csv_reconcile_geo']}

setup_kwargs = {
    'name': 'csv-reconcile-geo',
    'version': '0.1.2',
    'description': 'Geo distance scoring plugin for csv-reconcile',
    'long_description': '\n# Table of Contents\n\n1.  [CSV Reconcile Geo distance scoring plugin](#org9a92411)\n    1.  [Reconciliation](#orgdc5ce9f)\n    2.  [Scoring](#org6e0d3e3)\n    3.  [Configuration](#org995a45b)\n    4.  [Future enhancements](#org5b7cc3c)\n\n\n<a id="org9a92411"></a>\n\n# CSV Reconcile Geo distance scoring plugin\n\nA scoring plugin for [csv-reconcile](https://github.com/gitonthescene/csv-reconcile) using geodesic distance.  See csv-reconcile for details.\n\n\n<a id="orgdc5ce9f"></a>\n\n## Reconciliation\n\nThis plugin is used to reconcile values representing points on the globe.  It expects those\nvalues to be in [well-known text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format for a point.  That is, like so: `POINT( longitude latitude )`.\n\nThe pre-processor automatically strips off [literal datatypes](https://www.w3.org/TR/sparql11-query/#matchingRDFLiterals) when present as well as double quotes.\n\nThe CSV column to be reconciled needs to be in the same format.  In addition, there must be at\nmost one instance of any id column.  For instance, if reconciling against [coordinate location](https://www.wikidata.org/wiki/Property:P625) for\na [wikidata item](https://www.wikidata.org/wiki/Help:Items), there must be at most one location per item.\n\n\n<a id="org6e0d3e3"></a>\n\n## Scoring\n\nThe scoring used is more or less arbitrary but has the following properties:\n\n-   The highest score is 100 and occurs when the distance to the reconciliation candidate is zero\n-   The lower the score the greater the distance to the reconciliation candidate\n-   The score is scaled so that a distance of 10km yields a score of 50\n\n\n<a id="org995a45b"></a>\n\n## Configuration\n\nThe plugin can be controlled via `SCOREOPTIONS` in the csv-reconcile `--config` file.\n`SCOREOPTIONS` is a [Python dictionary](https://www.w3schools.com/python/python_dictionaries.asp) and thus has the following form `SCOREOPTIONS={\n   "key1":"value1,"key2":"value2"}`.\n\n-   `SCALE` set distance in kilometers at which a score of 50 occurs.  ( Default 10km )  e.g. `"SCALE":2`\n-   `COORDRANGE` If supplied do a precheck that both the latitude and the longitude of the compared\n    values are within range.  This is for performance to avoid the more expensive distance\n    calculation for points farther apart. e.g. `"COORDRANGE":"1"`\n\n\n<a id="org5b7cc3c"></a>\n\n## Future enhancements\n\nSome of the current implementation was driven by the current design of csv-reconcile.  Both may\nbe updated to accommodate the following:\n\n-   Allow for separate latitude and longitude column in the CSV file\n-   Do some preliminary checks on coordinates before calculating distance for performance\n-   Add some scoring options such as the following:\n    -   Allow for overriding the scaling function\n    -   etc.\n\n',
    'author': 'Douglas Mennella',
    'author_email': 'trx2358-pypi@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gitonthescene/csv-reconcile-geo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
