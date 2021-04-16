from __future__ import annotations
from AIH_SDK.Object import Object
from AIH_SDK.AIHClient import AIHClient
from collections import defaultdict
import pandas as pd
import numpy as np
import json

class v2Object(Object):
    
    def __init__(self):
        super().__init__()


    def get(self, id:str=None, parameters:dict={}):
        """
        To get a list of all objects or a specific object.
        Result is set as self.value

        IN: id (str)          - The id of the object to get.
            parameters (dict) - A dictionary of the parameters to include in the query.
        
        OUT: self
        """
        
        if id:
            self.value = self._client._get(self._api, f'{self._endpoint}/{id}', parameters)
        else:
            self.value = self._client._get(self._api, self._endpoint, parameters)
    
        return self