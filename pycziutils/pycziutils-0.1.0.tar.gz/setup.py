# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycziutils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.9,<2.0',
 'pandas>=1.0,<2.0',
 'python-bioformats>=4.0.4,<5.0.0',
 'python-javabridge>=4.0.3,<5.0.0',
 'xmltodict>=0.12,<0.13']

setup_kwargs = {
    'name': 'pycziutils',
    'version': '0.1.0',
    'description': 'Python utilities to read CZI files and parse metadata through python-bioformats',
    'long_description': '==========\npycziutils\n==========\n\n\n.. image:: https://img.shields.io/pypi/v/pycziutils.svg\n        :target: https://pypi.python.org/pypi/pycziutils\n\n.. image:: https://img.shields.io/travis/yfukai/pycziutils.svg\n        :target: https://travis-ci.org/yfukai/pycziutils\n\n.. image:: https://ci.appveyor.com/api/projects/status/yfukai/branch/master?svg=true\n    :target: https://ci.appveyor.com/project/yfukai/pycziutils/branch/master\n    :alt: Build status on Appveyor\n\n.. image:: https://readthedocs.org/projects/pycziutils/badge/?version=latest\n        :target: https://pycziutils.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nPython utilities to read (tiled) CZI files and parse metadata through python-bioformats\n\n\n* Free software: BSD license\n\n* Documentation: https://pycziutils.readthedocs.io.\n\n\nInstallation:\n-------------\n\n.. code-block:: console\n\n    $ pip install pycziutils\n\nFeatures\n--------\n\nA tiny utility module to parse Zeiss CZI files in Python through python-bioformats.\nParse tiled images, organize planes into pandas.DataFrame, parse some hard-to-get metadata.\n\nExample\n-------\n\n.. code-block:: python\n    \n    import pycziutils\n   \n    @with_javabridge\n    def main():\n        tiled_czi_ome_xml=pycziutils.get_tiled_omexml_metadata("path/to/czi/file.czi")\n        tiled_properties_dataframe=pycziutils.parse_planes(tiled_czi_ome_xml)\n        print(tiled_properties_dataframe.columns)\n        #\n        print(tiled_properties_dataframe.iloc[0])\n        #\n\n        reader=pycziutils.get_tiled_czi_reader("path/to/czi/file.czi") #returns bioformats reader for tiled images\n        for i, row in tiled_properties_dataframe.iterrows():\n            image=reader.read(s=row["image"],t=row["T_index"],z=row["Z_index"],c=row["C_index"])\n        \n        bit_depth=pycziutils.get_camera_bits(tiled_czi_ome_xml)\n        # do whatever you like to do with javabridge, with adjusted log level!\n\n    if __name__=="__main__":\n        main()\n\nTODO\n----\n- Generate documentation\n- Writing tests and Github actions\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage-poetry`_ project template.\n\nThis package is using pysen_ for linting and formatting. \n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`wboxx1/cookiecutter-pypackage-poetry`: https://github.com/wboxx1/cookiecutter-pypackage-poetry\n.. _pysen: https://github.com/pfnet/pysen\n',
    'author': 'Yohsuke T. Fukai',
    'author_email': 'ysk@yfukai.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pycziutils.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
