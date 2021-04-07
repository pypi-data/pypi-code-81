import sys

from aiohttp import web
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from swissarmykit.lib.core import Singleton
from swissarmykit.conf import *
from swissarmykit.db.mongodb import BaseDocument

@Singleton
class SlackBot:
    ''' https://github.com/slackapi/python-slackclient
        https://slack.dev/python-slack-sdk/web/index.html
    '''

    def __init__(self, token=None):
        self.enable_slack = swissarmykit_conf.config.get('slack')

        if self.enable_slack or token:
            self.slack_token = token if token else swissarmykit_conf.config.get('slack').get('slack_token')
            self.db = BaseDocument.get_class(swissarmykit_conf.config.get('meta_db', 'meta') + '.slack')
            self.default_channel = swissarmykit_conf.config.get('slack').get('default_channel', '#random')

            self.client = WebClient(token=self.slack_token)

    def send_msg(self, text, channel=None):
        try:
            if not self.enable_slack:
                return ''

            if channel:
                channel = channel if channel[0] == '#' else ('#' + channel)
            else:
                channel = self.default_channel

            self.db.save_url(sys.argv[0] + ' ' + str(datetime.now()), attr={'name': channel, 'description': text},
                             force_insert=True, update_modified_date=True)
            return self.client.chat_postMessage(text=text, channel=channel)
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")
            return web.json_response(data={'message': f"Failed due to {e.response['error']}"})

    def notify(self, text, channel=None):
        return self.send_msg(text=text, channel=channel)


class Slack:

    def __init__(self, token):
        self.client = WebClient(token=token)

    def send(self, text, channel='#random'):
        try:
            if channel[0] != '#':
                channel += '#' + channel
            return self.client.chat_postMessage(text=text, channel=channel)

        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")
            return web.json_response(data={'message': f"Failed due to {e.response['error']}"})

if __name__ == '__main__':
    s = SlackBot.instance()
    # print(s.send_msg('Hello World!'))
    print(s.notify('Hello World!'))

