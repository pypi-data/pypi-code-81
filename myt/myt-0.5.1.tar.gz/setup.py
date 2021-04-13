# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['t']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'pytz>=2021.1,<2022.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['t = t.__main__:main']}

setup_kwargs = {
    'name': 'myt',
    'version': '0.5.1',
    'description': 'Time, zones',
    'long_description': '# t\n\nCommand line tool for showing time in different time zones and other temporal information.\n\n```\npipx install --user myt\n```\n\n```\nUsage: t [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -J, --json  Output in JSON\n  --help      Show this message and exit.\n\nCommands:\n  m      Moon matrix\n  s      Sun and moon\n  t      Time in different zones\n  z      24hrs in time zones (on date)\n  zones  List common time zones and UTC offset (on date)\n```\n\n## t m\n\n```\nUsage: t m [OPTIONS]\n\nOptions:\n  -y, --year TEXT  Year for calculation\n  --help           Show this message and exit.\n```\n\nExample: \n```\nt % t m\n     Moon phases for year: 2021\n     01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\nJan  🌖 🌖 🌖 🌖 🌗 🌗 🌗 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌔 🌕 🌕 🌕 🌖\nFeb  🌖 🌖 🌗 🌗 🌗 🌗 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌕\nMar  🌖 🌖 🌖 🌖 🌗 🌗 🌗 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌖 🌖\nApr  🌖 🌖 🌗 🌗 🌗 🌗 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖\nMay  🌖 🌖 🌗 🌗 🌗 🌘 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌓 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖 🌖 🌖\nJun  🌗 🌗 🌗 🌗 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌖 🌖 🌖 🌖 🌗\nJul  🌗 🌗 🌗 🌘 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖 🌖 🌖 🌗 🌗\nAug  🌗 🌗 🌘 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌓 🌓 🌓 🌓 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖 🌖 🌖 🌖 🌗 🌗 🌗\nSep  🌗 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖 🌖 🌖 🌗 🌗 🌗 🌗\nOct  🌘 🌘 🌘 🌘 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖 🌖 🌖 🌖 🌗 🌗 🌗 🌗 🌘\nNov  🌘 🌘 🌑 🌑 🌑 🌑 🌒 🌒 🌒 🌓 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖 🌖 🌖 🌖 🌗 🌗 🌗 🌘 🌘\nDec  🌘 🌘 🌑 🌑 🌑 🌒 🌒 🌒 🌒 🌓 🌓 🌓 🌔 🌔 🌔 🌔 🌔 🌕 🌕 🌕 🌖 🌖 🌖 🌖 🌖 🌗 🌗 🌗 🌘 🌘 🌘\n```\n\n## t s\n\n```\nUsage: t s [OPTIONS]\n\nOptions:\n  -l, --location TEXT  Location as longitude,latitude (WGS84, dd)\n  -t, --date TEXT      Date for calculation\n  -f, --format TEXT    Output time format\n  --help               Show this message and exit.\n```\n\nExample:\n```\nt s -t "2021-04-24"\nLocation: -76.6963,39.0715\nRise: 05:51:28  06:19:41  06:56:02\nSet:  19:16:19  19:52:39  05:51:28\nMoon: 🌔 (0.40)\n```\n\n## t t\n\n```\nUsage: t t [OPTIONS]\n\n  Time in different zones\n\nOptions:\n  -t, --date TEXT   Date for calculation\n  -z, --zones TEXT  Comma separated list of timezones\n  --help            Show this message and exit.\n```\n\nExample:\n```\nt t -t "1 April 8pm"\nLocal             2021-04-01T20:00:00-0400\nEurope/Copenhagen 2021-04-02T02:00:00+0200\nUTC               2021-04-02T00:00:00+0000\nUS/Eastern        2021-04-01T20:00:00-0400\nUS/Central        2021-04-01T19:00:00-0500\nUS/Mountain       2021-04-01T18:00:00-0600\nAmerica/Phoenix   2021-04-01T17:00:00-0700\nUS/Pacific        2021-04-01T17:00:00-0700\nUS/Alaska         2021-04-01T16:00:00-0800\nPacific/Tahiti    2021-04-01T14:00:00-1000\nPacific/Auckland  2021-04-02T13:00:00+1300\nAustralia/Sydney  2021-04-02T11:00:00+1100\n```\n\n## t z\n\n```\nUsage: t z [OPTIONS]\n\n  24hrs in time zones (on date)\n\nOptions:\n  -f, --format TEXT  Output time format\n  -t, --date TEXT    Date for calculation\n  -z, --zones TEXT   Comma separated list of timezones\n  --help             Show this message and exit.\n```\n\nExample:\n```\nt z\nLocal             07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04 05 06\nEurope/Copenhagen 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04 05 06 07 08 09 10 11\nUTC               11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04 05 06 07 08 09 10\nUS/Eastern        07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04 05 06\nUS/Central        06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04 05\nUS/Mountain       05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04\nAmerica/Phoenix   04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03\nUS/Pacific        04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03\nUS/Alaska         03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02\nPacific/Tahiti    01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00\nPacific/Auckland  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23\nAustralia/Sydney  22 23 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21\n```\n\n## t zones\n\n```\nUsage: t zones [OPTIONS]\n\n  List common time zones and UTC offset (on date)\n\nOptions:\n  -t, --date TEXT  Date for calculation\n  --help           Show this message and exit.\n```\n\nExample:\n```\nt zones -t "2021-12-21"\n-11:00 Pacific/Midway\n-11:00 Pacific/Niue\n-11:00 Pacific/Pago_Pago\n-10:00 America/Adak\n-10:00 Pacific/Honolulu\n-10:00 Pacific/Rarotonga\n-10:00 Pacific/Tahiti\n-10:00 US/Hawaii\n-09:30 Pacific/Marquesas\n...\n+00:00 Europe/London\n+00:00 GMT\n+00:00 UTC\n+01:00 Africa/Algiers\n...\n+13:45 Pacific/Chatham\n+14:00 Pacific/Apia\n+14:00 Pacific/Kiritimati\n```\n',
    'author': 'datadavev',
    'author_email': '605409+datadavev@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datadavev/t',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
