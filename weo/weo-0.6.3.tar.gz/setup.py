# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weo']

package_data = \
{'': ['*']}

install_requires = \
['iso3166>=1.0.1,<2.0.0',
 'matplotlib==3.2',
 'pandas>=1.1.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'weo',
    'version': '0.6.3',
    'description': 'Python client to download IMF World Economic Outlook (WEO) dataset as pandas dataframes.',
    'long_description': '# weo-reader\n\n[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/epogrebnyak/weo-reader)\n![pytest](https://github.com/epogrebnyak/weo-reader/workflows/pytest/badge.svg)\n[![Downloads](https://pepy.tech/badge/weo/week)](https://pepy.tech/project/weo/week)\n\nThis is a Python client to download [IMF World Economic Outlook Report][weo] dataset as [pandas](https://pandas.pydata.org/) dataframes by release dates. You can explore:\n- single country macroeconomic data and forecast, \n- macro variables across countries for a given year,\n- country-year panel for single macro variable. \n\nDataset releases (vintages) are available back to 2007, the reported data goes back to 1980, forecast is three years ahead.\n\n[weo]: https://www.imf.org/en/Publications/WEO\n\n\n![изображение](https://user-images.githubusercontent.com/9265326/103473902-8c64da00-4dae-11eb-957c-4737f56abdce.png)\n\n\n## Install\n\nThe program is tested to run under Python 3.8. It may work well with Python version 3.6 and above.\n\nTo install `weo`:\n\n`pip install weo`\n\n## Step 1. Download data\n   \nYou need to save data as from IMF web site as local file. Specify year\nand release: \n\n```python \nimport weo\n\nweo.download(year=2020, release="Oct", filename="weo.csv")\n```\n\nYou can access WEO releases starting October 2007 with this client. WEO is normally released in April and October, one exception is September 2011. \n\nRelease is referenced by number (`1` or `2`) or by month (`\'Apr\'` or `\'Oct\'`, and `\'Sep\'` in 2011).\n\nYour can list all years and releases available for download  with  `weo.all_releases()`. Combine it to create local dataset of WEO vintages from 2007 to present:\n\n```python\n\nfrom weo import all_releases\n\nfor (year, release) in all_releases():\n  weo.download(year, release, directory=\'weo_data\') \n```\n\nNote that folder \'weo_data\' must exist for this script to run.\n\n## Step 2. Inspect data\n\nUse `WEO` class to view and extract data. `WEO` is a wrapper around a pandas dataframe that ensures proper data import and easier access and slicing of data. \n\n\nTry code below:\n\n```python\nfrom weo import WEO\n\nw = WEO("weo.csv")\n```\n\nWhat variables and measurements are inside?\n\n```python\n# variable listing\nw.variables()\n\n# units\nw.units()\nw.units("Gross domestic product, current prices")\n\n# variable codes\nw.codes\nw.from_code("LUR")\n\n# countries\nw.countries("United")      # Dataframe with United Arab Emirates, United Kingdom\n                           # and United States\nw.iso_code3("Netherlands") # \'NLD\'\n```\n\nThe dataset is year-country-variable-value cube, you can fix any dimension to get a table.\n```python\n\nw.get("General government gross debt", "Percent of GDP")\nw.getc("NGDP_RPCH")\nw.country("DEU")\nw.fix_year(1994)\n```\n\nPlot a chart with the projected 12 largest economies in 2024 (current prices):\n\n```python\n(w.gdp_usd(2024)\n  .dropna()\n  .sort_values()\n  .tail(12)\n  .plot\n  .barh(title="GDP by country, USD billion (2024)")\n)\n```\n\nGet GDP per capita data from 2000 to 2020:\n\n```python\nw.gdp_pc_usd(start_year=2000, end_year=2020)\n```\n\n## Alternative data sources\n\n1\\. If you need the latest data as time series and not the vintages of WEO releases, and you know \nvariables that you are looking for, *dbnomics* is a good choice: \n- <https://db.nomics.world/IMF/WEO>\n- <https://db.nomics.world/IMF/WEOAGG>\n\nSmall example:\n\n```python\nfrom dbnomics import fetch_series_by_api_link\nts1 = fetch_series_by_api_link("https://api.db.nomics.world/v22/"\n                               "series/IMF/WEO/DEU.NGDPRPC"\n                               "?observations=1")\n```\n\n2\\. Similar dataset, not updated since 2018, but with earlier years: https://github.com/datasets/imf-weo\n\n## Development notes\n\n- You can download the WEO file in command line with `curl` command:\n```\ncurl -o weo.csv https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/02/WEOOct2020all.xls\n```\n- `WEOOct2020all.xls` from the web site is really a CSV file, not an Excel file.\n- There is an update of GDP figures in [June 2020](jun2020), but the file structure is incompatible with regular releases.\n- Prior to 2020 the URL was similar to `https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls`\n\n[jun2020]: https://www.imf.org/en/Publications/WEO/Issues/2020/06/24/WEOUpdateJune2020\n',
    'author': 'Evgeny Pogrebnyak',
    'author_email': 'e.pogrebnyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/epogrebnyak/weo-reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
