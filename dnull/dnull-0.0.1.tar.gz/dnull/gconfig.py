import yaml
import os

config_file = os.path.expanduser('~/.config/dnull.yaml')

def config():
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config['dnull']
