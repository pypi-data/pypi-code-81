# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yfbasic', 'yfbasic.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'yfbasic',
    'version': '0.2.0',
    'description': 'Thin python wrapper to retrieve and work with Yahoo! finance data',
    'long_description': 'yfbasic\n=======\n\nA thin python wrapper to retrieve price action data from the Yahoo! finance API.\n\nThere are similar packages available that does this, most notably\n[yfinance](https://github.com/ranaroussi/yfinance). The purpose of this package\nis to present the raw data as typed objects to be consumed as desired.\n\n# Getting started\n\nThe interface is straight forward, just import and query.\n\n``` python\nimport yfbasic\n\ndata = yfbasic.query("GME")\n```\n\nThe supporting parameters are typed as well.\n\n``` python\nimport yfbasic\nfrom yfbasic import Range, Interval\n\ndata = yfbasic.query("GME", range=Range.r1mo, interval=Interval.i1h)\n```\n\nYou can use `query_threaded` to parallelise the data retrieval.\n\n``` python\nimport yfbasic\n\nsymbols = ("GME", "AMC", "TSLA")\n\ndata = yfbasic.query_threaded(symbols)\n```\n\n# Working with the data\n\nThe data is modelled directly of the structure returned by the yahoo api. This\nmakes it a bit more low level to work with, but the package makes no presumptions about\nhow you intend to work with the data.\n\nThe best way to understand the data is to look at the [data structure](yfbasic/models/chart.py)\ndirectly.\n\n## Error handling\n\nIf we look at the `Chart` data model it contains two optional parameters, \n`result` and `error` which means we need to do application side checking of the\ndata. To satisfy type safety we need to at least verify the existence of\nresults by checking `data.chart.results` . If we want insight into any API side\nerrors we could verify and action upon `data.chart.error`\n\n``` python\nimport yfbasic\n\ndata = yfbasic.query("GME")\n\n# verifying the API produced results.\nif data.chart.result:\n    result = data.chart.result[0]\n    quotes = result.indicators.quote[0]\n\n    # getting price action data\n    timestamps = result.timestamp\n    open = quotes.open\n    close = quotes.close\n    high = quotes.high\n    low = quotes.low\n    volume = quotes.volume\n```\n',
    'author': 'jens',
    'author_email': 'jens.v.han@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/jensusius/yfbasic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
