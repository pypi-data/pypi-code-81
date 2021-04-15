from .hashicorp_base import ConnBase
import hvac
import os
import json
from outfit import construct_dict_from_dotkv

class VaultCon(ConnBase):
    """Class to construct the dict properties for the app from Consul and Vault
    """
    
    exception_key = ['host','scheme', 'port', 'path']
    exception_dict = {}
    datakey = {}

    def __init__(self, params = None, exception_dict = None):
        """Constructor inisiating all properties
        """
        ConnBase.__init__(self)

        # if exception dict is known
        if exception_dict:
            self.exception_dict = exception_dict

        # construct the consul and vault params
        vault_params = self.get_configs_dict(self._content['vault'], self.exception_key) if not params else params

        # construct the vault url
        vault_params['url'] = self.exception_dict['scheme'] +'://' + self.exception_dict['host'] + ':' + str(self.exception_dict['port'])

        # construct the vault client objects
        self.vault = hvac.Client(**vault_params)
        self.vault.kv.default_kv_version = '1'

        # get the secret information from vault then save in self.secret dict
        self.secrets = self.vault.secrets.kv.read_secret(self.exception_dict['path'])['data']
   

    def _construct_data_vault(self, key = '', info = {}):
        """construct secret configuration informations of the services from vault return config dict

        Keyword arguments:
        data -- the dict information that came from configuration.py for vault_app_configs
        key -- the string of the path that will be concated with sub key in data dict (default '')
        info -- the informations of the structures of the app configurations that will be merged with secret info (default {})
        """
        result = {}
        for k, v in self.secrets.items():
            result = construct_dict_from_dotkv(result, k.split('.'), v)
        return result

    def get_secret_kv(self):
        """run config constructor return dict all configs
        """ 
        return self._construct_data_vault()
