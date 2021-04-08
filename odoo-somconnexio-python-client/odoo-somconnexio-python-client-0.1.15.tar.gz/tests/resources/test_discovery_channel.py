from __future__ import unicode_literals  # support both Python2 and 3

import pytest
import unittest2 as unittest

from odoo_somconnexio_python_client.resources.discovery_channel import DiscoveryChannel


class DiscoveryChannelTests(unittest.TestCase):
    @pytest.mark.vcr()
    def test_search(self):
        discovery_channels = DiscoveryChannel.search()

        for dc in discovery_channels:
            self.assertIsInstance(dc, DiscoveryChannel)
