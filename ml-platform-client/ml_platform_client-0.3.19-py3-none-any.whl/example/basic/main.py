from ml_platform_client.config import global_config
from ml_platform_client.dispatcher import register, set_config
from ml_platform_client.load_checker import checker
from ml_platform_client.server import app
from ml_platform_client.server import set_preload_models
from example.basic.algorithms import MyAlgorithm, FakeAlgorithm

minio_host = '172.16.99.29:9000'
minio_access_key = '24WTCKX23M0MRI6BA72Y'
minio_secret_key = '6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX'
minio_secure = False
mysql_host = '172.16.99.29'
mysql_port = 3306
mysql_user = 'root'
mysql_password = 'password'


# 通过global_config向sdk传入minio和db信息
global_config.minio_host = minio_host
global_config.minio_access_key = minio_access_key
global_config.minio_secret_key = minio_secret_key
global_config.minio_secure = minio_secure

global_config.mysql_host = mysql_host
global_config.mysql_port = mysql_port
global_config.mysql_user = mysql_user
global_config.mysql_password = mysql_password

set_config(global_config)

# 注册自定义算法
register('my_alg', MyAlgorithm)
register('fake_alg', FakeAlgorithm)

# 如果有内置模型可以在这里指定模型id，会在服务启动时load起来
# set_preload_models('my_alg', ['pretrain_model_id1', 'pretrain_model_id2'])

# 定时从mlp表查询算法需要加载的模型，防止重启后所有模型都变为不加载状态
# checker.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
