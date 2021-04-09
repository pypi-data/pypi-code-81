# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tess_cloud']

package_data = \
{'': ['*'], 'tess_cloud': ['data/*']}

install_requires = \
['aioboto3>=8.2.0',
 'aiohttp>=3.7.4',
 'astropy>=4.2',
 'backoff>=1.10.0',
 'diskcache>=5.2.1',
 'lightkurve>=2.0.7',
 'nest-asyncio>=1.5.1',
 'numpy>=1.19',
 'pyarrow>=3.0.0',
 's3fs>=0.5.2',
 'tess-ephem>=0.2.0',
 'tess-locator>=0.4.0',
 'tqdm>=4.58.0']

setup_kwargs = {
    'name': 'tess-cloud',
    'version': '0.3.0',
    'description': 'Analyze NASA TESS data in the cloud.',
    'long_description': 'tess-cloud\n==========\n\n**Analyze the TESS open dataset in AWS S3.**\n\n|pypi|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/tess-cloud\n                :target: https://pypi.python.org/pypi/tess-cloud\n\n\n`tess-cloud` is a user-friendly package which provides fast access to TESS Full-Frame Image (FFI) data in the cloud.\nIt builds upon `aioboto3 <https://pypi.org/project/aioboto3/>`_,\n`asyncio <https://docs.python.org/3/library/asyncio.html>`_,\nand `diskcache <https://pypi.org/project/diskcache/>`_\nto access the `TESS data set in AWS S3 <https://registry.opendata.aws/tess/>`_\nin a fast, asynchronous, and cached way.\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    python -m pip install tess-cloud\n\n\nExample use\n-----------\n\nRetrieve the AWS S3 location of a TESS image:\n\n.. code-block:: python\n\n    >>> import tess_cloud\n    >>> tess_cloud.get_s3_uri("tess2019199202929-s0014-2-3-0150-s_ffic.fits")\n    "s3://stpubdata/tess/public/ffi/s0014/2019/199/2-3/tess2019199202929-s0014-2-3-0150-s_ffic.fits"\n\n\nList the images of a TESS sector:\n\n.. code-block:: python\n\n    >>> tess_cloud.list_images(sector=5, camera=2, ccd=3)\n    <TessImageList>\n\n\nRead a TESS image from S3 into local memory:\n\n.. code-block:: python\n\n    >>> from tess_cloud import TessImage\n    >>> img = TessImage("tess2019199202929-s0014-2-3-0150-s_ffic.fits")\n    >>> img.read()\n    <astropy.io.fits.HDUList>\n\n\nRead only the header of a TESS image into local memory:\n\n.. code-block:: python\n\n    >>> img.read_header(ext=1)\n    <astropy.io.fits.FitsHeader>\n\n\nCutout a Target Pixel File for a stationary object:\n\n.. code-block:: python\n\n    >>> from tess_cloud import cutout\n    >>> cutout("Alpha Cen", shape=(10, 10))\n    TargetPixelFile("Alpha Cen")\n\n\nCutout a Target Pixel File centered on a moving asteroid:\n\n.. code-block:: python\n\n    >>> from tess_cloud import cutout_asteroid\n    >>> cutout_asteroid("Vesta", start="2019-04-28", stop="2019-06-28)\n    TargetPixelFile("Vesta")\n\n\nDocumentation\n-------------\n\nComing soon!\n\n\nSimilar services\n----------------\n\n`TESScut <https://mast.stsci.edu/tesscut/>`_ is an excellent API service which allows cut outs\nto be obtained for stationary objects.  Tess-cloud provides an alternative implementation of this\nservice by leveraging the TESS public data set on AWS S3.\n\nAt this time tess-cloud is an experiment, we recommend that you keep using TESScut for now!\n',
    'author': 'Geert Barentsen',
    'author_email': 'hello@geert.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SSDataLab/tess-cloud',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
