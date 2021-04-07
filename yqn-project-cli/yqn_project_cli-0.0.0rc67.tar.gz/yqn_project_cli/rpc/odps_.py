# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/1
from odps import ODPS, options
from yqn_project_cli.rpc import RPCConfigBase
from yqn_project_cli.utils.decorators import time_it
from yqn_project_cli.utils import health_mark, warning_mark


class ODPSClient(RPCConfigBase):

    def __init__(self, **kwargs):
        super(ODPSClient, self).__init__(**kwargs)
        self.odps_access_id = None
        self.odps_secret_access_key = None
        self.odps_project = None
        self.odps_endpoint = None

    def connect(self, **kwargs):
        self.odps_access_id = self.server_manager.get_value('odps_access_id') if self.use_conf_management \
            else self.client_config.odps_access_id

        self.odps_secret_access_key = \
            self.server_manager.get_value('odps_secret_access_key') if self.use_conf_management \
                else self.client_config.odps_secret_access_key

        self.odps_project = self.server_manager.get_value('odps_project') if self.use_conf_management \
            else self.client_config.odps_project

        self.odps_endpoint = self.server_manager.get_value('odps_endpoint') if self.use_conf_management \
            else self.client_config.odps_endpoint

        self.connector = ODPS(self.odps_access_id, self.odps_secret_access_key, self.odps_project, self.odps_endpoint)

        options.tunnel.use_instance_tunnel = True
        options.tunnel.limit_instance_tunnel = False
        options.allow_antique_date = True

    def close(self, **kwargs):
        pass

    def reconnect(self, **kwargs):
        pass

    def __str__(self):
        return self.odps_project

    def check_table_info(self, tb_name):
        tb = self.connector.get_table(tb_name)
        print(tb.schema)

    @time_it
    def execute_sql(self, sql, print_info=False):
        with self.connector.execute_sql(sql).open_reader() as r:

            if print_info:
                print('sql:', sql)

                if r.count:
                    health_mark('count: %s \n %s' % (r.count, r[0]))

                else:
                    warning_mark('None of Match')

            return r
