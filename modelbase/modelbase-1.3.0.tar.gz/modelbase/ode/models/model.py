"""Main ODE model module.

Description of the module
"""

# Standard Library
import subprocess
import warnings

# Third party
import libsbml
import numpy as np
import pandas as pd

# Local code
from ...core import (
    AlgebraicMixin,
    BaseModel,
    CompoundMixin,
    ParameterMixin,
    RateMixin,
    StoichiometricMixin,
)
from ...core.utils import convert_id_to_sbml


class Model(
    RateMixin,
    StoichiometricMixin,
    AlgebraicMixin,
    ParameterMixin,
    CompoundMixin,
    BaseModel,
):
    """The main class for modeling. Provides model construction and inspection tools."""

    def __init__(
        self,
        parameters=None,
        compounds=None,
        algebraic_modules=None,
        rate_stoichiometries=None,
        rates=None,
        functions=None,
        meta_info=None,
    ):
        BaseModel.__init__(self, meta_info=meta_info)
        CompoundMixin.__init__(self, compounds=compounds)
        ParameterMixin.__init__(self, parameters=parameters)
        AlgebraicMixin.__init__(self, algebraic_modules=algebraic_modules)
        StoichiometricMixin.__init__(self, rate_stoichiometries=rate_stoichiometries)
        RateMixin.__init__(self, rates=rates, functions=functions)
        self.meta_info["model"].sbo = "SBO:0000062"  # continuous framework

    def __str__(self):
        """Give a string representation.

        Returns
        -------
        representation : str
        """
        return (
            "Model:"
            + f"\n    {len(self.get_compounds())} Compounds"
            + f"\n    {len(self.get_stoichiometries())} Reactions"
        )

    ##########################################################################
    # Reactions
    ##########################################################################

    def add_reaction(
        self,
        rate_name,
        function,
        stoichiometry,
        modifiers=None,
        dynamic_variables=None,
        parameters=None,
        reversible=False,
        **meta_info,
    ):
        """Add a reaction to the model.

        Shortcut for add_rate and add stoichiometry functions.
        Additional variable ["time"] can be passed for time-dependent functions.

        Parameters
        ----------
        rate_name : str
        function : callable
        stoichiometry : dict
        modifiers: iterable(str)
        parameters: iterable(str)
        reversible: bool

        See Also
        --------
        add_rate
        add_stoichiometry

        Examples
        --------
        >>> add_reaction(
                rate_name="v1",
                function=mass_action,
                stoichiometry={"X": -1, "Y": 1},
                parameters=["k2"],
            )
        >>> add_reaction(
                rate_name="v1",
                function=reversible_mass_action,
                stoichiometry={"X": -1, "Y": 1},
                parameters=["k1_fwd", "k1_bwd"],
                reversible=True,
            )
        """
        substrates = [k for k, v in stoichiometry.items() if v < 0]
        products = [k for k, v in stoichiometry.items() if v > 0]

        self.add_rate(
            rate_name=rate_name,
            function=function,
            substrates=substrates,
            products=products,
            dynamic_variables=dynamic_variables,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            **meta_info,
        )
        self.add_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

    def update_reaction(
        self,
        rate_name,
        function=None,
        stoichiometry=None,
        modifiers=None,
        dynamic_variables=None,
        parameters=None,
        reversible=None,
        **meta_info,
    ):
        """Update an existing reaction.

        Parameters
        ----------
        rate_name : str
        function : callable, optional
        stoichiometry : dict, optional
        modifiers: iterable(str), optional
        parameters: iterable(str), optional
        reversible: bool, optional

        See Also
        --------
        add_reaction
        update_rate
        update_stoichiometry
        """
        if function is None:
            function = self.rates[rate_name]["function"]
        if stoichiometry is None:
            stoichiometry = self.stoichiometries[rate_name]
        if modifiers is None:
            modifiers = self.rates[rate_name]["modifiers"]
        if parameters is None:
            parameters = self.rates[rate_name]["parameters"]
        if reversible is None:
            reversible = self.rates[rate_name]["reversible"]
        meta = self.meta_info["rates"][rate_name].__dict__
        meta.update(meta_info)
        self.remove_reaction(rate_name=rate_name)
        self.add_reaction(
            rate_name=rate_name,
            function=function,
            stoichiometry=stoichiometry,
            modifiers=modifiers,
            dynamic_variables=dynamic_variables,
            parameters=parameters,
            reversible=reversible,
            **meta,
        )

    def add_reaction_from_ratelaw(self, rate_name, ratelaw, **meta_info):
        """Add a reaction from a ratelaw.

        Parameters
        ----------
        rate_name : str
        ratelaw : modelbase.ode.utils.ratelaw.BaseRateLaw
            Ratelaw instance
        meta_info : dict, optional

        Examples
        --------
        >>> add_reaction_from_ratelaw(
                rate_name="v1",
                ratelaw=ReversibleMassAction(
                    substrates=["X"],
                    products=["Y"],
                    k_fwd="k1p",
                    k_bwd="k1m"
                ),
            )
        """
        default_meta_info = {"sbml_function": ratelaw.get_sbml_function_string()}
        default_meta_info.update(meta_info)

        self.add_rate(
            rate_name=rate_name,
            function=ratelaw.get_rate_function(),
            substrates=ratelaw.substrates,
            products=ratelaw.products,
            modifiers=ratelaw.modifiers,
            parameters=ratelaw.parameters,
            reversible=ratelaw.reversible,
            **default_meta_info,
        )
        self.add_stoichiometry(rate_name=rate_name, stoichiometry=ratelaw.stoichiometry)

    def remove_reaction(self, rate_name):
        """Remove a reaction from the model.

        Parameters
        ----------
        rate_name : str
        """
        self.remove_rate(rate_name=rate_name)
        self.remove_rate_stoichiometry(rate_name=rate_name)

    def remove_reactions(self, rate_names):
        """Remove multiple reactions from the model.

        Parameters
        ----------
        names : iterable(str)
        """
        for rate_name in rate_names:
            self.remove_reaction(rate_name=rate_name)

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def get_full_concentration_dict(self, y, t=0):
        """Calculate the derived variables (at time(s) t).

        Parameters
        ----------
        y : Union(dict(str: num), iterable(num))
        t : Union(num, iterable(num)), optional

        Returns
        -------
        y_full : dict
            Dictionary of the concentrations of all compounds and derived compounds

        Example
        -------
        >>> get_full_concentration_dict(y=[0, 0])
        >>> get_full_concentration_dict(y={"X": 0, "Y": 0})
        """
        self._update_derived_parameters()
        if isinstance(t, (int, float)):
            t = [t]
        t = np.array(t)
        if isinstance(y, dict):
            y = {k: np.ones(len(t)) * v for k, v in y.items()}
        else:
            y = dict(zip(self.get_compounds(), (np.ones((len(t), 1)) * y).T))
        return {k: np.ones(len(t)) * v for k, v in self._get_fcd(t=t, y=y).items()}

    def get_fluxes_dict(self, y, t=0):
        """Calculate the fluxes at time point(s) t.

        Parameters
        ----------
        y : Union(dict(str: num), iterable(num))
        t : Union(num, iterable(num))

        Returns
        -------
        fluxes : dict
        """
        self._update_derived_parameters()
        fcd = self.get_full_concentration_dict(y=y, t=t)
        return {k: np.ones(len(fcd["time"])) * v for k, v in self._get_fluxes(fcd=fcd).items()}

    def get_fluxes_array(self, y, t=0):
        """Calculate the fluxes at time point(s) t.

        Parameters
        ----------
        y : Union(dict(str: num), iterable(num))
        t : Union(num, iterable(num))

        Returns
        -------
        fluxes : numpy.array
        """
        return np.array([i for i in self.get_fluxes_dict(y=y, t=t).values()]).T

    def get_fluxes_df(self, y, t=0):
        """Calculate the fluxes at time point(s) t.

        Parameters
        ----------
        y : Union(dict(str: num), iterable(num))
        t : Union(num, iterable(num))

        Returns
        -------
        fluxes : pandas.DataFrame
        """
        if isinstance(t, (int, float)):
            t = [t]
        return pd.DataFrame(data=self.get_fluxes_dict(y=y, t=t), index=t, columns=self.get_rate_names())

    # This can't get keyword-only arguments, as the integrators are calling it with
    # positional arguments
    def _get_rhs(self, t, y):
        """Calculate the right hand side of the ODE system.

        This is the more performant version of get_right_hand_side()
        and thus returns only an array instead of a dictionary.

        Watch out that this function swaps t and y!

        Parameters
        ----------
        t : num
        y : iterable(num)

        Returns
        -------
        rhs : list
            List of the right hand side
        """
        y = dict(zip(self.get_compounds(), np.array(y).reshape(-1, 1)))
        fcd = self._get_fcd(t=t, y=y)
        fluxes = self._get_fluxes(fcd=fcd)
        compounds_local = self.get_compounds()
        dxdt = dict(zip(compounds_local, np.zeros(len(compounds_local))))
        for k, stoc in self.stoichiometries_by_compounds.items():
            for flux, n in stoc.items():
                dxdt[k] += n * fluxes[flux]
        return np.array([dxdt[i] for i in compounds_local]).flatten()

    def get_right_hand_side(self, y, t=0):
        """Calculate the right hand side of the ODE system.

        Parameters
        ----------
        y : Union(dict(str: num), iterable(num))
        t : Union(num, iterable(num))
        """
        self._update_derived_parameters()
        y = self.get_full_concentration_dict(y=y, t=t)
        y = [y[i] for i in self.get_compounds()]
        rhs = self._get_rhs(t=t, y=y)
        eqs = [f"d{cpd}dt" for cpd in self.get_compounds()]
        return dict(zip(eqs, rhs))

    ##########################################################################
    # Model conversion functions
    ##########################################################################

    def to_labelmodel(self, labelcompounds, labelmaps):
        """Create a LabelModel from this model.

        Parameters
        ----------
        labelcompounds : dict
            Mapping compound to the amount of labels they can carry
        labelmaps : dict
            Mapping reaction to labelmap

        Returns
        -------
        LabelModel: modelbase.ode.LabelModel

        Examples
        --------
        >>> m = Model()
        >>> m.add_reaction(
                rate_name="TPI",
                function=reversible_mass_action_1_1,
                stoichiometry={"GAP": -1, "DHAP": 1},
                parameters=["kf_TPI", "kr_TPI"],
                reversible=True,
            )
        >>> labelcompounds = {"GAP": 3, "DHAP": 3}
        >>> labelmaps = {"TPI": [2, 1, 0]}
        >>> m.to_labelmodel(labelcompounds=labelcompounds, labelmaps=labelmaps)
        """
        # Third party
        from modelbase.ode import LabelModel

        lm = LabelModel()
        lm.add_parameters(self.parameters)
        for compound in self.get_compounds():
            if compound in labelcompounds:
                lm.add_label_compound(compound=compound, num_labels=labelcompounds[compound])
            else:
                lm.add_compound(compound=compound)

        for module_name, module in self.algebraic_modules.items():
            lm.add_algebraic_module(
                module_name=module_name,
                function=module["function"],
                compounds=module["compounds"],
                derived_compounds=module["derived_compounds"],
                modifiers=module["modifiers"],
                parameters=module["parameters"],
            )

        for rate_name, rate_dict in self.rates.items():
            if rate_name not in labelmaps:
                lm.add_reaction(
                    rate_name=rate_name,
                    function=rate_dict["function"],
                    stoichiometry=self.stoichiometries[rate_name],
                    modifiers=rate_dict["modifiers"],
                    parameters=rate_dict["parameters"],
                    reversible=rate_dict["reversible"],
                )
            else:
                lm.add_labelmap_reaction(
                    rate_name=rate_name,
                    function=rate_dict["function"],
                    stoichiometry=self.stoichiometries[rate_name],
                    labelmap=labelmaps[rate_name],
                    modifiers=rate_dict["modifiers"],
                    parameters=rate_dict["parameters"],
                    reversible=rate_dict["reversible"],
                )
        return lm

    def to_linear_labelmodel(self, labelcompounds, labelmaps):
        """Create a LinearLabelModel from this model.

        Watch out that for a linear label model reversible reactions have to be split
        into a forward and backward part.

        Parameters
        ----------
        labelcompounds : dict
            Mapping compound to the amount of labels they can carry
        labelmaps : dict
            Mapping reaction to labelmap

        Returns
        -------
        LabelModel: modelbase.ode.LabelModel

        Examples
        --------
        >>> m = Model()
        >>> m.add_reaction(
                rate_name="TPI_fwd",
                function=_mass_action_1_1,
                stoichiometry={"GAP": -1, "DHAP": 1},
                parameters=["kf_TPI"],
            )
        >>> m.add_reaction(
                rate_name="TPI_bwd",
                function=mass_action_1_1,
                stoichiometry={"DHAP": -1, "GAP": 1},
                parameters=["kr_TPI"],
            )
        >>> labelcompounds = {"GAP": 3, "DHAP": 3}
        >>> labelmaps = {"TPI_fwd": [2, 1, 0], 'TPI_bwd': [2, 1, 0]}
        >>> m.to_linear_labelmodel(labelcompounds=labelcompounds, labelmaps=labelmaps)
        """
        # Third party
        from modelbase.ode import LinearLabelModel

        lm = LinearLabelModel()
        for compound in self.get_compounds():
            if compound in labelcompounds:
                lm.add_compound(compound=compound, num_labels=labelcompounds[compound])

        for rate_name, rate_dict in self.rates.items():
            if rate_name in labelmaps:
                if rate_dict["reversible"]:
                    warnings.warn(
                        f"Reaction {rate_name} is annotated as reversible. "
                        "Did you remember to split it into a forward and backward part?"
                    )
                lm.add_reaction(
                    rate_name=rate_name,
                    stoichiometry={
                        k: v for k, v in self.stoichiometries[rate_name].items() if k in labelcompounds
                    },
                    labelmap=labelmaps[rate_name],
                )
            else:
                warnings.warn(f"Skipping reaction {rate_name} as no labelmap is given")
        return lm

    ##########################################################################
    # Source code functions
    ##########################################################################

    def generate_model_source_code(self, linted=True, include_meta_info=False):
        """Generate source code of the model.

        Parameters
        ----------
        linted : bool
            Whether the source code should be formatted via black.
            Usually it only makes sense to turn this off if there is an error somewhere.
        include_meta_info : bool
            Whether to include meta info of the model components

        Returns
        -------
        model_source_code : str
        """
        parameters = self._generate_parameters_source_code(include_meta_info=include_meta_info)
        compounds = self._generate_compounds_source_code(include_meta_info=include_meta_info)
        functions = self._generate_function_source_code()
        module_functions, modules = self._generate_algebraic_modules_source_code(
            include_meta_info=include_meta_info
        )
        rate_functions, rates = self._generate_rates_source_code(include_meta_info=include_meta_info)
        stoichiometries = self._generate_stoichiometries_source_code()

        model_string = "\n".join(
            (
                "import math",
                "import numpy as np",
                "from modelbase.ode import Model, Simulator",
                functions,
                module_functions,
                rate_functions,
                "m = Model()",
                parameters,
                compounds,
                modules,
                rates,
                stoichiometries,
            )
        )
        if linted:
            blacked_string = subprocess.run(["black", "-c", model_string], stdout=subprocess.PIPE)
            return blacked_string.stdout.decode("utf-8")
        else:
            return model_string

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_reactions(self, *, sbml_model):
        """Create the reactions for the sbml model.

        Parameters
        ----------
        sbml_model : libsbml.Model
        """
        for rate_id, stoichiometry in self.stoichiometries.items():
            rate = self.meta_info["rates"][rate_id]
            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))
            name = rate.common_name
            if name:
                rxn.setName(name)
            rxn.setFast(False)
            rxn.setReversible(self.rates[rate_id]["reversible"])

            for compound_id, factor in stoichiometry.items():
                if factor < 0:
                    sref = rxn.createReactant()
                else:
                    sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound_id, prefix="CPD"))
                sref.setStoichiometry(abs(factor))
                sref.setConstant(False)

            for compound in self.rates[rate_id]["modifiers"]:
                sref = rxn.createModifier()
                sref.setSpecies(convert_id_to_sbml(id_=compound, prefix="CPD"))

            function = rate.sbml_function
            if function is not None:
                kinetic_law = rxn.createKineticLaw()
                kinetic_law.setMath(libsbml.parseL3Formula(function))

    def _model_to_sbml(self):
        """Export model to sbml."""
        doc = self._create_sbml_document()
        sbml_model = self._create_sbml_model(doc=doc)
        self._create_sbml_units(sbml_model=sbml_model)
        self._create_sbml_compartments(sbml_model=sbml_model)
        self._create_sbml_compounds(sbml_model=sbml_model)
        if bool(self.algebraic_modules):
            self._create_sbml_algebraic_modules(sbml_model=sbml_model)
        self._create_sbml_reactions(sbml_model=sbml_model)
        return doc
