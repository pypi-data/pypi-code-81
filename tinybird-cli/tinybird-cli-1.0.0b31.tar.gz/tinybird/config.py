from pathlib import Path
import os.path
import json
import click
from .feedback_manager import FeedbackManager

DEFAULT_HOST = 'https://api.tinybird.co'


async def get_config(hostFlag, tokenFlag):
    config_file = Path(os.getcwd()) / ".tinyb"
    config = {}
    try:
        config = json.loads(open(config_file).read())
    except IOError:
        pass
    except json.decoder.JSONDecodeError:
        click.echo(FeedbackManager.error_load_file_config(config_file=config_file))
        return
    config['token'] = tokenFlag or config.get('token', None)
    config['host'] = hostFlag or config.get('host', DEFAULT_HOST)
    config['workspaces'] = config.get('workspaces', [])
    return config


async def write_config(config):
    config_file = Path(os.getcwd()) / ".tinyb"
    open(config_file, 'w').write(json.dumps(config))
