# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jembe']

package_data = \
{'': ['*'],
 'jembe': ['src/js/*',
           'src/js/componentApi/*',
           'src/js/componentApi/directives/*',
           'src/js/componentApi/magic/*',
           'src/js/morphdom/*',
           'static/js/*',
           'templates/*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'lxml>=4.5.2,<5.0.0', 'simplejson>=3.17.2,<4.0.0']

setup_kwargs = {
    'name': 'jembe',
    'version': '0.3.0',
    'description': 'Jembe Web Framework',
    'long_description': 'Jembe Web Framework\n===================\n\nPython Web Framework for modern web applications, build on top of Flask, designed with following goals:\n\n- App is build using custom, reusable, reactive, responsive UI components;\n- Developers can stay focused on "business" logic and write UI logic only for very specific use cases;\n- UI Component is created by extending Python class, with simple API, and writing associated Jinja2 template; \n- Complex UI interactions can be created without or with minimal use of javascript code;\n- There should be no reason to think off, consider or implement logic for:\n    - Handling http request-response cycle\n    - Routing\n    - Handling any "low level" web/http api\n\nOfficial web site https://jembe.io\n\n\nLicense\n-------\n\n\nJembe Web Framework \nCopyright (C) 2021 BlokKod <info@blokkod.me>\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as published\nby the Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.',
    'author': 'Predrag Peranovic',
    'author_email': 'predrag.peranovic@blokkod.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jembe.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
