#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tue 27 Sep 2016 16:47:45 CEST

"""`UTFVP`_ is a database for biometric fingervein recognition

The University of Twente Finger Vascular Pattern (UTFVP) Database is made
publically available in order to support and stimulate research efforts in the
area of developing, testing and evaluating algorithms for vascular patter
recognition. The University of Twente, Enschede, The Netherlands (henceforth,
UT) owns copyright of and serves as the source for the UTFVP database, which is
now distributed to any research group approved by the UTFVP principal
investigator. The reference citation is [TV13]_.

You can download the raw data of the `UTFVP`_ database by following the link.

.. include:: links.rst
"""

from bob.extension import rc
from bob.bio.vein.database.utfvp import Database
from bob.bio.base.pipelines.vanilla_biometrics import DatabaseConnector

import logging
logger = logging.getLogger("bob.bio.vein")

_utfvp_directory = rc["bob.db.utfvp.directory"]
"""Value in ``~/.bobrc`` for this dataset directory"""

# Set default protocol if not given via a config file
if 'protocol' not in locals():
    logger.info("protocol not specified, using default: 'nom'")
    protocol = 'nom'

legacy_database = Database(
    original_directory = _utfvp_directory,
    original_extension = '.png',
    protocol = protocol,
    )
"""The :py:class:`bob.bio.base.database.BioDatabase` derivative with UTFVP settings
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

Notice that ``original_directory`` is set to ``rc[bob.db.utfvp.directory]``.
You must make sure to set this value with
``bob config set bob.db.utfvp.directory`` to the place where you actually
installed the `utfvp`_ dataset, as explained in the section
:ref:`bob.bio.vein.baselines`.
"""

logger.debug(f"Loaded database utfvp config file, using protocol '{protocol}'.")
