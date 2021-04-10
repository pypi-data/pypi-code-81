# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicomtrolley']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0',
 'pydicom>=2.1.2,<3.0.0',
 'pynetdicom>=1.5.6,<2.0.0',
 'requests-futures>=1.0.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dicomtrolley',
    'version': '0.5.1',
    'description': 'Retrieve medical images via WADO, MINT and DICOM-QR',
    'long_description': '# dicomtrolley\n\n[![CI](https://github.com/sjoerdk/dicomtrolley/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/sjoerdk/dicomtrolley/actions/workflows/build.yml?query=branch%3Amaster)\n[![PyPI](https://img.shields.io/pypi/v/dicomtrolley)](https://pypi.org/project/dicomtrolley/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicomtrolley)](https://pypi.org/project/dicomtrolley/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nRetrieve medical images via WADO, MINT and DICOM-QR.\nRequires python 3.7, 3.8 or 3.9\nRepresents images as `pydicom.Dataset` instances.\n\n![A trolley](docs/resources/trolley.png)\n\n## Usage\n\n### Basic example\n\n```python\n# Create a logged-in http session\nsession = VitreaConnection(\n    "https://server/login").log_in(user,password,realm)\n                           \n# Use this session to create a trolley using MINT and WADO\ntrolley = Trolley(searcher=Mint(session, "https://server/mint"),\n                  wado=Wado(session, "https://server/wado"]))\n\n# find some studies (using MINT)\nstudies = trolley.find_studies(MintQuery(patientName=\'B*\'))  \n\n# download the fist one (using WADO)\ntrolley.download(studies[0], output_dir=\'/tmp/trolley\')\n```\n\n### Finding studies\n\n```python\nstudies = trolley.find_studies(MintQuery(patientName=\'B*\'))\n```\n\nQuery parameters can be found in [dicomtrolley.query.Query](dicomtrolley/query.py). Valid include fields (which information gets sent back) can be found in [include_fields.py](dicomtrolley/fields.py):\n\n```python\nstudies = trolley.find_studies_mint(\n    MintQuery(modalitiesInStudy=\'CT*\', \n              patientSex="F", \n              minStudyDate=datetime(year=2015, month=3, day=1),\n              maxStudyDate=datetime(year=2020, month=3, day=1),\n              includeFields=[\'PatientBirthDate\', \'SOPClassesInStudy\']))\n```\n\n### Finding series and instance details\nTo include series and instance level information as well, use the `queryLevel` parameter\n\n```python\nstudies = trolley.find_studies(  # find studies series and instances\n    MintQuery(studyInstanceID=\'B*\', \n              queryLevel=QueryLevels.INSTANCE)\n\na_series = studies.series[0]  # studies now contain series    \nan_instance = a_series.instances[0]  # and series contain instances\n```\n\n### Downloading data\nAny study, series or instance can be downloaded\n```python\nstudies = trolley.find_studies(MintQuery(patientName=\'B*\',\n                                         queryLevel=QueryLevels.INSTANCE))\n\npath = \'/tmp/trolley\'\ntrolley.download(studies, path)                             # all studies\ntrolley.download(studies[0]), path                          # a single study\ntrolley.download(studies[0].series[0], path)                # a single series\ntrolley.download(studies[0].series[0].instances[:3], path)  # first 3 instances\n```\nMore control over download: obtain `pydicom.Dataset` instances directly \n\n```python\nstudies = trolley.find_studies(              # find study including instances\n    Query(PatientID=\'1234\', \n          queryLevel=QueryLevels.INSTANCE)\n\nfor ds in trolley.get_dataset(studies):      # obtain Dataset for each instance\n    ds.save_as(f\'/tmp/{ds.SOPInstanceUID}.dcm\')\n```\n### DICOM-QR\n`Trolley` can use DICOM-QR instead of MINT as a search method\n```python\ndicom_qr = DICOMQR(host,port,aet,aec)\ntrolley = Trolley(searcher=dicom_qr, wado=wado)\n\n# Finding is similar to MINT, but a DICOMQuery is used instead\ntrolley.find_studies(  \n    query=DICOMQuery(PatientName="BAL*",   \n                     minStudyDate=datetime(year=2015, month=3, day=1),\n                     maxStudyDate=datetime(year=2015, month=4, day=1),\n                     includeFields=["PatientBirthDate", "SOPClassesInStudy"],\n                     QueryRetrieveLevel=QueryRetrieveLevels.STUDY)) \n```\n## Examples\n* [search for studies in MINT](examples/search_for_studies_mint.py) \n* [search for studies in DICOM-QR](examples/search_for_studies_dicom_qr.py)\n* [Find and download studies](examples/go_shopping.py)\n\n\n## Caveats\nDicomtrolley has been developed for and tested on a Vitrea Connection 8.2.0.1 system. This claims to\nbe consistent with WADO and MINT 1.2 interfaces, but does not implement all parts of these standards. \n\nCertain query parameter values and restraints might be specific to Vitrea Connection 8.2.0.1. For example,\nthe exact list of DICOM elements that can be returned from a query might be different for different servers.\n',
    'author': 'sjoerdk',
    'author_email': 'sjoerd.kerkstra@radboudumc.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sjoerdk/dicomtrolley',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
