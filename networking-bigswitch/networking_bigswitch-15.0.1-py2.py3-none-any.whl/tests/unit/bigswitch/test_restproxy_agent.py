# Copyright 2014 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from neutron.tests import base
from oslo_utils import importutils

from networking_bigswitch.plugins.bigswitch import config as pl_config
from networking_bigswitch.tests.unit.bigswitch.mock_paths import AGENT_MOD
from networking_bigswitch.tests.unit.bigswitch.mock_paths import \
    CONSUMER_CREATE
from networking_bigswitch.tests.unit.bigswitch.mock_paths import CONTEXT
from networking_bigswitch.tests.unit.bigswitch.mock_paths import NEUTRON_CFG
from networking_bigswitch.tests.unit.bigswitch.mock_paths import OVS_BRIDGE
from networking_bigswitch.tests.unit.bigswitch.mock_paths import PL_CONFIG
from networking_bigswitch.tests.unit.bigswitch.mock_paths import PLUGIN_API
from networking_bigswitch.tests.unit.bigswitch.mock_paths import SG_AGENT
from networking_bigswitch.tests.unit.bigswitch.mock_paths import SG_RPC


class BaseAgentTestCase(base.BaseTestCase):

    def setUp(self):
        pl_config.register_config()
        super(BaseAgentTestCase, self).setUp()
        self.mod_agent = importutils.import_module(AGENT_MOD)


class TestRestProxyAgentOVS(BaseAgentTestCase):
    def setUp(self):
        super(TestRestProxyAgentOVS, self).setUp()
        self.plapi = mock.patch(PLUGIN_API).start()
        self.ovsbridge_p = mock.patch(OVS_BRIDGE)
        self.ovsbridge = self.ovsbridge_p.start()
        self.context = mock.patch(CONTEXT).start()
        self.rpc = mock.patch(CONSUMER_CREATE).start()
        self.sg_agent = mock.patch(SG_AGENT).start()
        self.sg_rpc = mock.patch(SG_RPC).start()

    def mock_agent(self):
        mock_context = mock.Mock(return_value='abc')
        self.context.get_admin_context_without_session = mock_context
        return self.mod_agent.RestProxyAgent('int-br', 2)

    def mock_port_update(self, **kwargs):
        agent = self.mock_agent()
        agent.port_update(mock.Mock(), **kwargs)

    def test_port_update(self):
        port = {'id': '1', 'security_groups': 'default'}

        with mock.patch.object(self.ovsbridge.return_value,
                               'get_vif_port_by_id',
                               return_value='1') as get_vif:
            self.mock_port_update(port=port)

        get_vif.assert_called_once_with('1')
        self.sg_agent.assert_has_calls([
            mock.call().refresh_firewall()
        ])

    def test_port_update_not_vifport(self):
        port = {'id': '1', 'security_groups': 'default'}

        with mock.patch.object(self.ovsbridge.return_value,
                               'get_vif_port_by_id',
                               return_value=False) as get_vif:
            self.mock_port_update(port=port)

        get_vif.assert_called_once_with('1')
        self.assertFalse(self.sg_agent.return_value.refresh_firewall.called)

    def test_port_update_without_secgroup(self):
        port = {'id': '1'}

        with mock.patch.object(self.ovsbridge.return_value,
                               'get_vif_port_by_id',
                               return_value='1') as get_vif:
            self.mock_port_update(port=port)

        get_vif.assert_called_once_with('1')
        self.assertFalse(self.sg_agent.return_value.refresh_firewall.called)

    def mock_update_ports(self, vif_port_set=None, registered_ports=None):
        vif_port_set = vif_port_set or set()
        registered_ports = registered_ports or set()
        with mock.patch.object(self.ovsbridge.return_value,
                               'get_vif_port_set',
                               return_value=vif_port_set):
            agent = self.mock_agent()
            return agent._update_ports(registered_ports)

    def test_update_ports_unchanged(self):
        self.assertIsNone(self.mock_update_ports())

    def test_update_ports_changed(self):
        vif_port_set = set(['1', '3'])
        registered_ports = set(['1', '2'])
        expected = dict(current=vif_port_set,
                        added=set(['3']),
                        removed=set(['2']))

        actual = self.mock_update_ports(vif_port_set, registered_ports)

        self.assertEqual(expected, actual)

    def mock_process_devices_filter(self, port_info):
        agent = self.mock_agent()
        agent._process_devices_filter(port_info)

    def test_process_devices_filter_add(self):
        port_info = {'added': 1}

        self.mock_process_devices_filter(port_info)

        self.sg_agent.assert_has_calls([
            mock.call().prepare_devices_filter(1)
        ])

    def test_process_devices_filter_remove(self):
        port_info = {'removed': 2}

        self.mock_process_devices_filter(port_info)

        self.sg_agent.assert_has_calls([
            mock.call().remove_devices_filter(2)
        ])

    def test_process_devices_filter_both(self):
        port_info = {'added': 1, 'removed': 2}

        self.mock_process_devices_filter(port_info)

        self.sg_agent.assert_has_calls([
            mock.call().prepare_devices_filter(1),
            mock.call().remove_devices_filter(2)
        ])

    def test_process_devices_filter_none(self):
        port_info = {}

        self.mock_process_devices_filter(port_info)

        self.assertFalse(
            self.sg_agent.return_value.prepare_devices_filter.called)
        self.assertFalse(
            self.sg_agent.return_value.remove_devices_filter.called)


class TestRestProxyAgent(BaseAgentTestCase):
    def mock_main(self):
        cfg_attrs = {'CONF.RESTPROXYAGENT.integration_bridge': 'integ_br',
                     'CONF.RESTPROXYAGENT.polling_interval': 5,
                     'CONF.AGENT.root_helper': 'helper',
                     'CONF.AGENT.report_interval': 60}
        with\
            mock.patch(AGENT_MOD + '.cfg', **cfg_attrs) as mock_conf,\
            mock.patch(AGENT_MOD + '.config.init'),\
            mock.patch(NEUTRON_CFG) as mock_log_conf,\
                mock.patch(PL_CONFIG):
            self.mod_agent.main()

        mock_log_conf.assert_has_calls([
            mock.call(mock_conf),
        ])

    def test_main(self):
        agent_attrs = {'daemon_loop.side_effect': SystemExit(0)}
        with mock.patch(AGENT_MOD + '.RestProxyAgent',
                        **agent_attrs) as mock_agent:
            self.assertRaises(SystemExit, self.mock_main)

        mock_agent.assert_has_calls([
            mock.call('integ_br', 5),
            mock.call().daemon_loop()
        ])
