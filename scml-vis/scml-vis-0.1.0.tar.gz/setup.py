# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scml_vis', 'scml_vis.vendor', 'scml_vis.vendor.quick']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0',
 'click-config-file>=0.6.0,<0.7.0',
 'click>=7.1.2,<8.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'streamlit>=0.80.0,<0.81.0',
 'watchdog>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['scml-vis = scml_vis.cli:main',
                     'scmlv = scml_vis.cli:main',
                     'scmlvis = scml_vis.cli:main']}

setup_kwargs = {
    'name': 'scml-vis',
    'version': '0.1.0',
    'description': 'A simple visualiser for SCML worlds and tournaments',
    'long_description': '# scml-vis\n\n[![ci](https://github.com/scml-vis/scml-vis/workflows/ci/badge.svg)](https://github.com/scml-vis/scml-vis/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://scml-vis.github.io/scml-vis/)\n[![pypi version](https://img.shields.io/pypi/v/scml-vis.svg)](https://pypi.org/project/scml-vis/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/scml-vis/community)\n\nA simple visualiser for SCML worlds and tournaments\n\n## Requirements\n\nscml-vis requires Python 3.8 or above.\n\n<details>\n<summary>To install Python 3.8, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.8\npyenv install 3.8.12\n\n# make it available globally\npyenv global system 3.8.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.8 -m pip install scml-vis\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.8 -m pip install --user pipx\n\npipx install --python python3.8 scml-vis\n```\n',
    'author': 'Yasser Mohammad',
    'author_email': 'yasserfarouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scml-vis/scml-vis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
