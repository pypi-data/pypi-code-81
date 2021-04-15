#import conf.bootstrap as config
#import conf.datakey as datakey
from .hashicorp_base import ConnBase
import consul
import os
import json
from ..utils.io import convert_yaml
from ..utils.logger import Logger

class ConsulCon(ConnBase):
    """Class to construct the dict properties for the app from Consul and Vault
    """

    exception_key = ['path']
    exception_dict = {}
    cons = None

    def __init__(self, params = None, exception_dict = None):
        """Constructor inisiating all properties
        """
        ConnBase.__init__(self)

        # if exception dict is known
        if exception_dict:
            self.exception_dict = exception_dict
        
        # construct the consul and vault params
        consul_params = self.get_configs_dict(self._content['consul'], self.exception_key) if not params else params

        # construct the consul
        self.cons = consul.Consul(**consul_params)

   
    def get_kv(self, type = 'json'):
        """run config constructor return dict all configs
        
        Keyword arguments :
            type -- The type of the value text format
        """

        type_enum = {
            'json' : lambda x: json.loads(x.decode('utf-8')) if x else '',
            'yaml' : lambda x: convert_yaml(x) if x else ''
        }
        temp = self.cons.kv.get(self.exception_dict['path'])[1]['Value']
        result = type_enum[type](temp) 
        return result

