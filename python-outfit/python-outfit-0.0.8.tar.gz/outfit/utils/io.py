import os
import yaml
from .logger import Logger

def load_yaml(path):
    current_path = os.getcwd()
    full_path = ''

    if path[0:2] == './':
        full_path = os.path.join(current_path, path[2:])
    elif path[0:2] == '..':
        full_path = os.path.join(current_path, path)
    else:
        full_path = path

    content = {}
    # get the yaml file
    with open(full_path, 'r') as stream:
        try:
            content = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            Logger.error('error load yaml file ' + str(err))

    return content

def convert_yaml(stream):
    try:
        return yaml.safe_load(stream)
    except yaml.YAMLError as err:
        Logger.error('error load yaml stream text ' + str(err)) 
