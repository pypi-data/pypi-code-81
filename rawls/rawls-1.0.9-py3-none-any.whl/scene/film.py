"""Film class which store Film information    
"""

from .params import Params


class Film(Params):
    """Film class which store Film params information

    Attributes:
        name: {str} -- name of the kind of Film used
        params_name: [{str}] -- parameters names of Film used
        params_values: [{str}] -- parameters values of Film used
        params_types: [{str}] -- parameters values of Film used
    """
    def __init__(self, name, params_names, params_values, params_types):
        """Construct Film with all information
        
        Arguments:
            name: {str} -- name of the kind of film used
            params_name: [{str}] -- parameters names of Film used
            params_values: [{str}] -- parameters values of Film used
            params_types: [{str}] -- parameters values of Film used
        """
        self.module = "Film"
        self.name = name
        self.params_names = params_names
        self.params_values = params_values
        self.params_types = params_types
