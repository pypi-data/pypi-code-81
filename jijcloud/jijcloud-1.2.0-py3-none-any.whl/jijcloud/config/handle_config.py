import os
from pathlib import Path
from typing import Optional
import toml

# DEFAULT SETTING
CONFIG_PATH = str(Path.home())+'/.jijcloud/'
HOST_URL = 'https://apim-jijcloud-prod.azure-api.net/'
DEFAULT_CONFIG_FILE = 'config.toml'


def create_config(token: str, host_url=HOST_URL, config_path=CONFIG_PATH):
    Path(config_path).mkdir(parents=True, exist_ok=True)

    config_dict = {
        'default': {
            'url': host_url,
            'token': token
        }
    }
    # save config file's
    config_path = config_path if config_path[-1] == '/' else config_path + '/'
    config_file_name = config_path + DEFAULT_CONFIG_FILE
    with open(config_file_name, mode='w') as f:
        toml.dump(config_dict, f)

    return config_file_name


def load_config(file_name: str, config='default') -> dict:
    """load config file (TOML file)

    Args:
        file_name (str): path to config file.
        config (str, optional): loading enviroment name. Defaults to 'default'.

    Raises:
        TypeError: if 'config' enviroment is not defined in config file.

    Returns:
        dict: {'token': 'xxxx', 'url': 'xxxx'} 
    """
    p_rel = Path(file_name)
    with open(p_rel) as f:
        toml_setting_file = toml.load(f)
    if config not in toml_setting_file:
        raise TypeError(
            "'{}' is not define in config file ({}).".format(config, file_name))
    return toml_setting_file


class Config:
    """JijCloud API Config
    Attributes:
        url (str): API URL.
        token (str): Secret token to connect API.
    """
    def __init__(
            self,
            url: Optional[str] = None,
            token: Optional[str] = None,
            config: Optional[str] = None,
            config_env: str = 'default'):

        if url is not None and token is not None:
            if not isinstance(url, str) or not isinstance(token, str):
                raise TypeError("'url' and 'token' are `str`.")
            self.url = url
            self.token = token
        else:
            if config is None:
                config_file = CONFIG_PATH + DEFAULT_CONFIG_FILE
            else:
                config_file = config
            if not os.path.exists(config_file):
                message = "A configuration file is not exist.\n"
                message += "set arguments of __init__(): 'url' and 'token'\n"
                message += "or create config file"
                message += " using `jijcloud create` command."
                raise ValueError(message)
            _config = load_config(config_file, config_env)
            self.token = _config[config_env]['token']
            self.url = _config[config_env]['url']
