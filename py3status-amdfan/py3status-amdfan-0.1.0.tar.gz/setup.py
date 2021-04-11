# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py3status_amdfan']

package_data = \
{'': ['*']}

install_requires = \
['amdfan>=0.1.9,<0.2.0', 'py3status>=3.34,<4.0']

entry_points = \
{'py3status': ['module = py3status_amdfan.fan_monitor']}

setup_kwargs = {
    'name': 'py3status-amdfan',
    'version': '0.1.0',
    'description': 'py3status monitor show amdgpu fan speeds and temp',
    'long_description': '# py3status-amdfan\nPython module for monitoring fan RPMs and temperature for `amdgpu` cards in **i3wm** using py3status.\n\n[![Downloads](https://static.pepy.tech/personalized-badge/py3status-amdfan?period=total&units=international_system&left_color=blue&right_color=green&left_text=Downloads)](https://pepy.tech/project/py3status-amdfan)\n\n## Screenshot\n![Status Bar with py3status_amdfan](https://raw.githubusercontent.com/mcgillij/py3status-amdfan/main/images/py3status-amdfan.png)\n\n## Prerequisites\n\n* i3\n* py3status\n* [amdfan](https://github.com/mcgillij/amdfan)\n* poetry (if installing from git)\n\n## Installation\n\n### From Git\n\n``` bash\ngit clone https://github.com/mcgillij/py3status-amdfan.git\ncd py3status-amdfan && poetry install\nmkdir -p ~/.i3/py3status && cd ~/.i3/py3status\nln -s <PATH_TO_CLONED_REPO>/src/py3status_amdfan/fan_monitor.py ./\n```\n\n### With Pip, Pipenv or Poetry\n\n``` bash\npip install py3status-amdfan amdfan\npipenv install py3status-amdfan amdfan\npoetry add py3status-amdfan amdfan && poetry install\n```\n\n### Building Arch package w/PKGBUILD\n\n``` bash\ngit clone https://aur.archlinux.org/py3status-amdfan.git\ncd py3status-amdfan.git\nmakechrootpkg -c -r $HOME/$CHROOT\n```\n\n### Installing built Arch package\n\n``` bash\nsudo pacman -U --asdeps py3status-amdfan-*-any.pkg.tar.zst\n```\n\n## Configuration\n\nNext you will need to add the services you want to monitor, and optionally choose some appropriate emoji\'s.\nYou can also configure actions to open up your browser when you click on the icon, which I find pretty handy.\n\n**~/.config/i3/i3status.conf**\n\n```bash\n...\norder += "fan_monitor"\norder += "clock"\norder += "mail"\n...\n```\n\n## Configuration Options\n\nYou can pass in the following configuration options:\n\n* cache_timeout\n* format\n\n## Restart i3\n\nOnce the package is installed and configured you just need to restart i3.\n',
    'author': 'mcgillij',
    'author_email': 'mcgillivray.jason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcgillij/py3status-amdfan',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
