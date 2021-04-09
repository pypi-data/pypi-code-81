import json

import requests

from selfcheck.config import SelfCheckConfig, TrainConfig
from selfcheck.executor.executor import Executor
from selfcheck.minio_accessor import MinIOAccessor
from selfcheck.util import get_uuid


class TrainExecutor(Executor):

    def __init__(self, config: SelfCheckConfig, train_config: TrainConfig):
        self.config = config
        self.train_config = train_config
        self.train_request = None
        self.url = None
        self.model_id = None
        minio_addr = '{}:{}'.format(config.minio_host, config.minio_port)
        self.minio_client = MinIOAccessor(minio_addr, config.minio_access_key, config.minio_secret_key,
                                          config.minio_secure)

    def prepare(self):
        self.model_id = get_uuid()
        self.train_request = {
            'model_id': self.model_id,
            'algorithm': self.config.algorithm_name,
            'parameter': self.train_config.parameter,
            'model_path': '',
            'extend': self.train_config.extend,
            'data': {
                'location': None
            }
        }
        self.url = 'http://{}:{}{}/{}'.format(self.config.algorithm_host, self.config.algorithm_offline_port,
                                              self.config.algorithm_url_prefix, 'train')

        if self.train_config.data_path:
            data_path = 'test/' + get_uuid()
            minio_path = 'ml-platform-data/' + data_path
            self.minio_client.save_object(self.train_config.data_path, minio_path)
            self.train_request['data']['location'] = data_path

        if self.train_config.dict_path:
            dict_path = 'test/' + get_uuid()
            minio_path = 'ml-platform-data/' + dict_path
            self.minio_client.save_object(self.train_config.dict_path, minio_path)
            self.train_request['extend']['dict_location'] = dict_path

        if self.train_config.extra_path:
            extra_path = 'test/' + get_uuid()
            minio_path = 'ml-platform-data/' + extra_path
            self.minio_client.save_object(self.train_config.extra_path, minio_path)
            self.train_request['extend']['extra_location'] = extra_path

    def execute(self):
        print('train url: {}, train request: {}'.format(self.url, json.dumps(self.train_request, ensure_ascii=False,
                                                                             indent=4)))
        resp = requests.post(self.url, json=self.train_request)
        print('train response:', resp.text)
        print()
        resp_json = resp.json()
        if resp_json['status'] in ['success', 'ok']:
            if resp_json['data']['model_id']:
                return resp_json['data']['model_id']
            else:
                return self.model_id
        else:
            raise Exception('train error, {}'.format(json.dumps(resp_json)))
