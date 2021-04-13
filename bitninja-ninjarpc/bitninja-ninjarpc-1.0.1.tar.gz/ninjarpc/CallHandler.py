import logging

from ninjarpc.Helpers import microtime

logger = logging.getLogger(__name__)


class CallHandler:

    def __init__(self, client, command, timeout=600):
        self.client = client
        self.command = command
        self.timeout = timeout
        self.start_time_stamp = microtime(True)
        self.reply_arrived = False
        self.result = None

    def wait(self):
        while not self.reply_arrived:
            self.client.wait()
            self.reply_arrived = self.client.is_result_arrived(self.command.correlation_id)

        self.result = self.client.get_result(self.command.correlation_id)
        return self.result

    def dump_result(self):
        if self.reply_arrived:
            logger.info(self.result.to_array())
            return
        logger.info("No reply has arrived yet!")

    def is_timeouted(self):
        now = microtime(True)
        diff = now - self.start_time_stamp
        if diff > self.timeout:
            return True
        return False
