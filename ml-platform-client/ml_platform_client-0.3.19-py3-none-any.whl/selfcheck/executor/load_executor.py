import json

import requests

from selfcheck.config import SelfCheckConfig
from selfcheck.executor.executor import Executor


class LoadExecutor(Executor):
    def __init__(self, config: SelfCheckConfig, model_id: str, extend=None):
        self.config = config
        self.model_id = model_id
        self.request = None
        self.url = None
        if extend is None:
            self.extend = {}
        else:
            self.extend = extend

    def prepare(self):
        self.request = {
            'algorithm': self.config.algorithm_name,
            'model_id': self.model_id,
            'extend': self.extend,
            'model_path': ''
        }
        self.url = 'http://{}:{}{}/{}'.format(self.config.algorithm_host, self.config.algorithm_port,
                                              self.config.algorithm_url_prefix, 'load')

    def execute(self):
        print('load url: {}, load request: {}'.format(self.url, json.dumps(self.request, ensure_ascii=False,
                                                                           indent=4)))
        resp = requests.post(self.url, json=self.request)
        print('load response:', resp.text)
        resp_json = resp.json()
        if resp_json['status'] in ['success', 'ok']:
            return
        else:
            raise Exception('status error, {}'.format(json.dumps(resp_json)))
