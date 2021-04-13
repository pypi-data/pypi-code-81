"""Mixin for algebraic modules. These are used to calculate e.g. QSSA assumptions."""

# Standard Library
import warnings
from dataclasses import dataclass, field

# Third party
import numpy as np

# Local code
from .utils import (
    get_formatted_function_source_code,
    patch_lambda_function_name,
    warning_on_one_line,
)

warnings.formatwarning = warning_on_one_line


@dataclass
class Module:
    """Meta-info container for an algebraic module."""

    common_name: str = None
    notes: dict = field(default_factory=dict)
    database_links: dict = field(default_factory=dict)


class AlgebraicMixin:
    """Mixin for algebraic modules.

    This adds the capability to calculate concentrations of derived
    compounds that are calculated before the rate functions are calculated.
    """

    def __init__(self, algebraic_modules=None):
        self.derived_compounds = []
        self.algebraic_modules = {}
        if algebraic_modules is not None:
            self.add_algebraic_modules(algebraic_modules=algebraic_modules)

    ##########################################################################
    # Derived compound functions
    ##########################################################################

    def _add_derived_compound(self, *, compound):
        """Add a derived compound to the model.

        Derived compounds are dynamic quantities calculated by algebraic modules.
        They are accessible by other rates but are not returned to any integrators.

        Parameters
        ----------
        compound : str
            Name / id of the compound
        """
        if not isinstance(compound, str):
            raise TypeError("The compound name should be string")
        if compound == "time":
            raise KeyError("time is a protected variable for time")
        if compound in self.derived_compounds:
            warnings.warn(f"Overwriting derived compound {compound}")
        self.derived_compounds.append(compound)

    def _add_derived_compounds(self, *, compounds):
        """Add multiple derived compounds to the model.

        Derived compounds are dynamic quantities calculated by algebraic modules.
        They are accessible by other rates but are not returned to any integrators.

        Parameters
        ----------
        compounds : Iterable(str)

        See Also
        --------
        _add_derived_compound
        """
        for compound in compounds:
            self._add_derived_compound(compound=compound)

    def _remove_derived_compound(self, *, compound):
        """Remove a derived compound from the model.

        Parameters
        ----------
        compound : str
            Name / id of the compound
        """
        self.derived_compounds.remove(compound)

    def _remove_derived_compounds(self, *, compounds):
        """Remove multiple derived compounds from the model.

        Parameters
        ----------
        compounds : Iterable(str)
        """
        for compound in compounds:
            self._remove_derived_compound(compound=compound)

    def get_derived_compounds(self):
        """Return names of compounds derived from algebraic modules.

        Returns
        -------
        derived_compounds : list(str)
        """
        return list(self.derived_compounds)

    def get_all_compounds(self):
        """Return names of compounds and derived compounds in that order.

        Returns
        -------
        all_compounds: list(str)
        """
        return list(self.get_compounds() + self.get_derived_compounds())

    ##########################################################################
    # Algebraic Modules
    ##########################################################################

    def add_algebraic_module(
        self,
        module_name,
        function,
        compounds=None,
        derived_compounds=None,
        modifiers=None,
        parameters=None,
        args=None,
        **meta_info,
    ):
        """Add an algebraic module to the model.

        CAUTION: The Python function of the module has to return an iterable.
        The Python function will get the function arguments in the following order:
        [**compounds, **modifiers, **parameters]

        Parameters
        ----------
        module_name : str
            Name of the module
        function : callable
            Python method of the algebraic module
        compounds : iterable(str)
            Names of compounds used for module
        derived_compounds : iterable(str)
            Names of compounds which are calculated by the module
        modifiers : iterable(str)
            Names of compounds which act as modifiers on the module
        parameters : iterable(str)
            Names of the parameters which are passed to the function
        meta_info : dict, optional
            Meta info of the algebraic module. Allowed keys are
            {common_name, notes, database_links}

        Warns
        -----
        UserWarning
            If algebraic module is already in the model.

        Examples
        --------
        def rapid_equilibrium(substrate, k_eq):
            x = substrate / (1 + k_eq)
            y = substrate * k_eq / (1 + k_eq)
            return x, y

        add_algebraic_module(
            module_name="fast_eq",
            function=rapid_equilibrium,
            compounds=["A"],
            derived_compounds=["X", "Y"],
            parameters=["K"],
        )
        """
        if compounds is None:
            compounds = []
        if derived_compounds is None:
            derived_compounds = []
        if modifiers is None:
            modifiers = []
        if parameters is None:
            parameters = []
        if args is None:
            args = compounds + modifiers + parameters

        patch_lambda_function_name(function=function, name=module_name)

        if module_name in self.algebraic_modules:
            self.remove_algebraic_module(module_name=module_name)
            warnings.warn(f"Overwriting algebraic module {module_name}")

        self.algebraic_modules[module_name] = {
            "function": function,
            "compounds": compounds,
            "derived_compounds": derived_compounds,
            "modifiers": modifiers,
            "parameters": parameters,
            "args": args,
        }
        for compound in derived_compounds:
            self._add_derived_compound(compound=compound)

        self.meta_info.setdefault("modules", {}).setdefault(module_name, Module(**meta_info))

    def add_algebraic_modules(self, algebraic_modules, meta_info=None):
        """Add multiple algebraic modules to the model.

        CAUTION: The Python function of the module has to return an iterable.

        Parameters
        ----------
        algebraic_modules : dict

        See Also
        --------
        add_algebraic_module
        """
        meta_info = {} if meta_info is None else meta_info
        for module_name, module in algebraic_modules.items():
            try:
                info = meta_info[module_name]
            except KeyError:
                info = {}
            self.add_algebraic_module(module_name=module_name, **module, **info)

    def update_algebraic_module(
        self,
        module_name,
        function=None,
        compounds=None,
        derived_compounds=None,
        modifiers=None,
        parameters=None,
        args=None,
    ):
        """Update an existing reaction.

        Parameters
        ----------
        module_name : str
            Name of the module
        function : callable
            Python method of the algebraic module
        compounds : iterable(str)
            Names of compounds used for module
        derived_compounds : iterable(str)
            Names of compounds which are calculated by the module
        modifiers : iterable(str)
            Names of compounds which act as modifiers on the module
        parameters : iterable(str)
            Names of the parameters which are passed to the function
        """
        module = self.algebraic_modules[module_name]
        args_have_changed = False
        if function is not None:
            patch_lambda_function_name(function=function, name=module_name)
            module["function"] = function
        if compounds is not None:
            module["compounds"] = compounds
            args_have_changed = True
        if derived_compounds is not None:
            old_compounds = module["derived_compounds"]

            # If there are now less derived compounds, remove the excess ones
            if len(derived_compounds) < len(old_compounds):
                for compound in old_compounds[len(derived_compounds) :]:
                    self.derived_compounds.remove(compound)

            # Update old derived compounds (keeping their order)
            replacements = dict(zip(old_compounds, derived_compounds))
            self.derived_compounds = [replacements.get(x, x) for x in self.derived_compounds]

            # Add new derived compounds (if there are any)
            for compound in derived_compounds[len(replacements) :]:
                self._add_derived_compound(compound=compound)

            module["derived_compounds"] = derived_compounds
            args_have_changed = True
        if modifiers is not None:
            module["modifiers"] = modifiers
            args_have_changed = True
        if parameters is not None:
            module["parameters"] = parameters
            args_have_changed = True
        if args is not None:
            module["args"] = args
        else:
            if args_have_changed:
                module["args"] = module["compounds"] + module["modifiers"] + module["parameters"]

    def update_module_meta_info(self, module, meta_info):
        """Update meta info of an algebraic module.

        Parameters
        ----------
        module : str
            Name of the algebraic module
        meta_info : dict
            Meta info of the algebraic module. Allowed keys are
            {common_name, notes, database_links}
        """
        self.update_meta_info(component="modules", meta_info={module: meta_info})

    def remove_algebraic_module(self, module_name):
        """Remove an algebraic module.

        Parameters
        ----------
        module_name : str
            Name of the algebraic module
        """
        module = self.algebraic_modules.pop(module_name)
        for compound in module["derived_compounds"]:
            self._remove_derived_compound(compound=compound)

    def remove_algebraic_modules(self, module_names):
        """Remove multiple algebraic modules.

        Parameters
        ----------
        module_names : iterable(str)
            Names of the algebraic modules
        """
        for module_name in module_names:
            self.remove_algebraic_module(module_name=module_name)

    def get_algebraic_module_compounds(self, module_name):
        """Return the compounds of the algebraic module.

        Parameters
        ----------
        module_name : str
            Name of the algebraic module

        Returns
        -------
        module_compounds : list(str)
        """
        return list(self.algebraic_modules[module_name]["compounds"])

    def get_algebraic_module_derived_compounds(self, module_name):
        """Return the derived compounds of the algebraic module.

        Parameters
        ----------
        module_name : str
            Name of the algebraic module

        Returns
        -------
        module_compounds : list(str)
            Derived compounds of the algebraic module
        """
        return list(self.algebraic_modules[module_name]["derived_compounds"])

    def get_algebraic_module_modifiers(self, module_name):
        """Return the derived compounds of the algebraic module.

        Parameters
        ----------
        module_name : str
            Name of the algebraic module

        Returns
        -------
        module_compounds : list(str)
            Derived compounds of the algebraic module
        """
        return list(self.algebraic_modules[module_name]["modifiers"])

    def get_algebraic_module_parameters(self, module_name):
        """Return the parameters of the algebraic module.

        Parameters
        ----------
        module_name : str
            Name of the algebraic module

        Returns
        -------
        parameters : list(str)
            Parameters of the algebraic module
        """
        return list(self.algebraic_modules[module_name]["parameters"])

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def _get_fcd(self, *, t, y):
        """Calculate the derived variables of all algebraic modules.

        Parameters
        ----------
        t : num, array(num)
            One are multiple time points
        y : dict(str: num)
            A dictionary of the concentrations of all non-derived compounds
        """
        y["time"] = t
        # args = self.parameters | y # that is python 3.9+ syntax, wait for a bit
        args = {**self.parameters, **y}
        for name, module in self.algebraic_modules.items():
            try:
                derived_values = module["function"](*(args[arg] for arg in module["args"]))
            except KeyError as e:
                raise KeyError(f"Could not find argument {e} for module {name}")
            derived_compounds = dict(
                zip(
                    module["derived_compounds"],
                    np.array(derived_values).reshape((len(module["derived_compounds"]), -1)),
                )
            )
            y.update(derived_compounds)
            args.update(derived_compounds)
        # return dict(set(args) - set(self.parameters)) # alternative solution, think about it
        return y

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_algebraic_modules_source_code(self, *, include_meta_info=True):
        """Generate modelbase source code for algebraic modules.

        This is mainly used for the generate_model_source_code function.

        Parameters
        ----------
        include_meta_info : bool
            Whether to include meta info in the source code.

        Returns
        -------
        algebraic_module_source_code : str
            Code generating the Python functions of the algebraic modules
        algebraic_module_modelbase_code : str
            Code generating the modelbase objects

        See Also
        --------
        generate_model_source_code
        """
        module_functions = set()
        modules = []
        for name, module in self.algebraic_modules.items():
            function = module["function"]
            compounds = module["compounds"]
            derived_compounds = module["derived_compounds"]
            modifiers = module["modifiers"]
            parameters = module["parameters"]

            function_code = get_formatted_function_source_code(
                function_name=name, function=function, function_type="module"
            )
            module_functions.add(function_code)
            module_definition = (
                "m.add_algebraic_module(\n"
                f"    module_name={repr(name)},\n"
                f"    function={function.__name__},\n"
                f"    compounds={compounds},\n"
                f"    derived_compounds={derived_compounds},\n"
                f"    modifiers={modifiers},\n"
                f"    parameters={parameters},\n"
            )
            if include_meta_info:
                meta_info = self._get_nonzero_meta_info(component="modules")
                try:
                    info = meta_info[name]
                    module_definition += f"**{info}"
                except KeyError:
                    pass
            module_definition += ")"
            modules.append(module_definition)
        return "\n".join(sorted(module_functions)), "\n".join(modules)

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_algebraic_modules(self, *, sbml_model):
        """Convert the algebraic modules their sbml equivalent.

        Notes
        -----
        The closest we can get in SBML are assignment rules of the form x = f(V), see
        http://sbml.org/Software/libSBML/docs/python-api/classlibsbml_1_1_assignment_rule.html

        Thus we have to split algebraic modules that contain multiple derived compounds
        into multiple assignment rules.

        But apparently they do not support parameters, so for now I am skipping
        this.
        """
        warnings.warn("SBML does support algebraic modules, skipping.")
