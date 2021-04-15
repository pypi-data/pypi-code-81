# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jailrootdetector']

package_data = \
{'': ['*']}

install_requires = \
['r2pipe>=1.5.3,<2.0.0', 'sh>=1.14.1,<2.0.0']

entry_points = \
{'console_scripts': ['jrd = jailrootdetector.main:main']}

setup_kwargs = {
    'name': 'jailrootdetector',
    'version': '0.1.1',
    'description': 'Identify root and jailbreak detection in mobile applications',
    'long_description': '#+TITLE: jailrootDetector\n\nAttempted automation to detect root and jailbreak detection in mobile applications.\n\n* Example Usage\n\nDetect common detection strings like "jailbroken" and "rooted" as well as a few others. The script leverages [[https://www.radare.org/r/][radare2]] and [[https://sourceware.org/binutils/docs/binutils/strings.html][GNU strings]] to attempt to quickly identify if that application is going to give you a hard time.\n\n** Demo\n\n#+begin_src shell :results output :dir ./jailrootdetector/ :exports both\n  jrd --help\n#+end_src\n\nThe script *does not* extract the IPA or APK, It assums you know how to do that ;) .\n\n#+RESULTS:\n: usage: jrd [-h] (--dex DEX | --ios IOS)\n: \n: [+] root & jailbreak detection\n: \n: optional arguments:\n:   -h, --help  show this help message and exit\n:   --dex DEX   path to android dex file\n:   --ios IOS   path to extracted payload binary\n\nOnce you have an extracted app, then run the script with the relevant option, for example;\n\n#+begin_src shell :results output :dir ./jailrootdetector/ :exports both\n  jrd --ios ./Documents/IPAs/Discord/Payload/Discord.app/Discord\n#+end_src\n\nThen the script will atempt to find hard-coded well known detection strings, frist with [[https://www.radare.org/r/][radare2]] and then falls back to [[https://sourceware.org/binutils/docs/binutils/strings.html][GNU strings]].\n\n#+RESULTS:\n#+begin_example\n[+] "jailbroken" detected in ./Documents/IPAs/Discord/Payload/Discord.app/Discord\n0x100d1be97 11 10 jailbroken\n0x100d1c0dc 13 12 isJailbroken\n0x100d1c0e9 22 21 TB,R,N,V_isJailbroken\n0x100ddcc6b 20 19 computeIsJailbroken\n0x100ddcd0a 13 12 isJailbroken\n0x100ddcd57 14 13 _isJailbroken\n\n\n[+] "/Applications/Cydia.app" detected in ./Documents/IPAs/Discord/Payload/Discord.app/Discord\n/Applications/Cydia.app\n\n\n[+] "/bin/bash" detected in ./Documents/IPAs/Discord/Payload/Discord.app/Discord\n/bin/bash\n\n\n[+] "/bin/sh" detected in ./Documents/IPAs/Discord/Payload/Discord.app/Discord\n/bin/sh\n\n#+end_example\n\n* Installation\n\nYou can install with =pip3=.\n\n#+begin_src shell :results output\n  pip3 install jailrootdetector\n#+end_src\n\nOr you can install with [[https://python-poetry.org/][poetry]]\n\n#+begin_src shell :results output\n  git clone https://gitlab.com/JxTx/jailrootdetector && \\\n    cd jailrootdetector && \\\n    poetry install && \\\n    poetry shell\n    jrd --help\n#+end_src\n\nif all else fails, here is a checklist of dependencies.\n\n - [[https://www.radare.org/r/][radare2]]\n   - Use the [[https://www.radare.org/r/down.html][installation documentation]] for this.\n - [[https://www.radare.org/n/r2pipe.html][r2pipe]]\n   - This can be installed with =pip3 install r2pipe=\n - [[https://pypi.org/project/sh/][sh]]\n   - This can be installed with =pip3 install sh=\n - [[https://sourceware.org/binutils/docs/binutils/strings.html][GNU Strings]]\n   - This should already be installed on your system, if not you should be able to install it with your package manager.\n\n',
    'author': 'JxTx',
    'author_email': 'joethorpe6@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/JxTx/jailrootdetector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
