###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import cPickle
import json

from DIRAC import gLogger


def pickleOrJsonDumps(data, **kwargs):
  """Dump to a string using either JSON or pickle

  FIXME: This is a temporary hack while migrating from pickle to JSON
  """
  try:
    return json.dumps(data)
  except Exception:
    gLogger.exception("Failed to serialise data with JSON", data)
    return cPickle.dumps(data, **kwargs)


def pickleOrJsonLoads(data):
  """Load a string using either JSON or pickle

  FIXME: This is a temporary hack while migrating from pickle to JSON
  """
  try:
    return json.loads(data)
  except Exception:
    return cPickle.loads(data)
