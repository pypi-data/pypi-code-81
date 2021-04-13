from ninjarpc import RemoteCommand

import json
import logging

logger = logging.getLogger(__name__)


class JsonEncoder:

    @staticmethod
    def decode(encoded_string):
        decoded_array = json.loads(encoded_string)
        command = RemoteCommand()
        command.load_from_array(decoded_array)

        return command

    @staticmethod
    def encode(command):
        command_dict = command.to_array()

        return json.dumps(command_dict)
