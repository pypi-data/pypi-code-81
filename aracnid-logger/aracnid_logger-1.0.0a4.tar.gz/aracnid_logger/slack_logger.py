"""Aracnid Slack Logger module.
"""
import logging
import os

try:
    from slack_bolt import App
except ImportError as e:
    pass

from aracnid_logger.i_logger import Logger


class SlackLogger(Logger):
    """Provides a customized slack logger.

    This class is just a shell that subclasses Logger.
    It may be expanded in the future.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SlackChannelHandler(logging.Handler):
    """Logging handler that sends logs to a Slack Channel.

    Environment Variables:
        SLACK_BOT_TOKEN: Access token for Slack.

    Attributes:
        channel: Slack channel where logs are sent.
        client: Interface to the Slack client.
    """
    def __init__(self, channel=None):
        """Initializes the Slack channel handler.

        Args:
            channel: Slack channel where logs are sent
        """
        # super(SlackChannelHandler, self).__init__()
        super().__init__()

        # set the channel
        self.channel = channel
        if not self.channel:
            raise ValueError('Must supply a "channel" in the logging configuration.')

        # obtain access token
        access_token = os.environ.get('SLACK_BOT_TOKEN')
        if not access_token:
            raise ValueError('Environmental variable, "SLACK_BOT_TOKEN", is not set.')

        # obtain signing secret
        signing_secret = os.environ.get('SLACK_SIGNING_SECRET')
        if not signing_secret:
            raise ValueError('Environmental variable, "SLACK_SIGNING_SECRET", is not set.')

        # authenticate and get slack client
        app = App(token=access_token, signing_secret=signing_secret)
        self.client = app.client

    def emit(self, record):
        """Emits log messages.

        If this chat_postMessage() function fails, it will throw a SlackApiError
        exception (from "slack.errors").

        Args:
            record: The event record to emit.
        """
        self.client.chat_postMessage(
            channel=self.channel,
            text=self.format(record)
        )
