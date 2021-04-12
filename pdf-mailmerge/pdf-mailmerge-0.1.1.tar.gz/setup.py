# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdf_mailmerge']

package_data = \
{'': ['*'], 'pdf_mailmerge': ['html/*', 'pdfs/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'argparse>=1.4.0,<2.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pdfkit>=0.6.1,<0.7.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'pdf-mailmerge',
    'version': '0.1.1',
    'description': 'easy command line mail merge to pdf',
    'long_description': None,
    'author': 'Joshua',
    'author_email': 'joshua.flies.planes@gmail.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
