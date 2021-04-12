# Copyright 2014 Big Switch Networks, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from neutron.tests.unit.db import test_db_base_plugin_v2 as test_plugin

from networking_bigswitch.tests.unit.bigswitch.mock_paths import HTTPCON
from networking_bigswitch.tests.unit.bigswitch.mock_paths import \
    SERVER_REST_CALL
from networking_bigswitch.tests.unit.bigswitch \
    import test_base as bsn_test_base


class CapabilitiesTestsstCase(bsn_test_base.BigSwitchTestBase,
                              test_plugin.NeutronDbPluginV2TestCase):

    def test_keep_alive_capability(self):
        self.skipTest("cached connections are currently disabled because "
                      "their assignment to the servermanager object is not "
                      "thread-safe")
        with mock.patch(
            SERVER_REST_CALL, return_value=(200, None, '["keep-alive"]', None)
        ):
            # perform a task to cause capabilities to be retrieved
            with self.floatingip_with_assoc():
                pass
        # stop default HTTP patch since we need a magicmock
        self.httpPatch.stop()
        # now mock HTTP class instead of REST so we can see headers
        conmock = mock.patch(HTTPCON).start()
        instance = conmock.return_value
        instance.getresponse.return_value.getheader.return_value = 'HASHHEADER'
        with self.network():
            callheaders = instance.request.mock_calls[0][1][3]
            self.assertIn('Connection', callheaders)
            self.assertEqual(callheaders['Connection'], 'keep-alive')
