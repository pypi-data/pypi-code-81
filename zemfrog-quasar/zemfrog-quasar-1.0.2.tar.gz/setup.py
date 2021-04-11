# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zemfrog_quasar']

package_data = \
{'': ['*'], 'zemfrog_quasar': ['templates/quasar/*']}

install_requires = \
['zemfrog-theme>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'zemfrog-quasar',
    'version': '1.0.2',
    'description': 'Quasar Framework Integration',
    'long_description': '# Zemfrog Quasar\n\nQuasar Framework Integration\n\n# Features\n\n* Support vue v2\n* Added Vuex & Vue-Router\n* Integrated with Quasar\n\n\n# Usage\n\nInstall this\n\n```sh\npip install zemfrog-quasar\n```\n\nAdd this to the `ZEMFROG_THEMES` configuration\n\n```python\nZEMFROG_THEMES = ["zemfrog_quasar"]\n```\n\n# Quick Tutorial\n\nIn this theme, several jinja blocks are available, such as:\n\n* `meta` - List of meta tags to include\n* `links` - This is to be included in the head tag as (`link`, `title`, etc)\n* `content` - This is to be included in the main tag (`div#q-app`)\n* `js` - The js script that will be included, after vue, vuex, vue-router & quasar\n* `vuex` - Configuration passed to vuex\n* `vue_router` - Configuration passed to vue-router\n* `vue` - Configuration passed to vue\n\n\n## Layouts\n\nExamples of using layouts:\n\n```html\n{% extends \'quasar/layout.html\' %}\n```\n\n## Links\n\nAn example of using block links, below we add material icons. By default it doesn\'t come with an icon, so you have to add it yourself.\n\n```html\n{% block links %}\n<link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons" rel="stylesheet" type="text/css">\n{% endblock %}\n```\n\n## Content\n\nAn example of using block content:\n\n```html\n{% block content %}\n<q-toolbar class="text-primary">\n    <q-btn flat round dense icon="menu" ></q-btn>\n    <q-toolbar-title>\n    Toolbar\n    </q-toolbar-title>\n    <q-btn flat round dense icon="more_vert" ></q-btn>\n</q-toolbar>\n{% endblock %}\n```\n\n## Vue\n\nExamples of using vue:\n\n```html\n{% block content %}\n<q-toolbar class="text-primary">\n    <q-btn flat round dense icon="menu" @click="active = !active"></q-btn>\n    <q-toolbar-title>\n    Is this active? <{ active }>\n    </q-toolbar-title>\n    <q-btn flat round dense icon="more_vert" ></q-btn>\n</q-toolbar>\n{% endblock %}\n{% block vue %}\ndata() {\n    return {\n        active: false\n    }\n},\n{% endblock %}\n```\n\nIn the example above, there are several explanations. See below:\n\n* We add `data` to vue via the `vue block`\n* We also change the vue delimiter to `<{`, `}>`\n\n# Quasar\n\nIf you use this, you can\'t use the self-closing tag. See here https://quasar.dev/start/umd#usage\n',
    'author': 'Aprila Hijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
