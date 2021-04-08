import logging
from waveletai import constants
import threading
from waveletai.sessions import Session
from waveletai.backends.hosted_backend import HostedBackend

logging.basicConfig(format='[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                    level=logging.INFO)

_logger = logging.getLogger(__name__)

__lock = threading.RLock()

""""Access as an anonymous user.
You can pass this value as api_token during init() call, either by an environment variable or passing it directly
"""
ANONYMOUS = constants.ANONYMOUS
"""Anonymous user API token.
You can pass this value as api_token during init() call, either by an environment variable or passing it directly
"""
ANONYMOUS_API_TOKEN = constants.ANONYMOUS_API_TOKEN
from waveletai._version import get_versions

__version__ = get_versions()['version']

_backend = None


def init(name=None, pwd=None, backend=None):
    with __lock:
        global _backend

        if backend is None:
            # backend_name = os.getenv(envs.BACKEND)
            # if backend_name == 'offline':
            #     backend = OfflineBackend()

            # elif backend_name is None:
            _backend = HostedBackend(name, pwd)

            # else:
            #     raise InvalidBackend(backend_name)
        return _backend
        # session = Session(backend=backend)
        # return session


def create_dataset(name, zone, path, data_type=constants.DataType.TYPE_FILE.value, desc=None):
    """
    创建数据集
    :param name: 数据集名称
    :param zone: 数据集区域
    :param path: 要上传的本地数据的路径
    :param data_type: 一个数据集中的数据类型是唯一的。备选值constants.DataType，固定提供图片、文件、视频、视频帧的数据类型
    :param desc: 数据集详情
    :return: Dataset对象
    """
    global _backend
    return _backend.create_dataset(name, zone, path, data_type, desc)



