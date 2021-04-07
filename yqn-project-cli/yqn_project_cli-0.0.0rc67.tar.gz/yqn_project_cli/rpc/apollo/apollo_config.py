# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/1
import os
import json
import inspect
from yqn_project_cli.rpc.eureka import eureka_client
from yqn_project_cli.rpc.apollo.apollo_client import ApolloClient
from yqn_project_cli.rpc import RPCConfigBase
from yqn_project_cli.utils import host_ip


class ApolloConfig(RPCConfigBase):

    def __init__(self, **kwargs):
        super(ApolloConfig, self).__init__(**kwargs)

        self.apollo_app_id = self.client_config.apollo_app_id
        self.apollo_app_name = self.client_config.apollo_app_name
        self.apollo_cluster = os.environ.get('YQN_APOLLO_CLUSTER', self.client_config.apollo_cluster)
        self.apollo_meta_server_url = os.environ.get('YQN_APOLLO_METADATA', self.client_config.apollo_meta_server_url)
        self.apollo_env = os.environ.get('YQN_APOLLO_ENV', self.client_config.apollo_env)
        self.apollo_namespace = getattr(self.client_config, 'apollo_namespace', 'application')

        self.apollo_eureka_server_key = getattr(self.client_config, 'apollo_eureka_server_key',
                                                'eureka.client.serviceUrl.defaultZone')

        self.apollo_eureka_status_page_url = getattr(self.client_config, 'apollo_eureka_status_page_url',
                                                     self.project_config.heartbeat_url)

        self.apollo_eureka_health_check_url = getattr(self.client_config, 'apollo_eureka_health_check_url',
                                                      self.project_config.heartbeat_url)

        self.apollo_eureka_instance_ip = getattr(self.client_config, 'apollo_eureka_instance_ip',
                                                 os.environ.get('YQN_POD_IP', host_ip()))

        self.apollo_eureka_instance_port = getattr(self.client_config, 'apollo_eureka_instance_port',
                                                   int(self.apollo_app_id))

        self.apollo_cache_file_path = getattr(self.client_config, 'apollo_cache_file_path',
                                              os.path.join(self.project_config.project_base_dir, 'config'))

        self.conf_management = {}
        self.services = {}

    def init_apollo(self):
        apollo_client = ApolloClient(app_id=self.apollo_app_id,
                                     cluster=self.apollo_cluster,
                                     config_server_url=self.apollo_meta_server_url,
                                     env=self.apollo_env,
                                     cache_file_path=self.apollo_cache_file_path)

        if self.project_config is not None and getattr(self.project_config, 'hot_update', False):
            apollo_client.start(lambda: self.manage_servers(apollo_client))  # hot update

        else:
            apollo_client.start(lambda: self.reload(apollo_client))

        self.connector = apollo_client

    def init_eureka(self):
        eureka_server = self.connector.get_value(self.apollo_eureka_server_key, self.connector.get_value('eureka_url'))
        eureka_client.init(eureka_server=eureka_server,
                           app_name=self.apollo_app_name,
                           instance_ip=self.apollo_eureka_instance_ip,
                           instance_port=self.apollo_eureka_instance_port,
                           status_page_url=self.apollo_eureka_status_page_url,
                           health_check_url=self.apollo_eureka_health_check_url)

    def manage_servers(self, apollo_client):
        updated = self.reload(apollo_client)
        if updated:
            for name, server in self.services.items():
                if server is self or not callable(getattr(server, 'reconnect', False)):
                    continue

                # server reconnect depend on certain conf_management attrs
                server.reconnect(**self.conf_management)

    def reload(self, apollo_client):

        # va
        # if 'certain_self_settings_namespace' in apollo_client._cache:
        #     self.conf_management = apollo_client._cache['certain_self_settings_namespace']
        #
        # else:
        #     self.conf_management = apollo_client._cache['application']

        # vb
        updated = False
        if self.conf_management != apollo_client._cache[self.apollo_namespace]:
            self.conf_management = apollo_client._cache[self.apollo_namespace]
            updated = True

        return updated

        # vc
        # for key, value in inspect.getmembers(ApolloConfigMapping):
        #     if not key.startswith('__') and not callable(value):
        #         self.conf_management[key] = apollo_client.get_value(key)

        # vd
        # self.conf_management = dict(
        #
        #     eureka_url=apollo_client.get_value('eureka_url'),
        #
        #     es_host=apollo_client.get_value('es_host'),
        #     es_port=apollo_client.get_value('es_port'),
        #     es_username=apollo_client.get_value('es_username'),
        #     es_password=apollo_client.get_value('es_password'),
        #
        #     mysql_engine=apollo_client.get_value('mysql_engine'),
        #     mysql_username=apollo_client.get_value('mysql_username'),
        #     mysql_password=apollo_client.get_value('mysql_password'),
        #     mysql_host=apollo_client.get_value('mysql_host'),
        #     mysql_port=apollo_client.get_value('mysql_port'),
        #     mysql_charset=apollo_client.get_value('mysql_charset'),
        #     mysql_database=apollo_client.get_value('mysql_database'),
        #     mysql_url=apollo_client.get_value('mysql_url'),
        #
        #     odps_access_id=apollo_client.get_value('odps_access_id'),
        #     odps_secret_access_key=apollo_client.get_value('odps_secret_access_key'),
        #     odps_project=apollo_client.get_value('odps_project'),
        #     odps_endpoint=apollo_client.get_value('odps_endpoint'),
        #
        # )

    def connect(self, **kwargs):
        self.init_apollo()
        self.init_eureka()
        return self.conf_management

    def close(self, **kwargs):
        pass

    def reconnect(self, **kwargs):
        pass
