"""Generic class which store module params information
"""


class Params():
    """Generic class which store module params information

    Attributes:
        module: {str} -- name of the module
        name: {str} -- name of the kind of module used
        params_name: [{str}] -- parameters names of module used
        params_values: [{str}] -- parameters values of module used
        params_types: [{str}] -- parameters values of module used
    """
    def __init__(self, module, name, params_names, params_values,
                 params_types):
        """Construct module with all information
        
        Arguments:
            module: {str} -- name of the module
            name: {str} -- name of the kind of module used
            params_name: [{str}] -- parameters names of module used
            params_values: [{str}] -- parameters values of module used
            params_types: [{str}] -- parameters values of module used
        """
        self.module = module
        self.name = name
        self.params_names = params_names
        self.params_values = params_values
        self.params_types = params_types

    def get_params(self):
        """Get information about available params

        Returns:
            [{str}] -- list of available params for this module
        """
        return self.params_names

    def get_param(self, name):
        """Get specific param value using its name 

        Arguments:
            name: {str} -- expected param name

        Returns:
            {(str|float|int)} -- returns param value with its specific type
        """

        if name not in self.params_names:
            raise Exception('Param `{0}` given not in available params: {1}'\
                    .format(name, self.params_names))

        # get param index
        index_param = self.params_names.index(name)

        # check if float or integer type
        if self.params_types[index_param] == 'integer':
            return int(self.params_values[index_param])

        if self.params_types[index_param] == 'float':
            return int(self.params_values[index_param])

        # default case is str
        return self.params_values[index_param]

    def __str__(self):
        """Display module information
        
        Returns:
            {str} -- module information
        """
        if len(self.name) > 0:

            output = "{0}: `{1}`".format(self.module, self.name)

            for index, p in enumerate(self.params_names):
                output += '\n\t\t- [{0}] {1}: {2}' \
                    .format(self.params_types[index], p, self.params_values[index])

            return output
        else:
            return "{0}: default".format(self.module)

    def to_rawls(self):
        """Display module information for .rawls file
        
        Returns:
            {str} -- module information for .rawls file
        """
        output = '#{0} {1}\n\t#params '.format(self.module, self.name)

        for index, p in enumerate(self.params_names):

            # check if value is digit or not
            if self.params_values[index].replace('.', '', 1).isdigit():
                output += '"{0} {1}" [{2} ] ' \
                    .format(self.params_types[index], p, self.params_values[index])
            else:
                output += '"{0} {1}" ["{2}" ] ' \
                    .format(self.params_types[index], p, self.params_values[index])

        return output
