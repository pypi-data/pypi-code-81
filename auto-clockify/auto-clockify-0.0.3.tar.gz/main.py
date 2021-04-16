import sys
import argparse
from datetime import datetime
from autoclockify.api_client import ApiClient
from autoclockify.config import load_config, get_config


def send_api_request(action):
    method = None
    endpoint = None
    headers = None
    data = None
    user_id = get_config("user_id")
    workspace_id = get_config("workspace_id")
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    api_client = ApiClient()
    if action == "start":
        method = "POST"
        endpoint = "/workspaces/{}/time-entries".format(workspace_id)
        data = {
            "start": now,
            "description": "___WORKING___",
            "billable": "false"
        }
    elif action == "stop":
        method = "PATCH"
        endpoint = "/workspaces/{}/user/{}/time-entries".format(workspace_id, user_id)
        data = {
            "end": now,
        }

    api_client.send_request(method, endpoint, headers=headers, data=data)


# Add command line arguments
parser = argparse.ArgumentParser(description='AutoClockify')
parser.add_argument('action', choices=['start', 'stop'], type=str, help='Your action: start or stop')
parser.add_argument('--config', type=str, default=None, help='The configuration file to use.')
args = parser.parse_args()

if __name__ == '__main__':
    print("Action: {}".format(args.action))
    load_config(args.config)
    send_api_request(args.action)
