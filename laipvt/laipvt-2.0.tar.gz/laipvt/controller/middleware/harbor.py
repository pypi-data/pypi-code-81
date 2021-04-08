from __future__ import absolute_import
from __future__ import unicode_literals

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.handler.middlewarehandler import HarborConfigHandler
from laipvt.sysutil.util import path_join, ssh_obj, log, status_me
from laipvt.sysutil.template import FileTemplate
from laipvt.model.cmd import ComposeModel


class HarborController(MiddlewareInterface):
    def __init__(self, result: CheckResultHandler, handler: HarborConfigHandler, template: str):
        super(HarborController, self).__init__(result, handler, template)

        self.harbor_conf_tmp = path_join("/tmp", "harbor.yml")
        self.harbor_conf_template = path_join(self.template, "config.tmpl")
        self.harbor_conf_file = path_join(self.base_dir, "harbor.yml")
        self.habor_data = path_join(self.template, "data")
        self._docker_compose_file = path_join(self.base_dir, "docker-compose.yaml")
        self.harbor_cfg = HarborConfigHandler().get_config_with_check_result()
        self.harbor_cfg["harbor"]["log_location"] = path_join(self.base_dir, "var/log/harbor")
        self.harbor_cfg["harbor"]["data_volume"] = path_join(self.base_dir, "data")


    def _generic_config(self):
        log.info("渲染分发 Harbor 安装包及配置文件")
        for num_id in range(len(self.harbor_server)):
            FileTemplate(self.harbor_cfg, self.harbor_conf_template, self.harbor_conf_tmp).fill()
            self.send_config_file(self.harbor_server[num_id], self.template, self.base_dir)
            self.send_config_file(self.harbor_server[num_id], self.harbor_conf_tmp, self.harbor_conf_file)

    def ssh_cli(self):
        for server in self.harbor_server:
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            return ssh_cli

    def _install_harbor(self):
        log.info("安装harbor")
        cmd_list = ["/bin/bash {}".format(path_join(self.base_dir, "install.sh")),
               "tar -zxmf {} -C {}".format(path_join(self.base_dir, "data.tar.gz"), self.base_dir)]
        res_list = self.ssh_cli().run_cmdlist(cmd_list)
        for res in res_list:
            if res["code"] != 0:
                log.error("{} {}".format(res["stdout"], res["stderr"]))
                exit(2)

    def _chmod_data(self):
        cmd_list = ["chown -R 999:999 {} {}".format(path_join(self.base_dir, "data", "database"), path_join(self.base_dir, "data", "redis")),
               "chown -R 10000:10000 {} {}  ".format(path_join(self.base_dir, "data", "secret"), path_join(self.base_dir, "data", "registry"))]
        res_list = self.ssh_cli().run_cmdlist(cmd_list)
        for res in res_list:
            if res["code"] != 0:
                log.error("{} {}".format(res["stdout"], res["stderr"]))
                exit(2)

    def _start(self):
        compose_cmd = ComposeModel(self.docker_compose_file)
        for server in self.harbor_server:
            log.info("启动 %s %s服务" % (server.ipaddress, self.middleware_name))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                res = ssh_cli.run_cmd(compose_cmd.up())
                if res["code"] != 0:
                    log.error("启动 %s: %s服务失败: %s %s" % (
                        server.ipaddress, self.middleware_name,
                        res["stdout"], res["stderr"]
                    ))
                    exit(2)
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def _check(self):
        super().wait_for_service_start()
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            for i in self.harbor_server:
                url = "http://{IP}:{PORT}/api/v2.0/health".format(
                    IP=i.ipaddress, PORT=self.harbor_cfg["harbor"]["http_port"]
                )
                log.info("检查 {}:{} 上的 Harbor 健康性".format(i.ipaddress, self.harbor_cfg["harbor"]["http_port"]))
                result = s.get(url, timeout=5).json()
                if result["status"] == "healthy":
                    log.info("Harbor 服务运行正常")
                else:
                    log.error("{IP} 上的 Harbor 服务异常".format(IP=i.ipaddress))
                    log.error("错误日志: {}".format(result))
                    exit(2)
        except Exception as e:
            log.error(e)
            log.error("{IP} 上的 Harbor 服务异常".format(IP=self.harbor_cfg["harbor"]["ipaddress"]))
            exit(2)

    def _change_password(self):
        log.info("修改 Harbor 登陆密码")
        try:
            url = "http://{IP}:{PORT}/api/v2.0/users/1/password".format(
                IP=self.harbor_cfg["harbor"]["harbor_ipaddress"], PORT=self.harbor_cfg["harbor"]["http_port"])
            headers = {"Content-Type": "application/json"}
            data_dit = {"old_password": "Harbor12345", "new_password": "{}".format(self.harbor_cfg["harbor"]["password"])}
            result = requests.put(url=url, json=data_dit, headers=headers, auth=HTTPBasicAuth('admin', 'Harbor12345'))
            if result:
                log.info("Harbor 密码修改成功")
            else:
                log.error("Harbor 密码修改失败,新密码至少包含1个大写字母、1个小写字母和1个数字")
                log.error(result)
                exit(2)
        except Exception as e:
            log.error(e)
            log.error("Harbor 密码修改失败,请检查Harbor服务是否正常启动或端口是否可达")

    @status_me("basesystem")
    def install_harbor(self):
        self._generic_config()
        self._install_harbor()
        self._chmod_data()
        self._start()
        self._check()
        self._change_password()