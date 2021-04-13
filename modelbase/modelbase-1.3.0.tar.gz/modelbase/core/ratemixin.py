"""Mixin for rates."""

# Standard Library
import warnings
from collections import defaultdict
from dataclasses import dataclass, field

# Third party
import libsbml as libsbml

# Local code
from .utils import (
    convert_id_to_sbml,
    get_formatted_function_source_code,
    patch_lambda_function_name,
    warning_on_one_line,
)

warnings.formatwarning = warning_on_one_line


@dataclass
class Rate:
    """Meta-info container for rates."""

    common_name: str = None
    unit: str = None
    gibbs0: float = None
    ec: str = None
    database_links: dict = field(default_factory=dict)
    notes: dict = field(default_factory=dict)
    sbml_function: str = None
    python_function: str = None


class RateMixin:
    """Mixin adding rate functions."""

    def __init__(self, rates=None, functions=None):
        self.rates = {}
        self.functions = {}
        if rates is not None:
            self.add_rates(rates=rates)
        if functions is not None:
            self.add_functions(functions=functions)

    ##########################################################################
    # Basic rate functions
    ##########################################################################

    def add_function(self, function_name, function):
        if function.__name__ == "<lambda>":
            patch_lambda_function_name(function=function, name=function_name)

        self.functions[function_name] = function

    def add_functions(self, functions):
        for function_name, function in functions.items():
            self.add_function(function_name=function_name, function=function)

    def add_rate(
        self,
        rate_name,
        function,
        substrates=None,
        products=None,
        modifiers=None,
        dynamic_variables=None,
        parameters=None,
        reversible=False,
        args=None,
        **meta_info,
    ):
        """Add a rate function to the model.

        The Python function will get the function arguments in the following order:
        [**substrates, **(products if reversible), **modifiers, **parameters.]

        Parameters
        ----------
        rate_name : str
            Name of the rate function
        function : callable
            Python method calculating the rate equation
        substrates: iterable(str)
            Names of the substrates
        products: iterable(str)
            Names of the products
        modifiers: iterable(str)
            Names of the modifiers. E.g time.
        parameters: iterable(str)
            Names of the parameters
        reversible: bool
            Whether the reaction is reversible.
        meta_info : dict, optional
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        Warns
        -----
        UserWarning
            If rate is already in the model

        Examples
        --------
        def mass_action(S, k1):
            return k1 * S

        m.add_reaction(
            rate_name="v1",
            function=mass_action,
            stoichiometry={"X": -1},
            parameters=["k1"],
        )

        def reversible_mass_action(S, P, k_fwd, k_bwd):
            return k_fwd * S - k_bwd * P

        m.add_reaction(
            rate_name="v2",
            function=reversible_mass_action,
            stoichiometry={"X": -1, "Y": 1},
            parameters=["k2_fwd", "k2_bwd"],
            reversible=True,
        )
        """
        if substrates is None:
            substrates = []
        if products is None:
            products = []
        if parameters is None:
            parameters = []
        if modifiers is None:
            modifiers = []
        if dynamic_variables is None:
            if reversible:
                dynamic_variables = substrates + products + modifiers
            else:
                dynamic_variables = substrates + modifiers
        if args is None:
            args = dynamic_variables + parameters

        if function.__name__ == "<lambda>":
            patch_lambda_function_name(function=function, name=rate_name)

        if rate_name in self.rates:
            warnings.warn(f"Overwriting rate {rate_name}")
            self.remove_rate(rate_name=rate_name)
        self.rates[rate_name] = {
            "function": function,
            "parameters": parameters,
            "substrates": substrates,
            "products": products,
            "modifiers": modifiers,
            "dynamic_variables": dynamic_variables,
            "reversible": reversible,
            "args": args,
        }
        self.meta_info.setdefault("rates", {}).setdefault(rate_name, Rate(**meta_info))

    def add_rates(self, rates, meta_info=None):
        """Add multiple rates to the model.

        Parameters
        ----------
        rates : dict
        meta_info : dict(rate_name: meta_info), optional
            Meta info of the rates

        See Also
        --------
        add_rate
        """
        meta_info = {} if meta_info is None else meta_info
        for rate_name, rate in rates.items():
            try:
                info = meta_info[rate_name]
            except KeyError:
                info = {}
            self.add_rate(rate_name=rate_name, **rate, **info)

    def update_rate(
        self,
        rate_name,
        function=None,
        substrates=None,
        products=None,
        modifiers=None,
        parameters=None,
        reversible=None,
        args=None,
        **meta_info,
    ):
        """Update an existing rate.

        Parameters
        ----------
        rate_name : str
            Name of the rate function
        function : callable, optional
            Python method calculating the rate equation
        substrates: iterable(str), optional
            Names of the substrates
        products: iterable(str), optional
            Names of the products
        modifiers: iterable(str), optional
            Names of the modifiers. E.g time.
        parameters: iterable(str), optional
            Names of the parameters
        reversible: bool, optional
            Whether the reaction is reversible.
        meta_info : dict, optional
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        See Also
        --------
        add_rate
        """
        old_rate = self.rates[rate_name]
        if function is None:
            function = old_rate["function"]
        if substrates is None:
            substrates = old_rate["substrates"]
        if products is None:
            products = old_rate["products"]
        if parameters is None:
            parameters = old_rate["parameters"]
        if modifiers is None:
            modifiers = old_rate["modifiers"]
        if reversible is None:
            reversible = old_rate["reversible"]
        if args is None:
            args = old_rate["args"]

        meta = self.meta_info["rates"][rate_name].__dict__
        meta.update(meta_info)

        self.remove_rate(rate_name=rate_name)
        self.add_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            args=args,
            **meta,
        )

    def update_rate_meta_info(self, rate, meta_info):
        """Update meta info of a rate.

        Parameters
        ----------
        rate : str
            Name of the rate
        meta_info : dict
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}
        """
        self.update_meta_info(component="rates", meta_info={rate: meta_info})

    def remove_rate(self, rate_name):
        """Remove a rate function from the model.

        Parameters
        ----------
        rate_name : str
            Name of the rate
        """
        self.rates.pop(rate_name)

    def remove_rates(self, rate_names):
        """Remove multiple rate functions from the model.

        Parameters
        ----------
        rate_names : iterable(str)
            Names of the rates
        """
        for rate_name in rate_names:
            self.remove_rate(rate_name=rate_name)

    def get_rate_names(self):
        """Return all rate names.

        Returns
        -------
        rate_names : tuple(str)
            Names of all rates
        """
        return tuple(self.rates)

    def get_rate_parameters(self, rate_name):
        """Get the parameters of a rate.

        Parameters
        ----------
        rate_name : str
            Name of the rate

        Returns
        -------
        parameters : list(str)
        """
        return list(self.rates[rate_name]["parameters"])

    def get_rate_substrates(self, rate_name):
        """Get the substrates of a rate.

        Parameters
        ----------
        rate_name : str
            Name of the rate

        Returns
        -------
        substrates : list(str)
        """
        return list(self.rates[rate_name]["substrates"])

    def get_rate_products(self, rate_name):
        """Get the products of a rate.

        Parameters
        ----------
        rate_name : str
            Name of the rate

        Returns
        -------
        products : list(str)
        """
        return list(self.rates[rate_name]["products"])

    def get_rate_modifiers(self, rate_name):
        """Get the modifiers of a rate.

        Parameters
        ----------
        rate_name : str
            Name of the rate

        Returns
        -------
        modifiers : list(str)
        """
        return list(self.rates[rate_name]["modifiers"])

    def get_rate_dynamic_variables(self, rate_name):
        """Get the dynamic variables of a rate.

        Parameters
        ----------
        rate_name : str
            Name of the rate

        Returns
        -------
        dynamic_variables : list(str)
        """
        return list(self.rates[rate_name]["dynamic_variables"])

    def get_rate_function_arguments(self, rate_name):
        """Get the rate function arguments of a rate.

        Parameters
        ----------
        rate_name : str
            Name of the rate

        Returns
        -------
        arguments : list(str)
        """
        return list(
            self.get_rate_dynamic_variables(rate_name=rate_name)
            + self.get_rate_parameters(rate_name=rate_name)
        )

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def _get_fluxes(self, *, fcd: dict):
        """Calculate the fluxes.

        This is the performance optimized version of the function

        Parameters
        ----------
        y : dictionary
            Concentration of each compound (including time!)

        Returns
        -------
        rates : dict(str: num)
            Dictionary containing all calculated rates
        """
        # args = self.parameters | fcd # python 3.9+ syntax
        args = {**self.parameters, **fcd}
        fluxes = {}
        for name, rate in self.rates.items():
            try:
                fluxes[name] = rate["function"](*(args[arg] for arg in rate["args"]))
            except KeyError as e:
                raise KeyError(f"Could not find argument {e} for rate {name}")
        return fluxes

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_function_source_code(self):
        function_strings = []
        for name, function in self.functions.items():
            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="function"
            )
            function_strings.append(function_code)
        return "\n".join(sorted(function_strings))

    def _generate_rates_source_code(self, *, include_meta_info=True):
        """Generate modelbase source code for rates.

        This is mainly used for the generate_model_source_code function.

        Parameters
        ----------
        include_meta_info : bool
            Whether to include meta info in the source code.

        Returns
        -------
        rate_source_code : str
            Code generating the Python functions of the rates
        rate_modelbase_code : str
            Code generating the modelbase objects

        See Also
        --------
        generate_model_source_code
        """
        rate_functions = set()
        rates = []

        for name, rate in self.rates.items():
            function = rate["function"]
            substrates = rate["substrates"]
            products = rate["products"]
            modifiers = rate["modifiers"]
            parameters = rate["parameters"]
            reversible = rate["reversible"]

            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="rate"
            )
            rate_functions.add(function_code)
            rate_definition = (
                "m.add_rate(\n"
                f"    rate_name={repr(name)},\n"
                f"    function={function.__name__},\n"
                f"    substrates={substrates},\n"
                f"    products={products},\n"
                f"    modifiers={modifiers},\n"
                f"    parameters={parameters},\n"
                f"    reversible={reversible},\n"
            )
            if include_meta_info:
                meta_info = self._get_nonzero_meta_info(component="rates")
                try:
                    info = meta_info[name]
                    rate_definition += f"    **{info}\n"
                except KeyError:
                    pass
            rate_definition += ")"
            rates.append(rate_definition)
        return "\n".join(sorted(rate_functions)), "\n".join(rates)

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_rates(self, *, sbml_model):
        """Convert the rates into sbml reactions.

        Parameters
        ----------
        sbml_model : libsbml.Model
        """
        for rate_id, rate in self.rates.items():
            meta_info = self.meta_info["rates"][rate_id]

            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))
            name = meta_info.common_name
            if name:
                rxn.setName(name)
            rxn.setFast(False)
            rxn.setReversible(rate["reversible"])

            substrates = defaultdict(int)
            products = defaultdict(int)
            for compound in rate["substrates"]:
                substrates[compound] += 1
            for compound in rate["products"]:
                products[compound] += 1

            for compound, stoichiometry in substrates.items():
                sref = rxn.createReactant()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(False)

            for compound, stoichiometry in products.items():
                sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(False)

            for compound in rate["modifiers"]:
                sref = rxn.createModifier()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))

            function = meta_info.sbml_function
            if function is not None:
                kinetic_law = rxn.createKineticLaw()
                kinetic_law.setMath(libsbml.parseL3Formula(function))
