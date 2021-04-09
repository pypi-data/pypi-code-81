import json
import time

import requests

from selfcheck.config import SelfCheckConfig
from selfcheck.constant import APP_ID_KEY
from selfcheck.executor.executor import Executor


class StatusExecutor(Executor):
    def __init__(self, config: SelfCheckConfig, model_id: str, app_id):
        self.config = config
        self.model_id = model_id
        self.url = None
        self.app_id = app_id
        self.request = None

    def prepare(self):
        self.url = 'http://{}:{}{}/{}'.format(self.config.algorithm_host, self.config.algorithm_offline_port,
                                              self.config.algorithm_url_prefix, 'status')
        self.request = {'algorithm': self.config.algorithm_name,
                        'model_id': self.model_id,
                        APP_ID_KEY: self.app_id}

    def execute(self):
        while True:
            print('status url: {}, status request: {}'.format(self.url, json.dumps(self.request, ensure_ascii=False,
                                                                                   indent=4)))
            resp = requests.get(self.url, params=self.request)
            print('status response:', resp.text)
            print()
            resp_json = resp.json()
            if resp_json['status'] in ['success', 'ok']:
                print('status: {}'.format(resp_json['data']['status']))
                if resp_json['data']['status'] == 'completed':
                    return
                if resp_json['data']['status'] == 'error':
                    raise Exception("status error, {}".format(json.dumps(resp_json)))

            else:
                raise Exception("status error, {}".format(json.dumps(resp_json)))
            time.sleep(5)
