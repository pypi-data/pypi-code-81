"""
Simple slack api
"""

import os
from slack import WebClient
from slack.errors import SlackApiError

from loris.errors import LorisError

# TODO slack blocks

def execute_slack_message(key_info, slack_info):
    """
    Parameters
    ----------
    key_info : dict
        Information of a single entry of a specific table
    slack_info : dict
        Slack information passed to slack config
    """

    token = slack_info['token']
    channel = slack_info['channel']
    text = slack_info.get('text', '').format(**key_info)

    client = WebClient(token=token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
        # assert response["message"]["text"] == text
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        # assert e.response["ok"] is False
        # assert e.response["error"]
        # str like 'invalid_auth', 'channel_not_found'
        raise LorisError(f"Got a Slack error: {e}")

    return response
