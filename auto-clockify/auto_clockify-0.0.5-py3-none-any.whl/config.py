import json
import sys
import os

_config: any = {}


def get_config(key, default=None):
    val = default
    if key in _config:
        val = _config[key]
    return val


def load_config(config_file=None):
    global _config
    if _config:
        return
    if config_file is None:
        if os.name == "posix":
            config_file = "{0}/.config/autoclockify.json".format(os.path.expanduser("~"))
        elif os.name == "nt":
            config_file = "{0}/AppData/Local/AutoClockify/autoclockify.json".format(os.path.expanduser("~"))
        else:
            print("Unsupported OS!")
            exit(1)

    try:
        print("Loading config file: {}".format(config_file))
        with open(config_file) as config_file:
            _config = json.load(config_file)
    except Exception as e:
        sys.exit(e)
