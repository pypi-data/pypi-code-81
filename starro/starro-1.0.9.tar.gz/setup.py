# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starro']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['coverage = scripts:coverage',
                     'lint = scripts:lint',
                     'security = scripts:security',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'starro',
    'version': '1.0.9',
    'description': 'The package objective is to mischaracterize sensitive data from this through blinding masks using asterisk',
    'long_description': '# STARRO\n\n![Starro](https://raw.githubusercontent.com/marcosborges/starro-python/master/assets/starro.png)\n\n\nStarro is a facilitator to overshadow sensitive information.\n\nIt reduces the brain overload inherent in the Regex complexity, bringing several commands closer to human language.\n\n\n## how to install?\n\n**Pip:**\n```\n    pip install starro\n```\n\n**Poetry:**\n```\n    poetry add starro\n```\n\n---\n\n## how it works?\n\n### Basic usage\n\n```python\nfrom starro import starro\n\npassword = "MyP@ssW0r$"\nprint(starro.password(password))\n#prints:    **********\n\ntoken =  "3hjsdf67kajh8990s5dff0lk5sdfsfhjks8923"\nprint(starro.secret(token))\n#prints:  **************************************\n\nfullname = "Marcos Monteiro Borges"\nprint(starro.name(fullname))\n#prints:    M***** M******* B*****\n\nmail =   "contato@marcosborges.com "\nprint(starro.mail(mail))\n#prints:  c******@marcosborges.com\n\nphone =  "+55 (11) 9999-9999"\nprint(starro.phone(phone)) \n#prints: "+** (**) ****-9999"\n\ncreditcard = "6666-0000-8888-3232"\nprint(starro.creditcard(creditcard))\n#prints: "6666-****-****-3232"\n\ncpf =    "313.789.874-45"\nprint(starro.cpf(cpf))\n#prints: "313.***.***-45"\n\nrg =     "34.275.057-4"\nprint(starro.rg(rg))\n#prints: "34.***.***-4"\n\n# Others examples\nassert starro.complete("1234567890") == "**********"\nassert starro.mask_left("Testing mask left", 3) == "***ting mask left"\nassert starro.mask_right("Testing mask right", 3) == "Testing mask ri***"\nassert starro.fix_left("Testing fix left", 3) == "Tes*************"\nassert starro.fix_right("Testing fix right", 3) == "**************ght"\nassert starro.mask_center(\'completeds\', 5) == \'com*****eds\'\nassert starro.mask_center(\'completeds\', 12) == \'**********\'\nassert starro.fix_center(\'complete\', 4) == \'**mple**\'\nassert starro.fix_center(\'complete\', 12) == \'********\'\n\n\n```\n\n### Decorator usage\n\n```python\nfrom starro.starro import starrofy\n\nclass MyClass:\n\n    @property\n    @starrofy(\'name\')\n    def fullname(self):\n        return self._fullname\n\n\n    @property\n    @starrofy(\'phone\')\n    def phone(self):\n        return self._phone\n\n    \n    @property\n    @starrofy(\'email\')\n    def mail(self):\n        return self._email\n\n    \n    @property\n    @starrofy(\'password\')\n    def password(self):\n        return self._password\n\n\n\nmyClass = MyClass()\n\nmyClass.fullname = "Full Name User"\nmyClass.phone = "+55 11 99999-9999"\nmyClass.cpf = "313.313.313-32"\nmyClass.mail = "contato@marcosborges.com"\nmyClass.creditcard = "2080-1408-0210-3005"\n\n\nprint("fullname:" + myClass.fullname + "\\n")\nprint("phone:" + myClass.phone + "\\n")\nprint("cpf:" + myClass.cpf + "\\n")\nprint("mail:" + myClass.mail + "\\n")\nprint("creditcard:"  + myClass.creditcard + "\\n")\n\n```\n---\n\n## What are the dependencies?\n\n- Core\n    - python = "^3.6"\n        - re\n        - math\n- Develop\n    - pytest = "^6.2.2"\n    - coverage = "^5.5"\n    - pylint = "^2.7.2"\n    - bandit = "^1.7.0"\n    - flake8 = "^3.9.0"\n    - dependency-check = "^0.5.0"\n\n\n---\n\n\n---\n## QualityGate\n\n\n**[SonarCloud](https://sonarcloud.io/dashboard?id=marcosborges_starro-python)** \n\n<p align=center>\n  <img src="https://sonarcloud.io/api/project_badges/quality_gate?project=marcosborges_starro-python" />\n</p>\n\n\n[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=bugs)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python)\n[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=code_smells)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=coverage)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python) [![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=ncloc)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=alert_status)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=security_rating)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python) [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=sqale_index)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python)\n[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=marcosborges_starro-python&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=marcosborges_starro-python)\n\n\n\n\n\n---\n',
    'author': 'Marcos Borges',
    'author_email': 'contato@marcosborges.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcosborges/starro-python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
