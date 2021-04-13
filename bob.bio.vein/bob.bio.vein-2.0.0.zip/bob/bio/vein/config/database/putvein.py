#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Mon 26 Sep 2016 17:21:42 CEST

"""`PUT Vein`_ is a database for biometric palm and wrist vein recognition.

PUT Vein pattern database consists of 2400 images presenting human vein patterns.
Half of images (1200 images) contain a palm vein pattern and the remaining images contain a wrist vein pattern (another 1200 images).
Data was acquired from both hands of 50 students. Thus, it has 100 different patterns for palm and wrist region.
Pictures ware taken in 3 series, 4 pictures each, with at least one week interval between each series.
Images in database have 1280x960 resolution and are stored as 24-bit bitmap. Database consist of 2 main splits:
hand and wrist, allowing to investigate both modalities.
The reference citation is [KK10]_.

You can download the raw data of the `PUT Vein`_ database by following
the link.
"""

from bob.extension import rc
from bob.bio.vein.database.putvein import PutveinBioDatabase
from bob.bio.base.pipelines.vanilla_biometrics import DatabaseConnector

import logging
logger = logging.getLogger("bob.bio.vein")

_putvein_directory = rc["bob.db.putvein.directory"]
"""Value in ``~/.bobrc`` for this dataset directory"""

# Set default protocol if not given via a config file
if 'protocol' not in locals():
    logger.info("protocol not specified, using default: 'wrist-LR_1'")
    protocol = 'wrist-LR_1'

legacy_database = PutveinBioDatabase(
    original_directory = _putvein_directory,
    original_extension = '.bmp',
    protocol = protocol,
    )
"""The :py:class:`bob.bio.base.database.BioDatabase` derivative with PUT Vein
database settings
"""

database = DatabaseConnector(
    legacy_database,
    annotation_type=None,
    fixed_positions=None
)

"""
The database interface wrapped for vanilla-biometrics

.. warning::

   This class only provides a programmatic interface to load data in an orderly
   manner, respecting usage protocols. It does **not** contain the raw
   datafiles. You should procure those yourself.

Notice that ``original_directory`` is set to ``rc[bob.db.putvein.directory]``.
You must make sure to set this value with
``bob config set bob.db.putvein.directory`` to the place where you actually
installed the `put vein`_ dataset, as explained in the section
:ref:`bob.bio.vein.baselines`.
"""

logger.debug(f"loaded database putvein config file, using protocol '{protocol}'.")
