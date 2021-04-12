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
    'version': '0.2.0',
    'description': 'Python utilities to read CZI files and parse metadata through python-bioformats',
    'long_description': '==========\npycziutils\n==========\n\n.. image:: https://github.com/yfukai/pycziutils/actions/workflows/python-test.yml/badge.svg\n        :target: https://github.com/yfukai/pycziutils/actions\n\n.. image:: https://img.shields.io/pypi/v/pycziutils.svg\n        :target: https://pypi.python.org/pypi/pycziutils\n\n.. image:: https://readthedocs.org/projects/pycziutils/badge/?version=latest\n        :target: https://pycziutils.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nPython utilities to read (tiled) CZI files and parse metadata through python-bioformats\n\n\n* Free software: BSD license\n\n* Documentation: https://pycziutils.readthedocs.io.\n\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install pycziutils\n\nFeatures\n--------\n\nA tiny utility module to parse Zeiss CZI files in Python through python-bioformats.\nParse tiled images, organize planes into pandas.DataFrame, parse some hard-to-get metadata.\n\nExample\n-------\n\n.. code-block:: python\n    \n    import pycziutils\n\n\n    @pycziutils.with_javabridge\n    def main():\n        czi_file_path="path/to/czi/file.czi"\n        tiled_czi_ome_xml=pycziutils.get_tiled_omexml_metadata(czi_file_path)\n        tiled_properties_dataframe=pycziutils.parse_planes(tiled_czi_ome_xml)\n\n        print(tiled_properties_dataframe.columns)\n        #Index([\'index\', \'X\', \'Y\', \'Z\', \'T\', \'C_index\', \'T_index\', \'Z_index\', \'image\',\n        #       \'plane\', \'image_acquisition_T\', \'absolute_T\'],\n        #        dtype=\'object\')\n\n        print(tiled_properties_dataframe.iloc[0])\n        #index                                                 0\n        #X                                             -1165.624\n        #Y                                               122.694\n        #Z                                                 0.001\n        #T                                                 1.027\n        #C                                                 Phase\n        #C_index                                               0\n        #T_index                                               0\n        #Z_index                                               0\n        #image                                                 0\n        #plane                                                 0\n        #image_acquisition_T    2021-04-12 02:12:21.340000+00:00\n        #absolute_T             2021-04-12 02:12:22.367000+00:00\n        #Name: 0, dtype: object\n\n        #returns bioformats reader for tiled images\n        reader=pycziutils.get_tiled_reader(czi_file_path) \n        for i, row in tiled_properties_dataframe.iterrows():\n            image = reader.read(\n                series=row["image"],\n                t=row["T_index"],\n                z=row["Z_index"],\n                c=row["C_index"],\n            )\n   \n    if __name__=="__main__":\n        main()\n\nCredits\n-------\n\nThis package uses `python-bioformats`_ as a nice tool to connect CZI files to Python.\n\nThis package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage-poetry`_ project template.\n\nThis package uses pysen_ for linting and formatting. \n\n.. _`python-bioformats`: https://github.com/CellProfiler/python-bioformats\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`wboxx1/cookiecutter-pypackage-poetry`: https://github.com/wboxx1/cookiecutter-pypackage-poetry\n.. _pysen: https://github.com/pfnet/pysen\n',
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
