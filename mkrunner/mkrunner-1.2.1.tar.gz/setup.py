# -*- coding: utf-8 -*-
from setuptools import setup
import io

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()


packages = \
['mkrunner',
 'mkrunner.app',
 'mkrunner.app.routers',
 'mkrunner.builtin',
 'mkrunner.ext',
 'mkrunner.ext.har2case',
 'mkrunner.ext.locust',
 'mkrunner.ext.uploader']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'jinja2>=2.10.3,<3.0.0',
 'jmespath>=0.9.5,<0.10.0',
 'loguru>=0.4.1,<0.5.0',
 'pydantic>=1.4,<2.0',
 'pytest-html>=2.1.1,<3.0.0',
 'pytest>=5.4.2,<6.0.0',
 'pyyaml>=5.1.2,<6.0.0',
 'requests>=2.22.0,<3.0.0',
 'sentry-sdk>=0.14.4,<0.15.0']

extras_require = \
{'allure': ['allure-pytest>=2.8.16,<3.0.0'],
 'locust': ['locust>=1.0.3,<2.0.0'],
 'upload': ['requests-toolbelt>=0.9.1,<0.10.0', 'filetype>=1.0.7,<2.0.0']}

entry_points = \
{'console_scripts': ['har2case = mkrunner.cli:main_har2case_alias',
                     'hmake = mkrunner.cli:main_make_alias',
                     'mkrun = mkrunner.cli:main_hrun_alias',
                     'mkrunner = mkrunner.cli:main',
                     'locusts = mkrunner.ext.locust:main_locusts']}

setup_kwargs = {
    'name': 'mkrunner',
    'version': '1.2.1',
    'description': 'One-stop solution for HTTP(S) testing.',
    'long_description': long_description,
    'author': 'zhushiwei',
    'author_email': '1396516176@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/httprunner/httprunner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
