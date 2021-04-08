# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
unittest
"""

from os import path
import os
import unittest

from dpt_runtime import Settings

class TestSettings(unittest.TestCase):
    """
Unittest for Settings

:since: v2.1.0
    """

    def test_paths(self):
        """
Tests the calculated paths.
        """

        settings = Settings()

        self.assertTrue(settings.get("path_base")
                        == path.sep.join(path.abspath(__file__).split(path.sep)[:-2])
                       )

        if ("DPT_PATH_DATA" in os.environ and os.access(os.environ['DPT_PATH_DATA'], (os.R_OK | os.X_OK))):
            self.assertTrue(settings.get("path_data") == os.environ['DPT_PATH_DATA'])
        #
    #
#

if (__name__ == "__main__"):
    unittest.main()
#
