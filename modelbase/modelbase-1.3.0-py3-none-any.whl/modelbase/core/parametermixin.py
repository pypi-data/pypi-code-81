"""Mixin for Parameters."""

# Standard Library
import json as json
import pickle as pickle
import warnings
from dataclasses import dataclass, field

# Local code
from .utils import convert_id_to_sbml, warning_on_one_line

warnings.formatwarning = warning_on_one_line


@dataclass
class Parameter:
    """Meta-info container for parameters."""

    unit: str = None
    annotation: str = None
    database_links: dict = field(default_factory=dict)
    notes: dict = field(default_factory=dict)


class ParameterMixin:
    """Adding parameter functions."""

    def __init__(self, parameters=None):
        self.parameters = {}
        self.derived_parameters = {}
        self._derived_from_parameters = set()
        if parameters is not None:
            self.add_parameters(parameters=parameters)
        self.initialization_parameters = self.parameters.copy()

    ##########################################################################
    # Parameter functions
    ##########################################################################

    def add_parameter(self, parameter_name, parameter_value, **meta_info):
        """Add a new parameter to the model.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter
        parameter_value : num
            Numeric value of the parameter
        meta_info : dict, optional
            Meta info of the parameter. Allowed keys are
            {unit, database_links, notes}

        Warns
        -----
        UserWarning
            If parameter is already in the model
        """
        if parameter_name in self.parameters:
            warnings.warn(
                f"Key {parameter_name} is already in the model. Please use the update_parameters method"
            )
        self.add_and_update_parameter(
            parameter_name=parameter_name, parameter_value=parameter_value, **meta_info
        )

    def add_parameters(self, parameters, meta_info=None):
        """Add new parameters to the model.

        Parameters
        ----------
        parameters : dict(str: num)
            Dictionary containing the parameter and value pairs
        meta_info : dict(parameter_name: meta_info)
            Meta info of the parameters

        See Also
        --------
        add_parameter
        """
        meta_info = {} if meta_info is None else meta_info
        for parameter_name, parameter_value in parameters.items():
            try:
                info = meta_info[parameter_name]
            except KeyError:
                info = {}
            self.add_parameter(
                parameter_name=parameter_name,
                parameter_value=parameter_value,
                **info,
            )

    def update_parameter(self, parameter_name, parameter_value, **meta_info):
        """Update a model parameter.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter
        parameter_value : num
            Numeric value of the parameter
        meta_info : dict, optional
            Meta info of the parameter. Allowed keys are
            {unit, database_links, notes}

        Warns
        -----
        UserWarning
            If parameter is not in the model
        """
        if parameter_name not in self.parameters:
            warnings.warn(f"Key {parameter_name} is not in the model. Please use the add_parameters method")
        self.add_and_update_parameter(
            parameter_name=parameter_name, parameter_value=parameter_value, **meta_info
        )

    def update_parameters(self, parameters, meta_info=None):
        """Update existing model parameters.

        Parameters
        ----------
        parameters : dict(str: num)
            Dictionary containing the parameter and value pairs
        meta_info : dict(parameter_name: meta_info)
            Meta info of the parameters

        See Also
        --------
        update_parameter
        """
        meta_info = {} if meta_info is None else meta_info
        for parameter_name, parameter_value in parameters.items():
            try:
                info = meta_info[parameter_name]
            except KeyError:
                info = {}
            self.update_parameter(parameter_name=parameter_name, parameter_value=parameter_value, **info)

    def add_and_update_parameter(self, parameter_name, parameter_value, update_derived=True, **meta_info):
        """Add a new or update an existing parameter.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter
        parameter_value : num
            Numeric value of the parameter
        meta_info : dict, optional
            Meta info of the parameter. Allowed keys are
            {unit, database_links, notes}
        """
        if parameter_name in self.parameters:
            old_meta_info = self.meta_info["parameters"][parameter_name].__dict__
            old_meta_info.update(meta_info)
            meta_info = old_meta_info
            self.remove_parameter(parameter_name=parameter_name)

        self.parameters[parameter_name] = parameter_value
        self.meta_info.setdefault("parameters", {}).setdefault(parameter_name, Parameter(**meta_info))
        if parameter_name in self._derived_from_parameters and update_derived:
            self._update_derived_parameters()

    def add_and_update_parameters(self, parameters, meta_info=None):
        """Add new and updates existing model parameters.

        Parameters
        ----------
        parameters : dict(str: num)
            Dictionary containing the parameter and value pairs
        meta_info : dict(parameter_name: meta_info)
            Meta info of the parameters

        See Also
        --------
        add_and_update_parameter
        """
        meta_info = {} if meta_info is None else meta_info
        for parameter_name, parameter_value in parameters.items():
            try:
                info = meta_info[parameter_name]
            except KeyError:
                info = {}
            self.add_and_update_parameter(
                parameter_name=parameter_name, parameter_value=parameter_value, **info
            )

    def update_parameter_meta_info(self, parameter, meta_info):
        """Update meta info of a parameter.

        Parameters
        ----------
        parameter : str
            Name of the parameter
        meta_info : dict, optional
            Meta info of the parameter. Allowed keys are
            {unit, database_links, notes}
        """
        self.update_meta_info(component="parameters", meta_info={parameter: meta_info})

    def remove_parameter(self, parameter_name):
        """Remove a parameter from the model.

        Parameters
        ----------
        parameter_name: str
        """
        del self.parameters[parameter_name]
        del self.meta_info["parameters"][parameter_name]

    def remove_parameters(self, parameter_names):
        """Remove parameters from the model.

        Parameters
        ----------
        parameter_names : iterable(str)
            Names of the parameters that should be removed

        See Also
        --------
        remove_parameter
        """
        for parameter_name in parameter_names:
            self.remove_parameter(parameter_name=parameter_name)

    def add_derived_parameter(self, parameter_name, function, parameters=None):
        """Add a derived parameter.

        Derived parameters are calculated from other model parameters and dynamically updated
        on any changes.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter
        function : callable
            Python function calculating the new parameter
        parameters : list(str)
            Names of parameters to be passed to the function
        """
        # Do this first to check if all parameters are actually in the model
        parameter_values = [self.parameters[i] for i in parameters]

        self.derived_parameters[parameter_name] = {
            "function": function,
            "parameters": parameters,
        }
        for parameter in parameters:
            self._derived_from_parameters.add(parameter)

        # Initial calculation
        self.add_parameter(
            parameter_name=parameter_name,
            parameter_value=function(*parameter_values),
        )

    def remove_derived_parameter(self, parameter_name):
        """Remove a derived parameter from the model.

        Parameters
        ----------
        parameter_name : str
            Name of the derived parameter
        """
        old_parameter = self.derived_parameters.pop(parameter_name)
        derived_from = old_parameter["parameters"]
        for i in derived_from:
            if all(i not in j["parameters"] for j in self.derived_parameters.values()):
                self._derived_from_parameters.remove(i)
        self.remove_parameter(parameter_name=parameter_name)

    def _update_derived_parameters(self):
        """Update values of all derived parameters.

        This function is supposed to be run after a change to any parameter
        from which a derived parameter is calculated. Since this operation
        is assumed to take not a lot of time, it is run for all parameters.
        If there ever is a model with lots of derived parameters, it might
        make sense to make this a little less brute-force ;)
        """
        for parameter_name, param_dict in self.derived_parameters.items():
            self.add_and_update_parameter(
                parameter_name=parameter_name,
                parameter_value=param_dict["function"](
                    *(self.parameters[i] for i in param_dict["parameters"])
                ),
                update_derived=False,
            )

    def store_parameters_to_file(self, filename, filetype="json"):
        """Store the parameters into a json or pickle file.

        Parameters
        ----------
        filename : str
            The name of the pickle file
        filetype : {json, pickle}
            Output file type.
        """
        if filetype == "json":
            if not filename.endswith(".json"):
                filename += ".json"
            with open(filename, "w") as f:
                json.dump(self.parameters, f)
        elif filetype == "pickle":
            if not filename.endswith(".p"):
                filename += ".p"
            with open(filename, "wb") as f:
                pickle.dump(self.parameters, f)
        else:
            raise ValueError("Can only save to json or pickle")

    def load_parameters_from_file(self, filename, filetype="json"):
        """Load parameters from a json or pickle file.

        Parameters
        ----------
        filename : str
            The name of the pickle file
        filetype : {json, pickle}
            Input file type.
        """
        if filetype == "json":
            with open(filename, "r") as f:
                self.add_and_update_parameters(parameters=json.load(f))
        elif filetype == "pickle":
            with open(filename, "rb") as f:
                self.add_and_update_parameters(parameters=pickle.load(f))
        else:
            raise ValueError("Can only load from json or pickle")

    def restore_initialization_parameters(self):
        """Restore parameters to initialization parameters."""
        self.parameters = self.initialization_parameters.copy()

    def get_parameter(self, parameter_name):
        """Return a single parameter.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter

        Returns
        -------
        parameter_value : float
            Value of the parameter
        """
        return float(self.parameters[parameter_name])

    def get_parameters(self):
        """Return all parameters.

        Returns
        -------
        parameters : dict(str, num)
        """
        return dict(self.parameters)

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_parameters_source_code(self, *, include_meta_info=True):
        """Generate modelbase source code for parameters.

        This is mainly used for the generate_model_source_code function.

        Parameters
        ----------
        include_meta_info : bool
            Whether to include the parameter meta info

        Returns
        -------
        parameter_modelbase_code : str
            Source code generating the modelbase parameters
        """
        parameters = repr(self.parameters)
        if include_meta_info:
            meta_info = self._get_nonzero_meta_info(component="parameters")
            if bool(meta_info):
                return f"m.add_parameters(parameters={parameters}, meta_info={meta_info})"
        return f"m.add_parameters(parameters={parameters})"

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_parameters(self, *, sbml_model):
        """Create the parameters for the sbml model.

        Parameters
        ----------
        sbml_model : libsbml.Model
        """
        for parameter_id, value in self.parameters.items():
            parameter = self.meta_info["parameters"][parameter_id]
            k = sbml_model.createParameter()
            k.setId(convert_id_to_sbml(id_=parameter_id, prefix="PAR"))
            k.setConstant(True)
            k.setValue(float(value))
            unit = parameter.unit
            if unit is not None:
                k.setUnits(unit)
