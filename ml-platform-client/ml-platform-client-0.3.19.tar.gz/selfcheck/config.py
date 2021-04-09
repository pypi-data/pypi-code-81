from selfcheck.algorithm_type import AlgorithmType


class SelfCheckConfig:
    def __init__(self, host='127.0.0.1', algorithm_type=AlgorithmType.text_custom, algorithm_host=None,
                 algorithm_port=None, algorithm_offline_port=None, algorithm_url_prefix='', algorithm_name=None,
                 minio_host=None, minio_port=9000, minio_access_key=None, minio_secret_key=None, minio_secure=False,
                 ):
        self.host = host

        self.algorithm_type = algorithm_type
        self.algorithm_host = algorithm_host if algorithm_host else host
        self.algorithm_port = algorithm_port
        self.algorithm_offline_port = algorithm_offline_port if algorithm_offline_port else algorithm_port
        self.algorithm_url_prefix = algorithm_url_prefix
        self.algorithm_name = algorithm_name

        self.minio_host = minio_host if minio_host else host
        self.minio_port = minio_port
        self.minio_access_key = minio_access_key
        self.minio_secret_key = minio_secret_key
        self.minio_secure = minio_secure

    def validate(self):
        if not self.algorithm_name:
            raise Exception('no [algorithm_name] configured')

        if not self.algorithm_port:
            raise Exception('no [algorithm_port] configured')

        if not self.minio_access_key:
            raise Exception('no [minio_access_key] configured')

        if not self.minio_secret_key:
            raise Exception('no [minio_secret_key] configured')


class TrainConfig:
    def __init__(self, data_path=None, dict_path=None, extra_path=None, parameter=None, extend=None):
        self.data_path = data_path
        self.dict_path = dict_path
        self.extra_path = extra_path

        if extend is None:
            self.extend = {}
        else:
            self.extend = extend
        if parameter is None:
            self.parameter = {}
        else:
            self.parameter = parameter

    def validate(self):
        pass


class PredictConfig:
    def __init__(self, features=None, params=None, extend=None):
        self.features = features
        if params is None:
            self.params = {}
        else:
            self.params = params
        if extend is None:
            self.extend = {}
        else:
            self.extend = extend

    def validate(self):
        if not self.features:
            raise Exception('no [features] configured')
