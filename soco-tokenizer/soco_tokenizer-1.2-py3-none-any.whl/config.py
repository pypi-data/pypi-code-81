import os


class EnvVars(object):
    # system configuration
    REGION = os.environ.get("REGION", 'cn').lower()
    USE_GPU = os.environ.get('USE_GPU', 'on').lower() == 'on'

    APP_VERSION = "0.0.1"
    APP_NAME = "RESTful API for Encoders"
    API_PREFIX = "/encoder"
    DEFAULT_MODEL_PATH = os.environ.get('DEFAULT_MODEL_PATH', "resources")
    MAX_NUM_MODEL = int(os.environ.get('MAX_NUM_MODEL', 10))
    IS_DEBUG = False



