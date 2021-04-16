# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cree_sro_syllabics']
setup_kwargs = {
    'name': 'cree-sro-syllabics',
    'version': '2021.4.16',
    'description': 'Convert between Western Cree SRO and syllabics',
    'long_description': 'Cree SRO/Syllabics\n==================\n\n[![Build Status](https://travis-ci.org/eddieantonio/cree-sro-syllabics.svg?branch=master)](https://travis-ci.org/eddieantonio/cree-sro-syllabics)\n[![codecov](https://codecov.io/gh/eddieantonio/cree-sro-syllabics/branch/master/graph/badge.svg)](https://codecov.io/gh/eddieantonio/cree-sro-syllabics)\n[![Documentation Status](https://readthedocs.org/projects/crk-orthography/badge/?version=stable)](https://crk-orthography.readthedocs.io/en/stable/?badge=stable)\n[![PyPI package](https://img.shields.io/pypi/v/cree-sro-syllabics.svg)](https://pypi.org/project/cree-sro-syllabics/)\n[![Calver YYYY.MM.DD](https://img.shields.io/badge/calver-YYYY.MM.DD-22bfda.svg)](http://calver.org/)\n\nPython 3 library to convert between Western Cree **standard Roman\nOrthography** (SRO) to **syllabics** and back again!\n\nCan be used for:\n\n - nêhiyawêwin/ᓀᐦᐃᔭᐍᐏᐣ/Cree Y-dialect\n - nīhithawīwin/ᓃᐦᐃᖬᐑᐏᐣ/Cree Th-dialect\n - nēhinawēwin/ᓀᐦᐃᓇᐍᐏᐣ/Cree N-dialect\n\nInstall\n-------\n\nUsing `pip`:\n\n    pip install cree-sro-syllabics\n\nOr, you can copy-paste or download [`cree_sro_syllabics.py`][download] into\nyour own Python 3 project!\n\n[download]: https://github.com/eddieantonio/cree-sro-syllabics/raw/master/cree_sro_syllabics.py\n\n\nUsage\n-----\n\n[Visit the full documentation here][documentation]! Wondering about\nwords like "syllabics", "transliterator", or "orthography"? Visit\n[the glossary][glossary]!\n\n[documentation]: https://crk-orthography.readthedocs.io/en/stable/\n[glossary]: https://crk-orthography.readthedocs.io/en/stable/glossary.html\n\n\nConvert SRO to syllabics:\n\n```python\n>>> from cree_sro_syllabics import sro2syllabics\n>>> sro2syllabics(\'nêhiyawêwin\')\n\'ᓀᐦᔭᐍᐏᐣ\'\n>>> sro2syllabics(\'write nêhiyawêwin\')\n\'write ᓀᐦᐃᔭᐍᐏᐣ\'\n```\n\nConvert syllabics to SRO:\n\n```python\n>>> from cree_sro_syllabics import syllabics2sro\n>>> syllabics2sro(\'ᐊᒋᒧᓯᐢ\')\n\'acimosis\'\n>>> syllabics2sro(\' → ᒪᐢᑫᑯᓯᕽ  ᑎᕒᐁᐩᓬ \')\n\' → maskêkosihk  tireyl \'\n```\n\nSee also\n--------\n\n[nêhiyawêwin syllabics](https://github.com/UAlbertaALTLab/nehiyawewin-syllabics)\n\n\nLicense\n-------\n\nCopyright © 2018–2021 National Research Council Canada.\n\nLicensed under the MIT license.\n',
    'author': 'Eddie Antonio Santos',
    'author_email': 'Eddie.Santos@nrc-cnrc.gc.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eddieantonio/cree-sro-syllabics',
    'py_modules': modules,
}


setup(**setup_kwargs)
