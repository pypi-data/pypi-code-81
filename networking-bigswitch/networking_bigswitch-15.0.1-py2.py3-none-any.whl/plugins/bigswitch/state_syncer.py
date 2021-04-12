# Copyright 2019 Big Switch Networks, Inc.
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
import copy
from datetime import datetime
from dateutil import parser
from dateutil import tz
import eventlet
import os

from keystoneauth1.identity import v3
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v3 import client as ksclient
from networking_bigswitch.plugins.bigswitch import constants as bsn_consts
from networking_bigswitch.plugins.bigswitch.utils import Util
from novaclient import client as nv_client
from oslo_log import log as logging
import six

if six.PY2:
    import servermanager
else:
    from networking_bigswitch.plugins.bigswitch import servermanager

LOG = logging.getLogger(__name__)


class StateSyncer(object):
    """StateSyncer

    Periodic state syncer for BCF.
    Used to provide additional orchestrator information to BCF for the
    orchestrator integration GUI.
    NOT the same as topo_sync.

    StateSyncer provides network information, along with metadata about a bunch
    of other objects - such as compute nodes available, interface groups,
    VMs running on each compute node, last X errors for the calls to BCF,
    last topo_sync status.
    """

    def __init__(self, ks_auth_dict, nova_auth_dict):
        # typically:
        # username = neutron
        # project_name = service
        # user_domain_name = Default
        # project_domain_name = Default

        # self.ks_auth_dict = ks_auth_dict

        # initialize keystone client
        auth = v3.Password(auth_url=ks_auth_dict['auth_url'],
                           username=ks_auth_dict['username'],
                           password=ks_auth_dict['password'],
                           project_name=ks_auth_dict['project_name'],
                           user_domain_name=ks_auth_dict['user_domain_name'],
                           project_domain_name=ks_auth_dict[
                               'project_domain_name'])
        sess = session.Session(auth=auth)
        self.keystone_client = ksclient.Client(session=sess)

        # initialize nova client
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(
            auth_url=nova_auth_dict['auth_url'],
            username=nova_auth_dict['username'],
            password=nova_auth_dict['password'],
            project_name=nova_auth_dict['project_name'],
            user_domain_name=nova_auth_dict['user_domain_name'],
            project_domain_name=nova_auth_dict['project_domain_name'])
        sess = session.Session(auth=auth)
        self.nova_client = nv_client.Client(bsn_consts.NOVA_CLIENT_VERSION,
                                            session=sess)
        # read the bridge mappings from os-net-config
        # this helps to generate interface group names in case of RH systems
        # if os-net-config is present, attempt to read physnet bridge_mappings
        # from openvswitch_agent.ini
        # this does not change at runtime. so read once at init is good.
        self.bridge_mappings = {}
        if os.path.isfile(bsn_consts.RH_NET_CONF_PATH):
            self.bridge_mappings = Util.read_ovs_bridge_mappings()

        self.bridge_name = None
        if (len(self.bridge_mappings) > 0):
            # if there are many bridge mappings, pick the first one
            # typically, generic RHOSP deployments have a single physnet:bridge
            # mappings. we can handle multiple physnet case later
            # missing info is physnet associated with an interface of a VM.
            # given that, we can utilize multiple bridge info at runtime.
            self.bridge_name = list(self.bridge_mappings.values())[0]

    def periodic_update(self, period=300):
        # get serverpool instance
        self.serverpool = servermanager.ServerPool.get_instance()

        while True:
            current_time = self.get_current_time_with_timezone()
            if self.should_cluster_be_updated(current_time, period):
                self.push_update(current_time)

            eventlet.sleep(period)

    def get_current_time_with_timezone(self):
        return datetime.now().replace(tzinfo=tz.tzlocal())

    def get_bcf_tenant_name(self, tenant_name, tenant_id):
        if self.serverpool.is_unicode_enabled():
            return tenant_id + '.' + self.serverpool.neutron_id
        else:
            # tenant name is already converted
            return tenant_name + '.' + self.serverpool.neutron_id

    def get_bcf_network_name(self, network_name, network_id):
        if self.serverpool.is_unicode_enabled():
            return network_id
        else:
            # network name needs convert in non-unicode mode
            return Util.format_resource_name(network_name)

    def should_cluster_be_updated(self, current_time, interval):
        # Time Format
        # 2018-12-07T16:06:40.993-08:00
        try:
            previous_time_string = \
                self.serverpool.rest_get_osp_cluster_last_update()

            if previous_time_string:
                previous_time = parser.parse(previous_time_string)
                span_in_seconds = (current_time -
                                   previous_time).total_seconds()

                # there is a chance it gets updated close to 1.9* interval
                # normally it gets updated between 1x interval ~ 1.9x interval
                if span_in_seconds < 0.9 * interval:
                    LOG.debug(
                        "Last Update: %s \nCurrent Time: %s \nSkipped "
                        "Update", previous_time_string, str(current_time))
                    return False
            return True
        except Exception as e:
            # if encountered an exception, try to update anyway
            LOG.warning("Failed to GET OSP cluster Last Update Time: " +
                        str(e))
            return True

    def push_update(self, current_time=None):
        """Push current state of OSP to BCF

        Collects the info about various objects from keystone, nova, neutron
        and posts an update to BCF. A typical update has the following
        structure:
        {
            "bridge-mapping": [
                {
                    "bridge-name": "br-ex",
                    "physnet-name": "physnet1"
                }
            ],
            "hypervisor": [
                {
                    "current-workload": 0,
                    "disk-capacity-gb-used": 1,
                    "id": "1",
                    "hostname": "localhost.localdomain",
                    "intf-group-name": "localhost.localdomain_br-ex",
                    "memory-mb": 16383,
                    "memory-mb-used": 1024,
                    "power-state": "up",
                    "status": "enabled",
                    "vcpu-count": 4,
                    "vcpu-count-used": 1
                }
            ],
            "origination": "neutron_123",
            "last-update": "2018-12-07T16:06:40.993600-08:00",
            "tenant-mapping": [
                {
                    "tenant-name": "bsn.neutron",
                    "tenant-display-name": "bsn"
                },
                {
                    "tenant-name": "uuid-something.neutron",
                    "tenant-display-name": "bsn2"
                }
            ],
            "vm": [
                {
                    "hypervisor-hostname": "localhost.localdomain",
                    "interface": [
                        {
                            "ip-address": "172.10.0.17",
                            "ip-alloc-type": "fixed",
                            "mac-address": "fa:16:3e:b7:f9:d8",
                            "network-display-name": "testnet",
                            "version": 4
                        }
                    ],
                    "display-name": "insta1",
                    "id": "1328305e-4a6a-47ac-b7e1-77f22b5c460c",
                    "state": "active",
                    "tenant-name": "11800d76a70d4c9eab24250b274c533d.neutron",
                    "tenant-display-name": "demo"
                }
            ]
        }
        :return: None - it does a REST call to BCF. does not return a value
        """
        try:
            # initialize empty dictionary post data
            post_data = {}

            if not current_time:
                current_time = self.get_current_time_with_timezone()

            # str(time): "2018-12-07 16:06:40.993600-08:00"
            # target: "2018-12-07T16:06:40.993600-08:00"
            # on BCF, last 3 digits of microseconds are truncated
            # "2018-12-07T16:06:40.993600-08:00" will be truncated to
            # "2018-12-07T16:06:40.993-08:00"
            post_data['last-update'] = 'T'.join(str(current_time).split(' '))

            # add tenant list
            keystone_tenants = copy.deepcopy(self.serverpool.keystone_tenants)
            tenant_list = []
            bcf_tenant_name_map = {}
            for tenant in keystone_tenants:
                bcf_tenant_name = self.get_bcf_tenant_name(
                    keystone_tenants[tenant], tenant)
                tenant_list.append({
                    'tenant-name': bcf_tenant_name,
                    'tenant-display-name': keystone_tenants[tenant]
                })
                bcf_tenant_name_map[tenant] = bcf_tenant_name

            post_data['tenant-mapping'] = tenant_list

            # get hypervisors info from nova
            hypervisors = self.nova_client.hypervisors.list()
            hv_list = []
            for hv in hypervisors:
                intf_group_name = (
                    (hv.hypervisor_hostname + '_' + self.bridge_name)
                    if self.bridge_name
                    else hv.hypervisor_hostname)
                hv_list.append({
                    'hostname': hv.hypervisor_hostname,
                    'id': str(hv.id),  # hv id is a number
                    'vcpu-count': hv.vcpus,
                    'vcpu-count-used': hv.vcpus_used,
                    'disk-capacity-gb': hv.local_gb,
                    'disk-capacity-gb-used': hv.local_gb_used,
                    'memory-mb': hv.memory_mb,
                    'memory-mb-used': hv.memory_mb_used,
                    'power-state': hv.state,
                    'status': hv.status,
                    'current-workload': hv.current_workload,
                    'intf-group-name': intf_group_name
                })
            post_data['hypervisor'] = hv_list

            # get VM info from nova
            vms = self.nova_client.servers.list(search_opts={'all_tenants': 1})
            vm_list = []
            for vm in vms:
                # network info needs more parsing
                interfaces = []
                for addr in vm.addresses:
                    for intf in vm.addresses[addr]:
                        interfaces.append({
                            'network-display-name': addr,
                            'mac-address': intf[bsn_consts.INTF_MAC_ADDR],
                            'ip-address': intf[bsn_consts.INTF_IP_ADDR],
                            'ip-alloc-type': intf[bsn_consts.INTF_IP_TYPE],
                            'version': intf[bsn_consts.INTF_IP_VERSION]
                        })

                vm_list.append({
                    'display-name': vm.name,
                    'id': vm.id,
                    # hypervisor hostname is not straightforward object prop
                    'hypervisor-hostname': getattr(
                        vm, bsn_consts.HYPERVISOR_HOSTNAME),
                    'state': getattr(vm, bsn_consts.VM_STATE),
                    'tenant-name': bcf_tenant_name_map[vm.tenant_id],
                    'tenant-display-name': self.serverpool.keystone_tenants[
                        vm.tenant_id],
                    'interface': interfaces
                })

            post_data['vm'] = vm_list

            # physnet info is not available for VMs, but we do have access to
            # bridge mappings in certain environments (RH). pass this info if
            # available
            bridge_mapping_list = []
            for key, value in self.bridge_mappings.items():
                bridge_mapping_list.append({
                    'bridge-name': key,
                    'physnet-name': value})

            post_data['bridge-mapping'] = bridge_mapping_list

            # post to BCF
            LOG.debug('OSP cluster info json sent to CCF is %s', post_data)
            self.serverpool.rest_update_osp_cluster_info(post_data)

        except Exception as e:
            LOG.warning("Failed to PUSH OSP cluster info." + str(e))
