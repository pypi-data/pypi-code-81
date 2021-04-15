'''
osmscigrid
===========

Filter for OpenStreetMap Protobuf data (aka `.pbf` files).

For convenience, the toplevel module :mod:`osm2scigrid_gas` links to the most
relevant classes and functions of this library:

.. autosummary::
    :nosignatures:
'''

import configparser
import os
from configparser import ExtendedInterpolation
from pathlib import Path


import pkg_resources
import os

resource_package = __name__
resource_path = '/'.join(('Setup', 'Setup_OSM.ini'))  # Do not use os.path.join()
template = pkg_resources.resource_string(resource_package, resource_path)

if not os.path.exists(os.path.dirname('Setup/')):
    os.makedirs(os.path.dirname('Setup/'))
    open(resource_path,"wb+").write(template)

if not os.path.exists(os.path.dirname('Data/')):
    os.makedirs(os.path.dirname('Data/'))

if not os.path.exists(os.path.dirname('../../TM_World_Borders/')):
    os.makedirs(os.path.dirname('../../TM_World_Borders/'))

