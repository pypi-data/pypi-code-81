# pylint: disable=dangerous-default-value
import json


class CollectioHelper(object):
    @staticmethod
    def process_key_join(value=[], separator="_"):
        return separator.join(value)

    @staticmethod
    def process_serialize_data(value):
        if isinstance(value, dict) is True:
            return json.dumps(value, check_circular=True)

        return ""

    @staticmethod
    def process_deserialize_data(value):
        if isinstance(value, str) is True:
            return json.loads(value)

        return dict()
