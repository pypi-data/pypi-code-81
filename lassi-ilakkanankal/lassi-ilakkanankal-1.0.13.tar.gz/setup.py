# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'மூலம்'}

packages = \
['லஸ்ஸியிலக்கணங்கள்',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.javascript',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.json',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.lark',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.nearley',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.python',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.python.சோதனைகள்',
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.எழில்']

package_data = \
{'': ['*'],
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.json': ['சோதனைகள்/*'],
 'லஸ்ஸியிலக்கணங்கள்.இலக்கணங்கள்.lark': ['சோதனைகள்/*']}

install_requires = \
['ennikkai>=1.2.5,<2.0.0',
 'lark-parser',
 'nuchabal>=0.0.1,<0.0.2',
 'semantic-version>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'lassi-ilakkanankal',
    'version': '1.0.13',
    'description': 'லஸ்ஸி மென்பொருளுக்காக இலக்கணம் விவரக்குறிப்புகள்',
    'long_description': None,
    'author': 'julienmalard',
    'author_email': 'julien.malard@mail.mcgill.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lassi-samaaj/lassi-ilakkanangal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
