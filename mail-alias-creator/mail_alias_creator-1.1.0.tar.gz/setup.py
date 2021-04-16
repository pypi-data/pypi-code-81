# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mail_alias_creator', 'mail_alias_creator.entry_processors']

package_data = \
{'': ['*']}

install_requires = \
['ldap3>=2.7,<3.0', 'pyyaml>=5.2,<6.0']

entry_points = \
{'console_scripts': ['mail_alias_creator = mail_alias_creator.main:main']}

setup_kwargs = {
    'name': 'mail-alias-creator',
    'version': '1.1.0',
    'description': 'Set of python scripts to create our mail alias tables from alias definitions',
    'long_description': "# mail_alias_creator\nA python program to create our mail alias tables from alias definitions\n\n## Configuration\nA configuration file is needed to configure this software.\nBy default it looks for `mac.conf` in the current working directory,\nbut this can be changed by the `-c` command line option or the `MAC_CONFIG` environment variable.\n\nThe configuration file is read by python configparser and must adhere to its format.\n\nA typical configuration file looks like this:\n\n```\n[main]\nlogging_conf = logging.conf\nstrict = false\ncheck_syntax_only = false\n\n[LDAP]\nuri = ldaps://myldap.com\nuser_search_base = ou=users,dc=example,dc=com\ngroup_search_base = ou=groups,dc=example,dc=com\nuser_filter = (objectClass=posixUser)\ngroup_filter = (objectClass=posixGroup)\nuser_uid_field = uid\nuser_primary_mail_field = mail\ngroup_id_field = cn\ngroup_membership_field = memberUid\n```\n\nThe `logging_conf` is file path relative to the main configuration file (or absolute). At this path should be a python `logging.conf` compatible logging configuration. This option may be omitted.\n\nThe `strict` flag enables strict checking of the inputs. In this case the program exits with a non-zero exit code when a possible problem with the given files is detected. This option may be omitted, which set's it to false.\n\nThe `check_syntax_only` flag can be used to abort the program after loading the alias files. This option may be omitted, which set's it to false.\n\nIn the LDAP section some more variables then shown are supported.\nFor a complete list and some explanations see [ldap.py](mail_alias_creator/ldap.py).\n\n## Alias defintion format\nAll given files and all files (recursively) in given folders are parsed as yaml files.\n\nEach file must be of the following format:\n```yaml\nmeta:\n  name: <name of the file>\n  description: <description of the file>\naliases:\n  <alias_mail>:\n    description: <description of the alias>\n    entries:\n      - kind: <kind>\n        ...\n      - kind: <kind2>\n        ...\n  <alias_mail2> ...\n  ...\n```\n\n### Alias entry kind\nThe following kinds of alias entries are currently supported.\n\n#### User\nThe user alias kind can be used to allow users to send and receive emails to/from this alias.\n\nKind name: `user`\n\nFormat:\n```yaml\n- kind: user\n  user: <username>\n```\n\n##### Optional attribues\nThe following optional attributes may be added.\n| name | default | description |\n| ---  | --- | --- |\n| `forbidSend` | `False` | Forbid the user to send via this alias.\n| `forbidReceive` | `False` | Don't foward incoming mails to that user.\n\n#### Group\nThe group alias kind can be used to allow a whole group to send and receive emails to/from this alias.\n\nKind name: `group`\n\nFormat:\n```yaml\n- kind: group\n  group: <groupname>\n```\n\n##### Optional attribues\nThe following optional attributes may be added.\n| name | default | description |\n| ---  | --- | --- |\n| `forbidSend` | `False` | Forbid the group to send via this alias.\n| `forbidReceive` | `False` | Don't foward incoming mails to the users of this group.\n\n#### Include alias\nThe include alias kind can be used to include another alias in this alias.\nAs the argument another alias  defined in this repo must be given.\nEvery recipient from that given alias is also forwared incoming mails to this alias.\nEvery sender from that given alias send mails via this alias.\nIf the given address is not an alias defined in this repo there will be an error.\n\nKind name: `include_alias`\n\nFormat:\n```yaml\n- kind: include_alias\n  alias: <alias address>\n```\n\n##### Optional attribues\nThe following optional attributes may be added.\n| name | default | description |\n| ---  | --- | --- |\n| `forbidSend` | `False` | Forbid the members of the given alias to send via this alias.\n| `forbidReceive` | `False` | Don't foward incoming mails to the members of the given alias.\n\n#### External address\nThe external address kind can be used to forward mails to external email addresses.\nSending is not possible for entries with this kind.\n\nKind name: `external_address`\n\nFormat:\n```yaml\n- kind: external_address\n  address: <email address>\n```\n\n##### Optional attribues\nEven though they do not make much sense, the following optional attributes may be added.\n| name | default | description |\n| ---  | --- | --- |\n| `forbidSend` | `False` | Forbid the members of the given alias to send via this alias.\n| `forbidReceive` | `False` | Don't foward incoming mails to the members of the given alias.\n",
    'author': 'Tim Neumann',
    'author_email': 'neumantm@fius.informatik.uni-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stuvusIT/mail_alias_creator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
