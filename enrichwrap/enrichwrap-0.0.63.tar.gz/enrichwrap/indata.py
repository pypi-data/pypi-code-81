import json

from enrichwrap import get_contents


def get_default_data():
    with open(get_contents('samples', 'sample_input.json')) as json_user_data_file:
        return json.load(json_user_data_file)


def get_data(val=None):
    if val is not None:
        return json.loads(val)
    return get_default_data()
