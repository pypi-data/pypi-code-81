import os
from .misc import get_script_location

def wrap(name):
    with open(os.path.join(os.getcwd(), name, 'Dockerfile'), 'w+') as t, open(os.path.join(get_script_location(), 'Dockerfile'), 'r') as s:
        t.write(s.read())

    with open(os.path.join(os.getcwd(), name, 'docker-compose.yml'), 'w+') as t, open(os.path.join(get_script_location(), 'docker-compose.yml'), 'r') as s:
        t.write(s.read())