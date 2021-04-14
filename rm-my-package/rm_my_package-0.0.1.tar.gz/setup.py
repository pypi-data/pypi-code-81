import os
from setuptools import setup
from setuptools.config import read_configuration

def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    config = read_configuration(os.path.join(here,'setup.cfg'))
    print("Version:", config['metadata']['version'])

# setup.
if __name__ == '__main__':
    get_version()
    setup()