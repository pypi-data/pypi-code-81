#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""`3D Fingervein`_ is a database for biometric fingervein recognition

The `3D Fingervein`_ Database for finger vein recognition consists of 13614
images from 141 subjects collected in various acquisition campaigns.

You can download the raw data of the `3D Fingervein`_ database by following
the link.
"""


from bob.extension import rc
from bob.bio.vein.database.fv3d import Database
from bob.bio.base.pipelines.vanilla_biometrics import DatabaseConnector

import logging
logger = logging.getLogger("bob.bio.vein")

# Retrieve directory from config
_fv3d_directory = rc["bob.db.fv3d.directory"]
"""Value in ``~/.bobrc`` for this dataset directory"""

# Set default protocol if not given via a config file
if 'protocol' not in locals():
    logger.info("protocol not specified, using default: 'central'")
    protocol = 'central'

legacy_database = Database(
    original_directory = _fv3d_directory,
    original_extension = '.png',
    protocol = protocol,
)
"""The :py:class:`bob.bio.base.database.BioDatabase` derivative with fv3d
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

Notice that ``original_directory`` is set to ``rc[bob.db.fv3d.directory]``. You
must make sure to set this value with ``bob config set bob.db.fv3d.directory``
to the place where you actually installed the `3D Fingervein`_ dataset, as
explained in the section :ref:`bob.bio.vein.baselines`.
"""

logger.debug(f"Loaded database fv3d config file, using protocol '{protocol}'.")
