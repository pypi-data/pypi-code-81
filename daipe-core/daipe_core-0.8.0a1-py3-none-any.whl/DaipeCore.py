from pyfonycore.bootstrap.config.config_reader import read  # noqa: F401
from pyfonybundles.Bundle import Bundle


class DaipeCore(Bundle):

    config_reader = read
