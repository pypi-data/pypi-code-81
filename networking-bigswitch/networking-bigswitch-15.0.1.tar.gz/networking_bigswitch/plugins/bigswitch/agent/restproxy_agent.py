# Copyright 2014 Big Switch Networks, Inc.
# All Rights Reserved.
#
# Copyright 2011 VMware, Inc.
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

import sys
import time

import eventlet
import oslo_messaging

from neutron_lib.agent import topics
from neutron_lib import constants as q_const
from neutron_lib import context as q_context
from oslo_config import cfg
from oslo_log import log
from oslo_service import loopingcall

from networking_bigswitch.plugins.bigswitch import config as pl_config
from networking_bigswitch.plugins.bigswitch.i18n import _LI
from neutron.agent.common import ovs_lib
from neutron.agent import rpc as agent_rpc
from neutron.agent import securitygroups_rpc as sg_rpc
from neutron.api.rpc.handlers import securitygroups_rpc as api_sg_rpc
from neutron.common import config
from neutron.extensions import securitygroup as ext_sg

eventlet.monkey_patch()

LOG = log.getLogger(__name__)


class FilterDeviceIDMixin(sg_rpc.SecurityGroupAgentRpc):
    """Override SecurityGroupAgentRpc methods that call firewall_driver.

    This is to ensure that device ID sent to firewall driver is always without
    any prefixes. Since the firewall_driver adds the prefix regardless of
    whether it already has or not AND when reading local maps/dicts in
    firewall driver, it tries to match the start of device ID _without_ prefix,
    it fails and goes in an inconsistent state when adding and removing
    interfaces and doing firewall operations.

    Hence the name FilterDeviceIDMixin :)

    """

    def prepare_devices_filter(self, device_ids):
        if not device_ids:
            return
        LOG.info(_LI("Preparing filters for devices %r"), device_ids)
        self._apply_port_filter(device_ids)

    def _apply_port_filter(self, device_ids, update_filter=False):
        # use tap as a prefix because ml2 is hard-coded to expect that
        device_ids = [d.replace('qvo', 'tap') for d in device_ids]
        LOG.info(_LI("Applying port filter for devices %r"), device_ids)

        if self.use_enhanced_rpc:
            devices_info = self.plugin_rpc.security_group_info_for_devices(
                self.context, list(device_ids))
            devices = devices_info['devices']
            security_groups = devices_info['security_groups']
            security_group_member_ips = devices_info['sg_member_ips']
        else:
            devices = self.plugin_rpc.security_group_rules_for_devices(
                self.context, list(device_ids))

        with self.firewall.defer_apply():
            if self.use_enhanced_rpc:
                LOG.debug("Update security group information for ports %s",
                          list(devices.keys()))
                self._update_security_group_info(
                    security_groups, security_group_member_ips)
            for device in devices.values():
                # strip off 'tap' prefix from device. all calls to
                # self.firewall i.e. firewall_driver must pass plain device-id
                # without annotations. firewall_driver adds the appropriate
                # prefix
                device['device'] = device['device'].replace('tap', '')
                if update_filter:
                    LOG.debug("Update port filter for %s", device['device'])
                    self.firewall.update_port_filter(device)
                else:
                    LOG.debug("Prepare port filter for %s", device['device'])
                    self.firewall.prepare_port_filter(device)

    def refresh_firewall(self, device_ids=None):
        LOG.info(_LI("Refresh firewall rules"))
        if not device_ids:
            device_ids = self.firewall.ports.keys()
            if not device_ids:
                LOG.info(_LI("No ports here to refresh firewall"))
                return
        self._apply_port_filter(device_ids, update_filter=True)

    def remove_devices_filter(self, device_ids):
        if not device_ids:
            return
        # strip off 'qvo' prefix from device. all calls to
        # self.firewall i.e. firewall_driver must pass plain device-id
        # without annotations. firewall_driver adds the appropriate
        # prefix
        device_ids = [d.replace('qvo', '') for d in device_ids]
        LOG.info(_LI("Remove device filter for %r"), device_ids)
        with self.firewall.defer_apply():
            for device_id in device_ids:
                device = self.firewall.ports.get(device_id)
                if not device:
                    continue
                self.firewall.remove_port_filter(device)


class RestProxyAgent(api_sg_rpc.SecurityGroupAgentRpcCallbackMixin):

    target = oslo_messaging.Target(version='1.1')

    def __init__(self, integ_br, polling_interval):
        super(RestProxyAgent, self).__init__()
        self.polling_interval = polling_interval

        self.int_br = ovs_lib.OVSBridge(integ_br)
        self.agent_type = "OVS Agent"
        self.agent_state = {
            'binary': 'neutron-bsn-agent',
            'host': cfg.CONF.host,
            'topic': q_const.L2_AGENT_TOPIC,
            'configurations': {},
            'agent_type': self.agent_type,
            'start_flag': True}
        self.use_call = True

        self._setup_rpc()
        self.sg_agent = FilterDeviceIDMixin(self.context, self.sg_plugin_rpc)

    def _report_state(self):
        # How many devices are likely used by a VM
        try:
            self.state_rpc.report_state(self.context,
                                        self.agent_state,
                                        self.use_call)
            self.use_call = False
            self.agent_state.pop('start_flag', None)
        except Exception:
            LOG.exception("Failed reporting state!")

    def _setup_rpc(self):
        self.topic = topics.AGENT
        self.plugin_rpc = agent_rpc.PluginApi(topics.PLUGIN)
        self.sg_plugin_rpc = api_sg_rpc.SecurityGroupServerRpcApi(
            topics.PLUGIN)
        self.context = q_context.get_admin_context_without_session()
        self.endpoints = [self]
        consumers = [[topics.PORT, topics.UPDATE],
                     [topics.SECURITY_GROUP, topics.UPDATE]]
        self.connection = agent_rpc.create_consumers(self.endpoints,
                                                     self.topic,
                                                     consumers)
        self.state_rpc = agent_rpc.PluginReportStateAPI(topics.PLUGIN)
        report_interval = cfg.CONF.AGENT.report_interval
        if report_interval:
            heartbeat = loopingcall.FixedIntervalLoopingCall(
                self._report_state)
            heartbeat.start(interval=report_interval)

    def port_update(self, context, **kwargs):
        LOG.debug("Port update received")
        port = kwargs.get('port')
        vif_port = self.int_br.get_vif_port_by_id(port['id'])
        if not vif_port:
            LOG.debug("Port %s is not present on this host.", port['id'])
            return

        LOG.debug("Port %s found. Refreshing firewall.", port['id'])
        if ext_sg.SECURITYGROUPS in port:
            self.sg_agent.refresh_firewall()

    def _update_ports(self, registered_ports):
        ports = self.int_br.get_vif_port_set()
        if ports == registered_ports:
            return
        added = ports - registered_ports
        removed = registered_ports - ports
        return {'current': ports,
                'added': added,
                'removed': removed}

    def _process_devices_filter(self, port_info):
        if 'added' in port_info:
            self.sg_agent.prepare_devices_filter(port_info['added'])
        if 'removed' in port_info:
            self.sg_agent.remove_devices_filter(port_info['removed'])

    def daemon_loop(self):
        ports = set()

        while True:
            start = time.time()
            try:
                port_info = self._update_ports(ports)
                if port_info:
                    LOG.debug("Agent loop has new device")
                    self._process_devices_filter(port_info)
                    ports = port_info['current']
            except Exception:
                LOG.exception("Error in agent event loop")

            elapsed = max(time.time() - start, 0)
            if (elapsed < self.polling_interval):
                time.sleep(self.polling_interval - elapsed)
            else:
                LOG.debug("Loop iteration exceeded interval "
                          "(%(polling_interval)s vs. %(elapsed)s)!",
                          {'polling_interval': self.polling_interval,
                           'elapsed': elapsed})


def main():
    config.init(sys.argv[1:])
    config.setup_logging()
    pl_config.register_config()

    integ_br = cfg.CONF.RESTPROXYAGENT.integration_bridge
    polling_interval = cfg.CONF.RESTPROXYAGENT.polling_interval
    bsnagent = RestProxyAgent(integ_br, polling_interval)
    bsnagent.daemon_loop()
    sys.exit(0)

if __name__ == "__main__":
    main()
