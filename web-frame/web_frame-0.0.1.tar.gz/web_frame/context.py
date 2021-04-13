import base64
import logging
import rsa

# 加载handler name列表
dynamic_handler_names = []

# 产业字典 { name -> code }
industry_dict = {}
# 城市字典 { name -> code }
city_dict = {}

# RSA
public_key, private_key = rsa.newkeys(1024)

public_key_base64 = base64.encodebytes(public_key.save_pkcs1())
private_key_base64 = base64.encodebytes(private_key.save_pkcs1())


# 应用配置项
class Config:
    def __init__(self):
        self.server_port = 8910
        # 数据服务地址
        self.data_server_host = "localhost"  # 内网Ip
        self.data_server_port = 8902

        self.data_server_url = f"http://{self.data_server_host}:{self.data_server_port}"

        # 校验token
        self.check_auth = False

        # redis缓存
        self.use_local_cache = True
        self.cache_ip = "localhost"
        self.cache_port = "6388"

        # es
        self.es_ip = "localhost"
        self.es_port = 9200
        self.es_user = "elastic"
        self.es_password = "esTupu@2020"

        # 打印sql
        self.echo_sql = True

        # 日志输出级别
        self.log_level = logging.INFO
        self.log_file = False

        # 用户表
        self.user_table = 'sys_user_info'

        # 数据库连接
        # mysql
        self.mysql_ip = "localhost"
        self.mysql_port = "3306"
        self.mysql_user = "root"
        self.mysql_password = "123456"
        self.mysql_database = "admin"

        # postgis
        self.postgis_ip = "localhost"
        self.postgis_port = "5454"
        self.postgis_user = "work"
        self.postgis_password = "work@post@2020"
        self.postgis_db = "china_basic"
        self.postgis_cube_db = "cube"

        # mongo
        self.mongo_ip = "localhost"
        self.mongo_port = 27017
        self.mongo_user = "root"
        self.mongo_password = ""
        self.mongo_database = ""

        # 白名单：免登录访问方法
        self.white_list = []

        # RSA加密
        self.rsa = False

        # 项目路径
        self.project_path = __file__
        self.project_name = ""

        self.static_path = ""
        self.template_path = ""
        self.log_path = ""
        self.handler_path = ""
        self.temp_path = ""
        self.sql_path = ""
        self.convert_path = ""
        self.dataset_path = ""

        self.doc_path = ""
        self.cookie_secret = ""

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    def keys(self):
        return self.__dict__.keys()


config = Config()
