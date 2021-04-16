from __future__ import absolute_import
from __future__ import unicode_literals

import os
import json
import requests
import time
from minio import Minio
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import path_join, log, status_me, walk_sql_path
from laipvt.model.sql import SqlModule


class CommanderController(ServiceInterface):
    def __init__(self, check_result, service_path):
        super(CommanderController, self).__init__(check_result, service_path)
        self.namespaces = ["rpa", "proxy"]
        self.istio_injection_namespaces = ["rpa", "mid", ]
        self.project = "rpa"

        self.nginx_template = path_join(self.templates_dir, "nginx/http/nginx-commander.tmpl")
        self.nginx_tmp = path_join("/tmp", "nginx-commander.conf")
        self.nginx_file_remote = path_join(self.deploy_dir, "nginx/http/nginx-commander.conf")

    @status_me("commander")
    def init_commander_mysql(self):
        sql_path = self.service_path.sqls
        log.info(sql_path)
        db_info = walk_sql_path(sql_path)
        sql = SqlModule(host=self.middleware_cfg.mysql.ipaddress[0], port=int(self.middleware_cfg.mysql.port),
                        user=self.middleware_cfg.mysql.username, passwd=self.middleware_cfg.mysql.password)
        for db_name, sql_files in db_info.items():
            create_db = "create database If Not Exists {db_name} DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci".format(
                db_name=db_name
            )
            sql.insert_sql(create_db)
            sql.import_from_dir(db_name, path_join(sql_path, db_name))
            #sql.use_db(db_name)
            #for sql_file in sql_files:
            #    sql.import_from_file_commander(sql_file, file_eof=";")

    @status_me("commander")
    def push_commander_images(self):
        self.push_images(self.project)

    def start_service(self, project, version):
        self._send_file(src=self.service_path.charts, dest=self.service_charts_remote)
        for service, processes in self.service_path.config.services.items():
            for process in processes:
                log.info("{}开始部署".format(process))

                check_cmd = "helm --host=localhost:44134 list --all --chart-name {}|grep -q '{}'".format(
                    process, process
                )
                check_results = self._exec_command_to_host(cmd=check_cmd, server=self.servers[0], check_res=False)
                if check_results["code"] == 0:
                    log.warning("{} helm部署记录中已经存在，不做更新，如需要更新，可以先行删除".format(process))

                else:
                    self._create_logs_dir(service)
                    file_path = os.path.join(self.service_charts_remote, process)
                    # print(file_path)
                    config_server = "\,".join(
                        [
                            "{}:{},serviceName=mymaster,allowAdmin=true".format(
                                server, self.middleware_cfg["redis"]["port_sentinel"]
                            ) for server in self.middleware_servers.get_role_ip("master")
                        ]
                    )
                    cmd = """helm --host=localhost:44134 install --name={process} --set replicaCount={replicas} \
                    --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
                    --set pvtWorkDir={pvt_work_dir} \
                    --set config.server="{config_server}" --set config.passwd={config_server_passwd} \
                    --set mysql.host={mysql_host} --set mysql.port={mysql_port} --set mysql.user={mysql_user} \
                    --set mysql.password={mysql_password} --set mysql.database={mysql_database} --set mysql.charset={mysql_charset} \
                    --set oidc.authority={oidc_authority} --set oidc.secret={oidc_secret} \
                    --set global.LM_CLIENT_SERVICE_ID=200001 --set global.LM_CLIENT_LICENSE_MANAGER_ADDR=dns:///license-manager.mid:19080 \
                    {file_path}""".format(
                        process=process, replicas=self.replicas,
                        registry_hub=path_join(self.registry_hub, project),
                        image_name=process, image_tag=version,
                        pvt_work_dir=self.deploy_dir,
                        config_server=config_server,
                        config_server_passwd=self.middleware_cfg["redis"]["password"],
                        mysql_host="mysql.default.svc", mysql_port=6033, mysql_user=self.middleware_cfg["mysql"]["username"],
                        mysql_password=self.middleware_cfg["mysql"]["password"],
                        etcd_endpoint=self.etcd_endpoint, mysql_database="uibot_global",
                        mysql_charset="utf8mb4",
                        oidc_authority="http://{}:{}".format(self.middleware_cfg["identity"]["lb"], self.middleware_cfg["identity"]["nginx_proxy_port"]),
                        oidc_secret="laiye",
                        file_path=file_path)

                    self._exec_command_to_host(cmd=cmd, server=self.servers[0])

    @status_me("commander")
    def start_commander_service(self):
        self.start_service(project=self.project, version=self.private_deploy_version)

    @status_me("commander")
    def commander_proxy_on_nginx(self):
        self.proxy_on_nginx(self.nginx_template, self.nginx_tmp, self.nginx_file_remote)

    @status_me("commander")
    def create_namespace(self):
        self._create_namespace(
            namespaces=self.namespaces,
            istio_injection_namespaces=self.istio_injection_namespaces
        )

    @status_me("commander")
    def init_minio_data(self):
        for bucket in self.service_info.buckets:
            try:
                if self.middleware_cfg.minio.is_deploy:
                    endpoint = "{}:{}".format(self.middleware_cfg.minio.lb, self.middleware_cfg.minio.nginx_proxy_port)
                else:
                    endpoint = "{}:{}".format(self.middleware_cfg.minio.ipaddress[0], self.middleware_cfg.minio.port)
                cli = Minio(
                    endpoint,
                    self.middleware_cfg.minio.username,
                    self.middleware_cfg.minio.password,
                    secure=False
                )
                if not cli.bucket_exists(bucket):
                    cli.make_bucket(bucket)
                    policy_read_only = {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": [
                                    "s3:GetObject"
                                ],
                                "Effect": "Allow",
                                "Principal": "*",
                                "Resource": [
                                    "arn:aws:s3:::{}/*".format(bucket)
                                ],
                                "Sid": ""
                            }
                        ]
                    }
                    cli.set_bucket_policy(bucket, json.dumps(policy_read_only))

            except Exception as e:
                log.error("Minio初始化数据失败:{}".format(e))
                exit(2)

    def login_tenant(self):
        log.info("登录租户管理平台")
        data = {'userName': 'admin', 'password': '123456'}
        login_url = "http://{host}:{port}/api/global/account/webLogin".format(
            host=self.middleware_cfg.nginx.lb, port=self.middleware_cfg.nginx.commander_tenant_port
        )
        response = requests.post(login_url, json=data)
        auth_cookie = ''
        # print(response)
        ret = response.json()
        if ret['code'] == 0:
            cookies = response.cookies
            auth_cookie = {'GlobalUser': cookies.get('GlobalUser', None)}
            # f"GlobalUser={cookies.get('GlobalUser', None)}"
            log.info(auth_cookie)
            log.info("Login succeed")
            return auth_cookie
        else:
            log.error("Login error!")
            exit(2)

    def tenant_init_mysql(self, auth_cookie):
        log.info("租户平台配置MySql数据库")
        db_mysql = {
            "name": "mysql-1",
            "host": "mysql.default.svc",
            "port": 6033,
            "dbName": "uibot_rpa",
            "userName": self.middleware_cfg.mysql.username,
            "password": self.middleware_cfg.mysql.password,
            "type": "10"
        }
        mysql_url = "http://{host}:{port}/api/global/database/create".format(
            host=self.middleware_cfg.nginx.lb, port=self.middleware_cfg.nginx.commander_tenant_port
        )
        resp1 = requests.post(mysql_url, json=db_mysql, cookies=auth_cookie)
        json_resp1 = resp1.json()
        if json_resp1['code'] == 0:
            log.info("配置MySQL数据库完成")
        else:
            log.error("配置MySQL数据库失败")
            exit(2)

    @status_me("commander")
    def init_tenant(self):
        counter = 0
        succeed = False
        # 重试 10 次，如果还是不成功就报错
        while not succeed and counter < 100:
            time.sleep(5)
            try:
                auth_cookie = self.login_tenant()
                self.tenant_init_mysql(auth_cookie=auth_cookie)
                succeed = True

            except Exception as e:
                # log.error(e)
                succeed = False
                counter += 1
        if not succeed:
            log.error("登录租户系统失败，请检查容器是否启动。")
            exit(2)

    def run(self):
        self.init_commander_mysql()
        self.init_rabbitmq()
        self.init_minio_data()
        self.init_redis()
        self.create_namespace()
        self.push_commander_images()
        self.deploy_istio()
        self.start_commander_service()
        self.commander_proxy_on_nginx()
        self.init_tenant()
