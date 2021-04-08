# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['numworkshop']
install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'numworkshop',
    'version': '0.1.1',
    'description': 'A python wrapper for the Numworks workshop',
    'long_description': '# Numworks-workshop.py\n\nThis project is a python wrapper for the numworks [workshop](workshop.numworks.com/).\n\n## How to install ?\n\nJust install the pypi package :\n\n## How to use ? \n\n```py\nfrom numWorkshop import Script, Workshop\n \nworkshop = Workshop("email", "password")\n\ntoaster = Script(name="name", description="description", content="print(\'hello-world\')", public=True)\nworkshop.createScript(toaster)\ntoaster.content = "print(\'nsi.xyz\')"\n# since we use the script name to get acess and edit your script, your should use the name parameter \n# of the editScript function, this will update the script at the end of the process and not break script\n# Other parameter are updated throught Script object...\nworkshop.editScript(toaster, name="namev2")\nworkshop.deleteScript(toaster)\n\nscript = workshop.getScript(https://workshop.numworks.com/python/thierry-barry/annuite_constante) # this return a script object\nprint(script)\n```\n\nIf you find a bug or want a new feature you can open an issue.\n\n',
    'author': 'Evann DREUMONT',
    'author_email': '53308142+LeGmask@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://workshop.numworks.com/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
