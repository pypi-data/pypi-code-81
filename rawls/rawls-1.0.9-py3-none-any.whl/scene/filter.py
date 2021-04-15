"""Filter class which store Filter information    
"""

from .params import Params


class Filter(Params):
    """Filter class which store Filter params information

    Attributes:
        name: {str} -- name of the kind of Filter used
        params_name: [{str}] -- parameters names of Filter used
        params_values: [{str}] -- parameters values of Filter used
        params_types: [{str}] -- parameters values of Filter used
    """
    def __init__(self, name, params_names, params_values, params_types):
        """Construct filter with all information
        
        Arguments:
            name: {str} -- name of the kind of filter used
            params_name: [{str}] -- parameters names of filter used
            params_values: [{str}] -- parameters values of filter used
            params_types: [{str}] -- parameters values of filter used
        """
        self.module = "Filter"
        self.name = name
        self.params_names = params_names
        self.params_values = params_values
        self.params_types = params_types
