# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataprep',
 'dataprep.assets',
 'dataprep.clean',
 'dataprep.connector',
 'dataprep.connector.generator',
 'dataprep.connector.schema',
 'dataprep.datasets',
 'dataprep.eda',
 'dataprep.eda.correlation',
 'dataprep.eda.correlation.compute',
 'dataprep.eda.create_report',
 'dataprep.eda.diff',
 'dataprep.eda.diff.compute',
 'dataprep.eda.distribution',
 'dataprep.eda.distribution.compute',
 'dataprep.eda.missing',
 'dataprep.eda.missing.compute',
 'dataprep.eda.outlier',
 'dataprep.tests',
 'dataprep.tests.clean',
 'dataprep.tests.connector',
 'dataprep.tests.datasets',
 'dataprep.tests.eda']

package_data = \
{'': ['*'],
 'dataprep.connector': ['assets/*'],
 'dataprep.datasets': ['data/*'],
 'dataprep.eda': ['templates/*'],
 'dataprep.eda.create_report': ['templates/*']}

install_requires = \
['aiohttp>=3.6,<4.0',
 'bokeh>=2,<3',
 'bottleneck>=1.3,<2.0',
 'dask[dataframe,delayed,array]>=2.25,<3.0',
 'ipywidgets>=7.5,<8.0',
 'jinja2>=2.11,<3.0',
 'jsonpath-ng>=1.5,<2.0',
 'metaphone>=0.6,<0.7',
 'nltk>=3.5,<4.0',
 'numpy>=1,<2',
 'pandas>=1.1,<2.0',
 'pydantic>=1.6,<2.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'regex>=2020.10.15,<2021.0.0',
 'scipy>=1,<2',
 'tqdm>=4.48,<5.0',
 'usaddress>=0.5.10,<0.6.0',
 'wordcloud>=1.8,<2.0']

setup_kwargs = {
    'name': 'dataprep',
    'version': '0.3.0a1',
    'description': 'Dataprep: Data Preparation in Python',
    'long_description': '<div align="center"><img width="100%" src="https://github.com/sfu-db/dataprep/raw/develop/assets/logo.png"/></div>\n\n---\n\n<p align="center">\n  <a href="LICENSE"><img src="https://img.shields.io/pypi/l/dataprep?style=flat-square"/></a>\n  <a href="https://sfu-db.github.io/dataprep/"><img src="https://img.shields.io/badge/dynamic/json?color=blue&label=docs&prefix=v&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdataprep%2Fjson&style=flat-square"/></a>\n  <a href="https://pypi.org/project/dataprep/"><img src="https://img.shields.io/pypi/pyversions/dataprep?style=flat-square"/></a>\n  <a href="https://www.codacy.com/gh/sfu-db/dataprep?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sfu-db/dataprep&amp;utm_campaign=Badge_Coverage"><img src="https://app.codacy.com/project/badge/Coverage/ed658f08dcce4f088c850253475540ba"/></a>\n<!--   <a href="https://codecov.io/gh/sfu-db/dataprep"><img src="https://img.shields.io/codecov/c/github/sfu-db/dataprep?style=flat-square"/></a> -->\n  <a href="https://www.codacy.com/gh/sfu-db/dataprep?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sfu-db/dataprep&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/ed658f08dcce4f088c850253475540ba"/></a>\n  <a href="https://discord.gg/xwbkFNk"><img src="https://img.shields.io/discord/702765817154109472?style=flat-square"/></a>\n</p>\n\n<p align="center">\n  <a href="https://sfu-db.github.io/dataprep/">Documentation</a>\n  |\n  <a href="https://discord.gg/xwbkFNk">Discord</a>\n  | \n  <a href="https://github.com/sfu-db/dataprep/discussions">Forum</a>\n</p>\n\nDataPrep lets you prepare your data using a single library with a few lines of code.\n\nCurrently, you can use DataPrep to:\n\n- Collect data from common data sources (through [`dataprep.connector`](#connector))\n- Do your exploratory data analysis (through [`dataprep.eda`](#eda))\n- Clean and standardize data (through [`dataprep.clean`](#clean))\n- ...more modules are coming\n\n## Releases\n\n<div align="center">\n  <table>\n    <tr>\n      <th>Repo</th>\n      <th>Version</th>\n      <th>Downloads</th>\n    </tr>\n    <tr>\n      <td>PyPI</td>\n      <td><a href="https://pypi.org/project/dataprep/"><img src="https://img.shields.io/pypi/v/dataprep?style=flat-square"/></a></td>\n      <td><a href="https://pepy.tech/project/dataprep"><img src="https://pepy.tech/badge/dataprep"/></a></td>\n    </tr>\n    <tr> \n      <td>conda-forge</td>\n      <td><a href="https://anaconda.org/conda-forge/dataprep"><img src="https://img.shields.io/conda/vn/conda-forge/dataprep.svg"/></a></td>\n      <td><a href="https://anaconda.org/conda-forge/dataprep"><img src="https://img.shields.io/conda/dn/conda-forge/dataprep.svg"/></a></td>\n    </tr>\n  </table>\n</div>\n\n## Installation\n\n```bash\npip install -U dataprep\n```\n\n## Connector\n\nConnector is an intuitive, open-source API wrapper that speeds up development by standardizing calls to multiple APIs as a simple workflow.\n\nConnector provides a simple wrapper to collect structured data from different Web APIs (e.g., Twitter, Spotify), making web data collection easy and efficient, without requiring advanced programming skills.\n\nDo you want to leverage the growing number of websites that are opening their data through public APIs? Connector is for you!\n\nLet\'s check out the several benefits that Connector offers:\n\n- **A unified API:** You can fetch data using one or two lines of code to get data from [tens of popular websites](https://github.com/sfu-db/DataConnectorConfigs).\n- **Auto Pagination:** Do you want to invoke a Web API that could return a large result set and need to handle it through pagination? Connector automatically does the pagination for you! Just specify the desired number of returned results (argument `_count`) without getting into unnecessary detail about a specific pagination scheme.\n- **Smart API request strategy:** Do you want to fetch results more quickly by making concurrent requests to Web APIs? Through the `_concurrency` argument, Connector simplifies concurrency, issuing API requests in parallel while respecting the API\'s rate limit policy.\n#### How to fetch all publications of Andrew Y. Ng?\n\n```python\nfrom dataprep.connector import connect\nconn_dblp = connect("dblp", _concurrency = 5)\ndf = await conn_dblp.query("publication", author = "Andrew Y. Ng", _count = 2000)\n```\n\nHere, you can find detailed [Examples.](https://github.com/sfu-db/dataprep/tree/develop/examples)\n\nConnector is designed to be easy to extend. If you want to connect with your own web API, you just have to write a simple [configuration file](https://github.com/sfu-db/DataConnectorConfigs/blob/develop/CONTRIBUTING.md#add-configuration-files) to support it. This configuration file describes the API\'s main attributes like the URL, query parameters, authorization method, pagination properties, etc.\n\n## EDA\n\nDataPrep.EDA is the fastest and the easiest EDA (Exploratory Data Analysis) tool in Python. It allows you to understand a Pandas/Dask DataFrame with a few lines of code in seconds.\n\n#### Create Profile Reports, Fast\n\nYou can create a beautiful profile report from a Pandas/Dask DataFrame with the `create_report` function. DataPrep.EDA has the following advantages compared to other tools:\n\n- **10-100X Faster**: DataPrep.EDA is 10-100X faster than Pandas-based profiling tools due to its highly optimized Dask-based computing module.\n- **Interactive Visualization**: DataPrep.EDA generates interactive visualizations in a report, which makes the report look more appealing to end users.\n- **Big Data Support**: DataPrep.EDA naturally supports big data stored in a Dask cluster by accepting a Dask dataframe as input.\n\nThe following code demonstrates how to use DataPrep.EDA to create a profile report for the titanic dataset.\n\n```python\nfrom dataprep.datasets import load_dataset\nfrom dataprep.eda import create_report\ndf = load_dataset("titanic")\ncreate_report(df).show_browser()\n```\n\nClick [here](https://sfu-db.github.io/dataprep/_downloads/c9bf292ac949ebcf9b65bb2a2bc5a149/titanic_dp.html) to see the generated report of the above code.\n\n#### Innovative System Design\n\nDataPrep.EDA is the **_only_** task-centric EDA system in Python. It is carefully designed to improve usability.\n\n- **Task-Centric API Design**: You can declaratively specify a wide range of EDA tasks in different granularities with a single function call. All needed visualizations will be automatically and intelligently generated for you.\n- **Auto-Insights**: DataPrep.EDA automatically detects and highlights the insights (e.g., a column has many outliers) to facilitate pattern discovery about the data.\n- **[How-to Guide](https://sfu-db.github.io/dataprep/user_guide/eda/how_to_guide.html)** : A how-to guide is provided to show the configuration of each plot function. With this feature, you can easily customize the generated visualizations.\n\n#### Understand the Titanic dataset with Task-Centric API:\n\n<a href="assets/eda_demo.gif"><img src="assets/eda_demo.gif"/></a>\n\nClick [here](https://sfu-db.github.io/dataprep/user_guide/eda/introduction.html) to check all the supported tasks.\n\nCheck [plot](https://sfu-db.github.io/dataprep/user_guide/eda/plot.html), [plot_correlation](https://sfu-db.github.io/dataprep/user_guide/eda/plot_correlation.html), [plot_missing](https://sfu-db.github.io/dataprep/user_guide/eda/plot_missing.html) and [create_report](https://sfu-db.github.io/dataprep/user_guide/eda/create_report.html) to see how each function works.\n\n## Clean\n\nDataPrep.Clean contains simple functions designed for cleaning and validating data in a DataFrame. It provides\n\n- **A Unified API**: each function follows the syntax `clean_{type}(df, \'column name\')` (see an example below).\n- **Speed**: the computations are parallelized using Dask. It can clean **50K rows per second** on a dual-core laptop (that means cleaning 1 million rows in only 20 seconds).\n- **Transparency**: a report is generated that summarizes the alterations to the data that occured during cleaning.\n\nThe following example shows how to clean and standardize a column of country names.\n\n``` python\nfrom dataprep.clean import clean_country\nimport pandas as pd\ndf = pd.DataFrame({\'country\': [\'USA\', \'country: Canada\', \'233\', \' tr \', \'NA\']})\ndf2 = clean_country(df, \'country\')\ndf2\n           country  country_clean\n0              USA  United States\n1  country: Canada         Canada\n2              233        Estonia\n3              tr          Turkey\n4               NA            NaN\n```\n\nType validation is also supported:\n\n``` python\nfrom dataprep.clean import validate_country\nseries = validate_country(df[\'country\'])\nseries\n0     True\n1    False\n2     True\n3     True\n4    False\nName: country, dtype: bool\n```\n\n**Currently supports functions for:** Column Headers | Country Names | Dates and Times | Duplicate Strings | Email Addresses | Geographic Coordinates | IP Addresses | Phone Numbers | URLs | US Street Addresses\n\n## Documentation\n\nThe following documentation can give you an impression of what DataPrep can do:\n\n- [Connector](https://sfu-db.github.io/dataprep/user_guide/connector/connector.html)\n- [EDA](https://sfu-db.github.io/dataprep/user_guide/eda/introduction.html)\n- [Clean](https://sfu-db.github.io/dataprep/user_guide/clean/introduction.html)\n\n## Contribute\n\nThere are many ways to contribute to DataPrep.\n\n- Submit bugs and help us verify fixes as they are checked in.\n- Review the source code changes.\n- Engage with other DataPrep users and developers on StackOverflow.\n- Help each other in the [DataPrep Community Discord](https://discord.gg/xwbkFNk) and [Forum].\n- [![Twitter]](https://twitter.com/sfu_db)\n- Contribute bug fixes.\n- Providing use cases and writing down your user experience.\n\nPlease take a look at our [wiki] for development documentations!\n\n[build status]: https://img.shields.io/circleci/build/github/sfu-db/dataprep/master?style=flat-square&token=f68e38757f5c98771f46d1c7e700f285a0b9784d\n[Forum]: https://github.com/sfu-db/dataprep/discussions\n[wiki]: https://github.com/sfu-db/dataprep/wiki\n[examples]: https://github.com/sfu-db/dataprep/tree/master/examples\n[twitter]: https://img.shields.io/twitter/follow/sfu_db?style=social\n\n## Acknowledgement\n\nSome functionalities of DataPrep are inspired by the following packages.\n\n- [Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling)\n\n  Inspired the report functionality and insights provided in `dataprep.eda`.\n\n- [missingno](https://github.com/ResidentMario/missingno)\n\n  Inspired the missing value analysis in `dataprep.eda`.\n',
    'author': 'SFU Database System Lab',
    'author_email': 'dsl.cs.sfu@gmail.com',
    'maintainer': 'Weiyuan Wu',
    'maintainer_email': 'youngw@sfu.com',
    'url': 'https://github.com/sfu-db/dataprep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
