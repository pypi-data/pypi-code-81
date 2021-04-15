"""Sampler class which store Sampler information    
"""

from .params import Params


class Sampler(Params):
    """Sampler class which store Sampler params information

    Attributes:
        name: {str} -- name of the kind of Sampler used
        params_name: [{str}] -- parameters names of Sampler used
        params_values: [{str}] -- parameters values of Sampler used
        params_types: [{str}] -- parameters values of Sampler used
    """
    def __init__(self, name, params_names, params_values, params_types):
        """Construct sampler with all information
        
        Arguments:
            name: {str} -- name of the kind of sampler used
            params_name: [{str}] -- parameters names of sampler used
            params_values: [{str}] -- parameters values of sampler used
            params_types: [{str}] -- parameters values of sampler used
        """
        self.module = "Sampler"
        self.name = name
        self.params_names = params_names
        self.params_values = params_values
        self.params_types = params_types
