import json
import random
from typing import List

import requests
from pyngrok import ngrok

from vsw import utils
from vsw.log import Log

logger = Log(__name__).logger


def main(args: List[str]) -> bool:
    try:
        ngrok_process = ngrok.get_ngrok_process()
        save_endpoint(ngrok_process)
        ngrok_process.proc.wait()

    except KeyboardInterrupt:
        print(" => Exit prepare")


def save_endpoint(ngrok_process):
    api_url = ngrok_process.api_url
    logger.info(f'api_url:{api_url}')
    configuration = utils.get_vsw_agent()
    port = configuration.get("inbound_transport_port")
    headers = {'Content-type': 'application/json'}
    response = requests.post(f'{api_url}/api/tunnels', headers=headers, json={
        "addr": f'{port}',
        "proto": "http",
        "name": f"agent{random.randint(0, 100)}"
    })
    logger.info(json.loads(response.text))
    utils.update_endpoint(json.loads(response.text)["public_url"])
