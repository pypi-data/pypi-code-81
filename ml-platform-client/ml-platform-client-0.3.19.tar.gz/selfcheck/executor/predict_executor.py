import json

import requests

from selfcheck.config import SelfCheckConfig, PredictConfig
from selfcheck.executor.executor import Executor


class PredictExecutor(Executor):
    def __init__(self, config: SelfCheckConfig, model_id: str, predict_config: PredictConfig):
        self.config = config
        self.model_id = model_id
        self.predict_config = predict_config
        self.request = None
        self.url = None

    def prepare(self):
        self.request = {
            'algorithm': self.config.algorithm_name,
            'model_id': self.model_id,
            'features': self.predict_config.features,
            'params': self.predict_config.params,
            'extend': self.predict_config.extend
        }
        self.url = 'http://{}:{}{}/{}'.format(self.config.algorithm_host, self.config.algorithm_port,
                                              self.config.algorithm_url_prefix, 'predict')

    def execute(self):
        print('predict url: {}, predict request: {}'.format(self.url, json.dumps(self.request, ensure_ascii=False,
                                                                                 indent=4)))
        resp = requests.post(self.url, json=self.request)
        print('predict response:', resp.text)
        print()
        resp_json = resp.json()
        if resp_json['status'] in ['success', 'ok']:
            return resp_json['data']['predictions']
        else:
            raise Exception('predict error, {}'.format(json.dumps(resp_json)))
