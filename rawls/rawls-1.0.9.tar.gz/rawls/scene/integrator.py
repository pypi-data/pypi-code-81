"""Integrator class which store Integrator information    
"""

from .params import Params


class Integrator(Params):
    """Integrator class which store Integrator params information

    Attributes:
        name: {str} -- name of the kind of Integrator used
        params_name: [{str}] -- parameters names of Integrator used
        params_values: [{str}] -- parameters values of Integrator used
        params_types: [{str}] -- parameters values of Integrator used
    """
    def __init__(self, name, params_names, params_values, params_types):
        """Construct integrator with all information
        
        Arguments:
            name: {str} -- name of the kind of integrator used
            params_name: [{str}] -- parameters names of integrator used
            params_values: [{str}] -- parameters values of integrator used
            params_types: [{str}] -- parameters values of integrator used
        """
        self.module = "Integrator"
        self.name = name
        self.params_names = params_names
        self.params_values = params_values
        self.params_types = params_types
