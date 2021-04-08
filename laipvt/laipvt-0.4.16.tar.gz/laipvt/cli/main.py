#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import json
from laipvt.sysutil.args import Args
from laipvt.sysutil.gvalue import CHECK_FILE, PROJECT_INFO_FILE
from laipvt.sysutil.util import find
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.handler.packagehandler import DeployPackageHandler
from laipvt.controller.kubernetes.kube import KubeController
from laipvt.controller.middleware.harbor import HarborController
from laipvt.controller.middleware.nginx import NginxController
from laipvt.controller.middleware.etcd import EtcdController
from laipvt.controller.middleware.minio import MinioController
from laipvt.controller.middleware.redis import RedisController
from laipvt.controller.middleware.mysql import MysqlController
from laipvt.controller.middleware.elasticsearch import EsController
from laipvt.controller.middleware.rabbitmq import RabbitmqController
from laipvt.controller.middleware.identity import IdentityController
from laipvt.controller.middleware.siber import SiberController
from laipvt.controller.service.license import LicenseController
from laipvt.controller.service.mage import MageController
from laipvt.controller.service.ocr_standard import OcrStandardController
from laipvt.controller.service.nlp import NlpController
from laipvt.controller.service.captcha import CaptchaController
from laipvt.controller.service.commander import CommanderController
from laipvt.controller.service.ocr import OcrController
from laipvt.handler.middlewarehandler import EtcdConfigHandler, MysqlConfigHandler, EsConfigHandler, \
    MinioConfigHandler, RabbitmqConfigHandler, RedisConfigHandler, HarborConfigHandler, NginxConfigHandler, \
    IdentityConfigHandler, SiberConfigHandler, OcrConfigHandler
from laipvt.sysutil.relation import module_require_tfserver, tfserver_name, tfserver_image_name
from laipvt.sysutil.util import write_to_file, read_form_json_file
from laipvt.sysutil.kube_common import wait_pod_running

def main():
    args = Args().parse_args()
    # 获取前置检查结果
    check_result_file = CHECK_FILE
    check_result = CheckResultHandler(check_result_file)

    if args.targzFile:

        pkg_path = False
        if not os.path.exists(args.targzFile):
            cwd = [os.getcwd(), check_result.deploy_dir]
            for d in cwd:
                pkg_path = find(d, args.targzFile, file=True)
                if pkg_path:
                    break
        else:
            pkg_path = os.path.join(os.getcwd(), args.targzFile)
        if not pkg_path:
            print("未找到文件")
            exit(1)
        PKG = os.path.dirname(pkg_path)
        ID = os.path.basename(pkg_path).split(".")[0]
        # 将项目ID和path写入文件缓存
        project_dict = { "PKG": PKG, "ID": ID }
        write_to_file(PROJECT_INFO_FILE, json.dumps(project_dict, indent=4))

        deploy_package = DeployPackageHandler(PKG, ID)
        deploy_package.unpack()
        # 解析大包
        parse_package = deploy_package.parse()

        kubernetes_package = parse_package.kubernetes
        kubernetes_package.kubernetes_unpack()

        middleware_package = parse_package.middleware
        middleware_package.unpack()

        harbor_package = parse_package.harbor
        harbor_package.unpack()

        # install harbor
        haror_path = harbor_package.parse().harbor
        harbor_config = HarborConfigHandler()
        harbor = HarborController(check_result, harbor_config, haror_path)
        harbor.install_harbor()

        # install nginx
        nginx_package = middleware_package.parse().nginx
        nginx_config = NginxConfigHandler()
        nginx = NginxController(check_result, nginx_config, nginx_package)
        nginx.install_nginx()

        # add hosts
        kube_info = kubernetes_package.parse()
        kube = KubeController(check_result, kube_info)
        kube.add_hosts()

        # install rpms
        # kube.install_rpms()

        # system prepare
        kube.system_prepare()

        # init primary master
        kube.init_primary_master()
        kube.kube_completion()
        kube.install_network_plugin()

        # join master
        kube.join_master()

        # join node
        kube.join_node()

        # install helm
        kube.install_helm()

        # install istio
        kube.install_istio()

        # 拷贝config
        kube.cp_kube_config()

        # 更新nginx tcp代理apiserever cluster
        nginx.renew_apiserver_config()
        #####################################
        # install etcd
        etcd_path = middleware_package.parse().etcd
        etcd_config = EtcdConfigHandler()
        etcd = EtcdController(check_result, etcd_config, etcd_path)
        etcd.deploy_etcd()

        # install license
        license_package = parse_package.license
        license_package.unpack()
        license_path = license_package.parse()
        license = LicenseController(check_result, license_path)
        license.deploy_license()

        #####################################
        # install minio
        minio_path = middleware_package.parse().minio
        minio_config = MinioConfigHandler()
        minio = MinioController(check_result, minio_config, minio_path)
        minio.deploy_minio()

        # install redis
        redis_path = middleware_package.parse().redis
        redis_config = RedisConfigHandler()
        redis = RedisController(check_result, redis_config, redis_path)
        redis.deploy_redis()

        # install mysql
        mysql_path = middleware_package.parse().mysql
        mysql_config = MysqlConfigHandler()
        mysql = MysqlController(check_result, mysql_config, mysql_path)
        mysql.deploy_mysql()

        # install es
        es_path = middleware_package.parse().elasticsearch
        es_config = EsConfigHandler()
        es = EsController(check_result, es_config, es_path)
        es.deploy_es()

        # install rabbitmq
        rabbitmq_path = middleware_package.parse().rabbitmq
        rabbitmq_config = RabbitmqConfigHandler()
        rabbitmq = RabbitmqController(check_result, rabbitmq_config, rabbitmq_path)
        rabbitmq.deploy_rabbitmq()

        # install identity
        identity_path = middleware_package.parse().identity
        identity_config = IdentityConfigHandler()
        identity = IdentityController(check_result, identity_config, identity_path)
        identity.deploy_identity()

        #####################################
        # install service
        mysql_path = middleware_package.parse().mysql
        mysql_config = MysqlConfigHandler()
        mysql = MysqlController(check_result, mysql_config, mysql_path)

        services = {
            "mage": MageController,
            "commander": CommanderController,
            "nlp": NlpController,
            "captcha": CaptchaController,
            "ocr_standard": OcrStandardController,
            "ocr": OcrController
        }

        for s in parse_package.service:
            s.unpack()
            service_path = s.parse()

            if s.project_name == "ocr":
                ocr_handler = OcrConfigHandler()
                deploy_service = services[s.project_name](service_path, check_result, ocr_handler, s.root_dir)
            else:
                deploy_service = services[s.project_name](check_result, service_path)
            if s.project_name == "commander":
                identity.update_identity_config()
            deploy_service.run()

            # tf-server
            if s.project_name in module_require_tfserver:
                for module_name in tfserver_name[s.project_name]:
                    deploy_service.deploy_tf_service(module_name, tfserver_image_name[s.project_name])

        # check all pod status
        if not wait_pod_running:
            print("kubernetes集群中有pod启动状态异常，请检查: kubectl get pod -A")
            exit(2)

        # install siber
        siber_path = middleware_package.parse().siber
        siber_config = SiberConfigHandler()
        siber = SiberController(check_result, siber_config, siber_path)
        siber.deploy_siber()
        for s in parse_package.service:
            if s.project_name == "mage":
                siber.replace_mage_collection_tag(parse_package.config.siber_tags)
            elif s.project_name == "commander":
                exit()

    if args.which == "license":
        if args.LicenseFile:
            if os.path.exists(args.LicenseFile):
                # print(args.LicenseFile)
                project_dict = read_form_json_file(PROJECT_INFO_FILE)

                # 解析大包
                deploy_package = DeployPackageHandler(project_dict["PKG"], project_dict["ID"])
                parse_package = deploy_package.parse()
                license_package = parse_package.license
                # license_package.unpack()
                license_path = license_package.parse()
                license = LicenseController(check_result, license_path)
                license.renew_license(license_file=args.LicenseFile)
            else:
                print("请检查指定的新授权文件是否存在: {}".format(args.LicenseFile))
                exit(1)

        if args.OcrLicenseFile:
            if os.path.exists(args.OcrLicenseFile):
                project_dict = read_form_json_file(PROJECT_INFO_FILE)

                deploy_package = DeployPackageHandler(project_dict["PKG"], project_dict["ID"])
                parse_package = deploy_package.parse()
                renew_flag = False
                for s in parse_package.service:
                    if s.project_name == "ocr":
                        service_path = s.parse()
                        ocr_handler = OcrConfigHandler()
                        deploy_ocr = OcrController(service_path, check_result, ocr_handler, s.root_dir)
                        deploy_ocr.renew_license(license_file=args.OcrLicenseFile)
                        renew_flag = True

                if not renew_flag:
                    print("OCR license未更新成功，请检查是否存在合合服务")
                    exit(2)

# if __name__ == '__main__':
#     args = Args().parse_args()
#     main(args)
