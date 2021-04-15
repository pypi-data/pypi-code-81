from abc import ABC
import yaml
import os
from ..utils.logger import Logger
from ..config_loader import Outfit

class ConnBase(ABC):
    exception_dict = {}

    def __init__(self):
        '''Connection Base constructor init the file config
        '''
        self._content = Outfit.content if Outfit.content else None

    def get_configs_dict(self, source = None, exception_key = None):
            """Constructing consul/vault properties from bootstrap.py return list of configs

            it will checking if the property is in exception_key list

            Keyword arguments:
                source -- The dict of vault/consul property from config parsed yaml file 
                exception_key -- The list of special condition field in source
            
            """
            params = {}
            # iterate source items
            for k,v in source.items():
                value = str(v) if type(v) == int else v
                
                def check_envvar(val):
                    return os.environ[val] if val in os.environ else None

                # checking if the string of value is in environment variables
                temp = check_envvar(v[2:len(v)-1]) if ('${' == value[0:2]) and ('}' == value[len(value)-1]) else v
                if temp == None:
                    raise Exception('var value {0}  not found'.format(value))

                # checking if the string of value is in exception keys
                if k not in exception_key:
                    # set the real value to params[k]
                    # if temp value is digit then convert to integer
                    params[k] = temp if type(temp) == int else temp
                else:
                    # if the string of value is in exception keys
                    # assing the temp value (real value) to exception_dict for index v[1:]
                    self.exception_dict[k] =temp if type(temp) == int else temp

            return params
