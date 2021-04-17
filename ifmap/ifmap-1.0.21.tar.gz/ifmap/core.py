import yaml
import simple_utils
import argparse
from .plugins.aws import AWSMap
from .plugins.docker import DockerMap
from .plugins.batch import BatchMap
import sys
import os
import template_manager
from simple_utils import logging
import time


def main(kind, name, kwargs):

    if kind == 'aws':
        AWSMap(name, kwargs).process()
    elif kind == 'docker':
        DockerMap(name, kwargs).process()
    elif kind == 'batch':
        BatchMap(name, kwargs).process()
    elif kind == 'sleep':
        # batch 때 사용되는 kind.
        time.sleep(int(name))
    else:
        logging.error(f"매개변수 'kind'의 값('{kind}')이 유효하지 않습니다.")
