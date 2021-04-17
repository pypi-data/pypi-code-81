import paramiko
from pprint import pprint
import boto3
from .interface import Map
import sys

import worldmap.argument
import worldmap.core
from simple_utils import logging


class BatchMap(Map):
    def __init__(self, name, kwargs):
        super().__init__(name, kwargs)
        self._name = name
        self._kwargs = kwargs
        self._templates = None
        self._batchs = None

    @property
    def batchs(self):
        if not self._batchs:
            self._batchs = self.get_specs('batch', 'batch')
        return self._batchs

    def execute(self, batch_name):
        batch = self.batchs[batch_name]
        for command in batch['commands']:
            kind = command['kind']
            name = command['name']
            unknown_args = []
            for k, v in command.get('kwargs', {}).items():
                unknown_args.extend([f'--{k}', v])
                
            kind, name, kwargs = worldmap.argument.get(caller='code', kind=kind, name=name, unknown_args=unknown_args)
            worldmap.core.main(kind, name, kwargs)

    def process(self):
        if self._name == 'execute':
            self.execute(self._kwargs['batch_name'])
        else:
            logging.error(f"매개변수 'kind'의 값('{self._name}')이 유효하지 않습니다.")
            exit()
