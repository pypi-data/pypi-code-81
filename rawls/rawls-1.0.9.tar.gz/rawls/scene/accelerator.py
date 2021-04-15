"""Accelerator class which store Accelerator information    
"""

from .params import Params


class Accelerator(Params):
    """Accelerator class which store accelerator params information

    Attributes:
        name: {str} -- name of the kind of accelerator used
        params_name: [{str}] -- parameters names of accelerator used
        params_values: [{str}] -- parameters values of accelerator used
        params_types: [{str}] -- parameters values of accelerator used
    """
    def __init__(self, name, params_names, params_values, params_types):
        """Construct accelerator with all information
        
        Arguments:
            name: {str} -- name of the kind of accelerator used
            params_name: [{str}] -- parameters names of accelerator used
            params_values: [{str}] -- parameters values of accelerator used
            params_types: [{str}] -- parameters values of accelerator used
        """
        self.module = "Accelerator"
        self.name = name
        self.params_names = params_names
        self.params_values = params_values
        self.params_types = params_types
