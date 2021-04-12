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
from neutron.conf.plugins.ml2 import config as ml2_config
from neutron.plugins.ml2.drivers import type_vlan as vlan_config
from neutron.tests.unit.api import test_extensions
from neutron.tests.unit.db import test_db_base_plugin_v2
from neutron.tests.unit.extensions import test_securitygroup as test_sg
from neutron.tests.unit.plugins.ml2 import test_plugin
from neutron_lib.api.definitions import portbindings
from neutron_lib import context as neutron_context
from neutron_lib.plugins import directory
from oslo_serialization import jsonutils
from oslo_utils import uuidutils

from networking_bigswitch.plugins.bigswitch import servermanager
from networking_bigswitch.tests.unit.bigswitch.fake_server \
    import HTTPResponseMock
from networking_bigswitch.tests.unit.bigswitch.mock_paths import DRIVER
from networking_bigswitch.tests.unit.bigswitch.mock_paths import HTTPCON
from networking_bigswitch.tests.unit.bigswitch.mock_paths import SERVER_POOL
import networking_bigswitch.tests.unit.bigswitch.test_restproxy_plugin as trp

_uuid = uuidutils.generate_uuid

PHYS_NET = 'physnet1'
VLAN_START = 1000
VLAN_END = 1100


class TestBigSwitchMechDriverBase(trp.BigSwitchProxyPluginV2TestCase):

    def setUp(self, plugin=None, service_plugins=None, ext_mgr=None):
        # Configure the ML2 mechanism drivers and network types
        ml2_opts = {
            'mechanism_drivers': ['bsn_ml2'],
            'tenant_network_types': ['vlan'],
        }
        for opt, val in ml2_opts.items():
                ml2_config.cfg.CONF.set_override(opt, val, 'ml2')

        # Configure the ML2 VLAN parameters
        phys_vrange = ':'.join([PHYS_NET, str(VLAN_START), str(VLAN_END)])
        vlan_config.cfg.CONF.set_override('network_vlan_ranges',
                                          [phys_vrange],
                                          'ml2_type_vlan')
        super(TestBigSwitchMechDriverBase,
              self).setUp(test_plugin.PLUGIN_NAME,
                          service_plugins=service_plugins,
                          ext_mgr=ext_mgr)


class TestBigSwitchMechDriverNetworksV2(test_db_base_plugin_v2.TestNetworksV2,
                                        TestBigSwitchMechDriverBase):
    def setUp(self, plugin=None, service_plugins=None, ext_mgr=None):
        TestBigSwitchMechDriverBase.setUp(self,
                                          plugin=plugin,
                                          service_plugins=service_plugins,
                                          ext_mgr=ext_mgr)

    def test_create_network(self):
        name = 'net1'
        keys = [('subnets', []), ('name', name), ('admin_state_up', True),
                ('status', self.net_create_status), ('shared', False)]

        with mock.patch(HTTPCON) as conmock:
            rv = conmock.return_value
            rv.getresponse.return_value = HTTPResponseMock(None)
            with self.network(name=name) as net:
                # for debug
                print(rv.request.mock_calls)

                # remove topo sync call
                filtered_calls = \
                    list(filter(lambda call: "topology" not in call[1][1],
                                rv.request.mock_calls))

                network = jsonutils.loads(filtered_calls[0][1][2])
                self.assertIn('tenant_name', network['network'])
                self.assertEqual('tenant_name',
                                 network['network']['tenant_name'])
                for k, v in keys:
                    self.assertEqual(net['network'][k], v)

    def test_update_network(self):
        with self.network() as network:
            data = {'network': {'name': 'a_brand_new_name'}}
            req = self.new_update_request('networks',
                                          data,
                                          network['network']['id'])
            res = self.deserialize(self.fmt, req.get_response(self.api))
            self.assertTrue('NeutronError' in res)
            self.assertEqual('NetworkNameChangeError',
                             res['NeutronError']['type'])


class TestBigSwitchML2SubnetsV2(test_db_base_plugin_v2.TestSubnetsV2,
                                TestBigSwitchMechDriverBase):
    pass


class TestBigSwitchML2SecurityGroups(test_sg.TestSecurityGroups,
                                     TestBigSwitchMechDriverBase):
    def setUp(self):
        ext_mgr = test_sg.SecurityGroupTestExtensionManager()
        super(TestBigSwitchML2SecurityGroups, self).setUp(ext_mgr=ext_mgr)
        self.ext_api = test_extensions.setup_extensions_middleware(ext_mgr)


class TestBigSwitchMechDriverPortsV2(test_db_base_plugin_v2.TestPortsV2,
                                     TestBigSwitchMechDriverBase):

    VIF_TYPE = portbindings.VIF_TYPE_OVS

    def setUp(self):
        super(TestBigSwitchMechDriverPortsV2, self).setUp()
        self.port_create_status = 'DOWN'

    def test_update_port_status_build(self):
        with self.port() as port:
            self.assertEqual(port['port']['status'], 'DOWN')
            self.assertEqual(self.port_create_status, 'DOWN')

    def test_dont_bind_vnic_type_direct(self):
        host_arg = {portbindings.HOST_ID: 'hostname',
                    portbindings.VNIC_TYPE: portbindings.VNIC_DIRECT}
        with\
            mock.patch(SERVER_POOL + '.rest_get_switch',
                       return_value=True) as rmock,\
            self.port(arg_list=(portbindings.HOST_ID, portbindings.VNIC_TYPE),
                      **host_arg):

            # bind_port() shall ignore this call
            rmock.assert_not_called()

    def test_dont_bind_vnic_type_direct_physical(self):
        host_arg = {portbindings.HOST_ID: 'hostname',
                    portbindings.VNIC_TYPE: portbindings.VNIC_DIRECT_PHYSICAL}
        with\
            mock.patch(SERVER_POOL + '.rest_get_switch',
                       return_value=True) as rmock,\
            self.port(arg_list=(portbindings.HOST_ID, portbindings.VNIC_TYPE),
                      **host_arg):

            # bind_port() shall ignore this call
            rmock.assert_not_called()

    def test_create404_triggers_background_sync(self):
        # allow the async background thread to run for this test
        self.spawn_p.stop()
        with\
            mock.patch(
                SERVER_POOL + '.rest_create_port',
                side_effect=servermanager.RemoteRestError(
                    reason=servermanager.NXNETWORK, status=404)),\
            mock.patch(DRIVER + '._send_all_data') as mock_send_all,\
            self.port(**{'device_id': 'devid', 'binding:host_id': 'host',
                         'arg_list': ('binding:host_id',)}) as p:

            # wait for thread to finish
            mm = directory.get_plugin().mechanism_manager
            bigdriver = mm.mech_drivers['bsn_ml2'].obj
            bigdriver.evpool.waitall()
            mock_send_all.assert_has_calls([
                mock.call(
                    timeout=None,
                    triggered_by_tenant=p['port']['tenant_id']
                )
            ])
        self.spawn_p.start()

    def test_udpate404_triggers_background_sync(self):
        with mock.patch(DRIVER + '.async_port_create',
                        side_effect=servermanager.RemoteRestError(
                            reason=servermanager.NXNETWORK,
                            status=404)),\
                mock.patch(DRIVER + '._send_all_data') as mock_send_all,\
                self.port() as p:

            plugin = directory.get_plugin()
            context = neutron_context.get_admin_context()
            plugin.update_port(context, p['port']['id'],
                               {'port': {'device_id': 'devid',
                                         'binding:host_id': 'host'}})
            mock_send_all.assert_has_calls([
                mock.call(
                    timeout=None,
                    triggered_by_tenant=p['port']['tenant_id']
                )
            ])

    def test_backend_request_contents(self):
        with\
            mock.patch(SERVER_POOL + '.rest_create_port') as mock_rest,\
            self.port(**{'device_id': 'devid', 'binding:host_id': 'host',
                         'arg_list': ('binding:host_id',)}):

            # make sure basic expected keys are present in the port body
            pb = mock_rest.mock_calls[0][1][2]
            self.assertEqual('host', pb['binding:host_id'])
            self.assertIn('bound_segment', pb)
            self.assertIn('network', pb)
