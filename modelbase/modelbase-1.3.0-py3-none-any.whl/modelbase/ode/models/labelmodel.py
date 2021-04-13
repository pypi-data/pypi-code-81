"""LabelModel base class."""

# Standard Library
import itertools as it
import warnings
from collections import defaultdict as _defaultdict

# Third party
import libsbml
import numpy as np
import pandas as pd

# Local code
from ...core.compoundmixin import Compound
from ...core.ratemixin import Rate
from ...core.utils import convert_id_to_sbml, warning_on_one_line
from .model import Model

warnings.formatwarning = warning_on_one_line


def total_concentration(*args):
    """Return concentration of all isotopomers.

    Algebraic module function to keep track of the total
    concentration of a compound (so sum of its isotopomers).
    """
    return [np.sum(args, axis=0)]


class LabelModel(Model):
    """LabelModel."""

    def __init__(
        self,
        parameters=None,
        compounds=None,
        algebraic_modules=None,
        rate_stoichiometries=None,
        rates=None,
        meta_info=None,
    ):
        self.label_compounds = {}
        self.nonlabel_compounds = []
        self.base_reactions = {}
        super().__init__(
            parameters=parameters,
            compounds=compounds,
            algebraic_modules=algebraic_modules,
            rate_stoichiometries=rate_stoichiometries,
            rates=rates,
            meta_info=meta_info,
        )

    @staticmethod
    def _generate_binary_labels(*, base_name, num_labels):
        """Create binary label string.

        Parameters
        ----------
        base_name : str
        num_labels : int

        Returns
        -------
        isotopomers : list(str)
            Returns a list of all label isotopomers of the compound

        Examples
        --------
        >>> _generate_binary_labels(base_name='cpd', num_labels=0)
        ['cpd']

        >>> _generate_binary_labels(base_name='cpd', num_labels=1)
        ['cpd__0', 'cpd__1']

        >>> _generate_binary_labels(base_name='cpd', num_labels=2)
        ['cpd__00', 'cpd__01', 'cpd__10', 'cpd__11']
        """
        if num_labels > 0:
            return [base_name + "__" + "".join(i) for i in it.product(("0", "1"), repeat=num_labels)]
        else:
            return [base_name]

    def add_compound(self, compound, is_isotopomer=False, **meta_info):
        """Add a single compound to the model.

        Parameters
        ----------
        compound : str
            Name / id of the compound
        is_isotopomer : bool
            Whether the compound is an isotopomer of a base compound
            or a non-label compound
        meta_info : dict, optional
            Meta info of the compound. Available keys are
            {common_name, compartment, formula, charge, gibbs0, smiles, database_links, notes}
        """
        super().add_compound(compound=compound, **meta_info)
        if not is_isotopomer:
            self.nonlabel_compounds.append(compound)

    def _add_base_compound(self, *, base_compound, num_labels, label_names, **meta_info):
        """Add a base compound of label isotopomer."""
        self.label_compounds[base_compound] = {
            "num_labels": num_labels,
            "isotopomers": label_names,
        }
        self.meta_info.setdefault("compounds", {}).setdefault(base_compound, Compound(**meta_info))

    def _add_isotopomers(self, *, base_compound, label_names):
        # Add all labelled compounds
        for compound in label_names:
            self.add_compound(compound=compound, is_isotopomer=True)
            del self.meta_info["compounds"][compound]

        # Create moiety for total compound concentration
        self.add_algebraic_module(
            module_name=base_compound + "__total",
            function=total_concentration,
            compounds=label_names,
            derived_compounds=[base_compound + "__total"],
            modifiers=None,
            parameters=None,
        )

    def add_label_compound(self, compound, num_labels, **meta_info):
        """Create all label isotopomers and add them as compounds.

        Also create an algebraic module that tracks the total
        concentration of that compound

        Parameters
        ----------
        base_compound : str
            Base name of the compound
        num_labels : int
            Number of labels in the compound

        Warns
        -----
        UserWarning
            If compound is already in the model
        """
        if compound in self.label_compounds:
            warnings.warn(f"Overwriting compound {compound}")
            self.remove_label_compound(compound=compound)
        if num_labels == 0:
            self.add_compound(compound=compound, is_isotopomer=False, **meta_info)
        else:
            label_names = self._generate_binary_labels(base_name=compound, num_labels=num_labels)
            self._add_base_compound(
                base_compound=compound,
                num_labels=num_labels,
                label_names=label_names,
                **meta_info,
            )
            self._add_isotopomers(base_compound=compound, label_names=label_names)

    def add_label_compounds(self, compounds, meta_info=None):
        """Add multiple label-containing compounds to the model.

        Parameters
        ----------
        compounds : dict(str, int)
            {compound: num_labels} dictionary

        Examples
        --------
        >>> add_label_compounds({"GAP": 3, "DHAP": 3, "FBP": 6})
        """
        meta_info = {} if meta_info is None else meta_info

        for compound, num_labels in compounds.items():
            try:
                info = meta_info[compound]
            except KeyError:
                info = {}
            self.add_label_compound(compound=compound, num_labels=num_labels, **info)

    def remove_compound(self, compound, is_isotopomer=False):
        """Remove a compound from the model.

        Parameters
        ----------
        compound : str
        is_isotopomer : bool
            Whether the compound is an isotopomer of a base compound
            or a non-label compound
        """
        super().remove_compound(compound=compound)
        if not is_isotopomer:
            self.nonlabel_compounds.remove(compound)

    def remove_label_compound(self, compound):
        """Remove a label compound from the model.

        Parameters
        ----------
        compound : str
            Name of the compound
        """
        label_compound = self.label_compounds.pop(compound)
        for key in label_compound["isotopomers"]:
            self.remove_compound(compound=key, is_isotopomer=True)

    def remove_label_compounds(self, compounds):
        """Remove label compounds.

        Parameters
        ----------
        compounds : iterable(str)
            Names of the compounds
        """
        for compound in compounds:
            self.remove_label_compound(compound=compound)

    def get_base_compounds(self):
        """Get all base compounds and non-label compounds.

        Returns
        -------
        base_compounds : list(str)
        """
        return sorted(list(self.label_compounds) + self.nonlabel_compounds)

    def get_compound_number_of_label_positions(self, compound):
        """Get the number of possible labels positions of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        num_labels : int
        """
        return int(self.label_compounds[compound]["num_labels"])

    def get_compound_isotopomers(self, compound):
        """Get all isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        isotopomers : list(str)
        """
        return list(self.label_compounds[compound]["isotopomers"])

    def get_compound_isotopomers_with_n_labels(self, compound, n_labels):
        """Get all isotopomers of a compound, that have excactly n labels.

        Parameters
        ----------
        compound : str

        Returns
        -------
        isotopomers : list(str)
        """
        label_positions = self.label_compounds[compound]["num_labels"]
        label_patterns = [
            ["1" if i in positions else "0" for i in range(label_positions)]
            for positions in it.combinations(range(label_positions), n_labels)
        ]
        return [f"{compound}__{''.join(i)}" for i in label_patterns]

    def get_compound_isotopomer_with_label_position(self, base_compound, label_position):
        """Get compound isotopomer with a given label position.

        Parameters
        ----------
        base_compound : str
        label_position : Union(int, iterable(int))

        Examples
        --------
        >>> add_label_compounds({"x": 2})
        >>> get_compound_isotopomer_with_label_position(x, 0) -> x__10
        >>> get_compound_isotopomer_with_label_position(x, [0]) -> x__10
        >>> get_compound_isotopomer_with_label_position(x, [0, 1]) -> x__11
        """
        if isinstance(label_position, int):
            label_position = [label_position]
        return f"{base_compound}__" + "".join(
            "1" if idx in label_position else "0" for idx in range(self.label_compounds[base_compound]["num_labels"])
        )

    @staticmethod
    def _split_label_string(label, *, labels_per_compound):
        """Split label string according to labels given in label list.

        The labels in the label list correspond to the number of
        label positions in the compound.

        Parameters
        ----------
        labels : str
        labels_per_compound : list(int)

        Examples
        --------
        >>>_split_label_string(label="01", labels_per_compound=[2])
        ["01"]

        >>>_split_label_string(label="01", labels_per_compound=[1, 1])
        ["0", "1"]

        >>>_split_label_string(label="0011", labels_per_compound=[4])
        ["0011"]

        >>>_split_label_string(label="0011", labels_per_compound=[3, 1])
        ["001", "1"]

        >>>_split_label_string(label="0011", labels_per_compound=[2, 2])
        ["00", "11"]

        >>>_split_label_string(label="0011", labels_per_compound=[1, 3])
        ["0", "011"]
        """
        split_labels = []
        cnt = 0
        for i in range(len(labels_per_compound)):
            split_labels.append(label[cnt : cnt + labels_per_compound[i]])
            cnt += labels_per_compound[i]
        return split_labels

    @staticmethod
    def _map_substrates_to_products(*, rate_suffix, labelmap):
        """Map the rate_suffix to products using the labelmap.

        Parameters
        ----------
        rate_suffix : str
        labelmap : iterable(int)
        """
        return "".join([rate_suffix[i] for i in labelmap])

    @staticmethod
    def _unpack_stoichiometries(*, stoichiometries):
        """Split stoichiometries into substrates and products.

        Parameters
        ----------
        stoichiometries : dict(str: int)

        Returns
        -------
        substrates : list(str)
        products : list(str)
        """
        substrates = []
        products = []
        for k, v in stoichiometries.items():
            if v < 0:
                substrates.extend([k] * -v)
            else:
                products.extend([k] * v)
        return substrates, products

    def _get_labels_per_compound(self, *, compounds):
        """Get labels per compound.

        This is used for _split_label string. Adds 0 for non-label compounds,
        to show that they get no label.

        Parameters
        ----------
        compounds : list(str)

        Returns
        -------
        label_per_compound : list(int)
        """
        labels_per_compound = []
        for compound in compounds:
            try:
                labels_per_compound.append(self.label_compounds[compound]["num_labels"])
            except KeyError:
                if compound not in self.get_compounds():
                    raise KeyError(f"Compound {compound} neither a compound nor a label compound")
                labels_per_compound.append(0)
        return labels_per_compound

    @staticmethod
    def _repack_stoichiometries(*, new_substrates, new_products):
        """Pack substrates and products into stoichiometric dict.

        Parameters
        ----------
        new_substrates : iterable(str)
        new_products : iterable(str)

        Returns
        -------
        stoichiometries : dict(str: int)
        """
        new_stoichiometries = _defaultdict(int)
        for arg in new_substrates:
            new_stoichiometries[arg] -= 1
        for arg in new_products:
            new_stoichiometries[arg] += 1
        return dict(new_stoichiometries)

    @staticmethod
    def _assign_compound_labels(*, base_compounds, label_suffixes):
        """Assign the correct suffixes.

        Parameters
        ----------
        base_compounds : iterable(str)
        label_suffixes : iterable(str)

        Returns
        -------
        new_compounds : list(str)
        """
        new_compounds = []
        for i, compound in enumerate(base_compounds):
            if label_suffixes[i] != "":
                new_compounds.append(compound + "__" + label_suffixes[i])
            else:
                new_compounds.append(compound)
        return new_compounds

    def add_algebraic_module(
        self,
        module_name,
        function,
        compounds=None,
        derived_compounds=None,
        modifiers=None,
        parameters=None,
    ):
        """Add an algebraic module to the model.

        CAUTION: The Python function of the module has to return an iterable.
        The Python function will get the function arguments in the following order:
        [**compounds, **modifiers, **parameters]

        CAUTION: In a LabelModel context compounds and modifiers will be mapped to
        __total if a label_compound without the isotopomer suffix is supplied.

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
        if compounds is not None:
            compounds = [i + "__total" if i in self.label_compounds else i for i in compounds]
        if modifiers is not None:
            modifiers = [i + "__total" if i in self.label_compounds else i for i in modifiers]
        super().add_algebraic_module(
            module_name=module_name,
            function=function,
            compounds=compounds,
            derived_compounds=derived_compounds,
            modifiers=modifiers,
            parameters=parameters,
        )

    def _get_external_labels(self, *, rate_name, total_product_labels, total_substrate_labels, external_labels):
        n_external_labels = total_product_labels - total_substrate_labels
        if n_external_labels > 0:
            if not external_labels:
                warnings.warn(f"Added external labels for reaction {rate_name}")
                external_label_string = ["1"] * n_external_labels
            else:
                external_label_string = ["0"] * n_external_labels
                for label_pos in external_labels:
                    external_label_string[label_pos] = "1"
            external_labels = "".join(external_label_string)
        else:
            external_labels = ""
        return external_labels

    def _add_base_reaction(
        self,
        *,
        rate_name,
        function,
        stoichiometry,
        labelmap,
        external_labels,
        modifiers,
        parameters,
        reversible,
        variants,
        **meta_info,
    ):
        self.base_reactions[rate_name] = {
            "function": function,
            "stoichiometry": stoichiometry,
            "labelmap": labelmap,
            "external_labels": external_labels,
            "modifiers": modifiers,
            "parameters": parameters,
            "reversible": reversible,
            "variants": variants,
        }
        self.meta_info.setdefault("rates", {}).setdefault(rate_name, Rate(**meta_info))

    def _create_isotopomer_reactions(
        self,
        *,
        rate_name,
        function,
        labelmap,
        modifiers,
        parameters,
        reversible,
        external_labels,
        total_substrate_labels,
        base_substrates,
        base_products,
        labels_per_substrate,
        labels_per_product,
    ):
        variants = []
        for rate_suffix in ("".join(i) for i in it.product(("0", "1"), repeat=total_substrate_labels)):
            rate_suffix += external_labels
            # This is the magic
            product_suffix = self._map_substrates_to_products(rate_suffix=rate_suffix, labelmap=labelmap)
            product_labels = self._split_label_string(label=product_suffix, labels_per_compound=labels_per_product)
            substrate_labels = self._split_label_string(label=rate_suffix, labels_per_compound=labels_per_substrate)

            new_substrates = self._assign_compound_labels(
                base_compounds=base_substrates, label_suffixes=substrate_labels
            )
            new_products = self._assign_compound_labels(base_compounds=base_products, label_suffixes=product_labels)
            new_stoichiometry = self._repack_stoichiometries(new_substrates=new_substrates, new_products=new_products)
            new_rate_name = rate_name + "__" + rate_suffix
            self.add_reaction(
                rate_name=new_rate_name,
                function=function,
                stoichiometry=new_stoichiometry,
                modifiers=modifiers,
                parameters=parameters,
                reversible=reversible,
            )
            del self.meta_info["rates"][new_rate_name]
            variants.append(new_rate_name)
        return variants

    def add_labelmap_reaction(
        self,
        rate_name,
        function,
        stoichiometry,
        labelmap,
        external_labels=None,
        modifiers=None,
        parameters=None,
        reversible=False,
        **meta_info,
    ):
        """Add a labelmap reaction.

        Parameters
        ----------
        rate_name : str
            Name of the rate function
        function : callable
            Python method calculating the rate equation
        stoichiometry : dict(str: int)
            stoichiometry of the reaction
        labelmap : iterable(int)
            Mapping of the product label positions to the substrates
        external_labels: iterable(int)
            Positions in which external labels are supposed to be inserted
        modifiers: iterable(str)
            Names of the modifiers. E.g time.
        parameters: iterable(str)
            Names of the parameters
        reversible: bool
            Whether the reaction is reversible.
        meta_info : dict, optional
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}

        Examples
        --------
        >>> add_labelmap_reaction(
                rate_name="triose-phosphate-isomerase",
                function=reversible_mass_action,
                labelmap=[2, 1, 0],
                stoichiometry={"GAP": -1, "DHAP": 1},
                parameters=["kf_TPI", "kr_TPI"],
                reversible=True,
            )
        >>> add_labelmap_reaction(
                rate_name="aldolase",
                function=reversible_mass_action_two_one,
                labelmap=[0, 1, 2, 3, 4, 5],
                stoichiometry={"DHAP": -1, "GAP": -1, "FBP": 1},
                parameters=["kf_Ald", "kr_Ald"],
                reversible=True,
            )
        """
        if modifiers is not None:
            modifiers = [i + "__total" if i in self.label_compounds else i for i in modifiers]

        base_substrates, base_products = self._unpack_stoichiometries(stoichiometries=stoichiometry)
        labels_per_substrate = self._get_labels_per_compound(compounds=base_substrates)
        labels_per_product = self._get_labels_per_compound(compounds=base_products)
        total_substrate_labels = sum(labels_per_substrate)
        total_product_labels = sum(labels_per_product)

        if len(labelmap) - total_substrate_labels < 0:
            raise ValueError(f"Labelmap 'missing' {abs(len(labelmap) - total_substrate_labels)} label(s)")

        external_labels = self._get_external_labels(
            rate_name=rate_name,
            total_product_labels=total_product_labels,
            total_substrate_labels=total_substrate_labels,
            external_labels=external_labels,
        )

        variants = self._create_isotopomer_reactions(
            rate_name=rate_name,
            function=function,
            labelmap=labelmap,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            external_labels=external_labels,
            total_substrate_labels=total_substrate_labels,
            base_substrates=base_substrates,
            base_products=base_products,
            labels_per_substrate=labels_per_substrate,
            labels_per_product=labels_per_product,
        )

        self._add_base_reaction(
            rate_name=rate_name,
            function=function,
            stoichiometry=stoichiometry,
            labelmap=labelmap,
            external_labels=external_labels,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
            variants=variants,
            **meta_info,
        )

    def update_labelmap_reaction(
        self,
        rate_name,
        function=None,
        stoichiometry=None,
        labelmap=None,
        modifiers=None,
        parameters=None,
        reversible=None,
        **meta_info,
    ):
        """Update an existing labelmap reaction.

        Parameters
        ----------
        rate_name : str
            Name of the rate function
        function : callable, optional
            Python method calculating the rate equation
        stoichiometry : dict(str: int), optional
            stoichiometry of the reaction
        labelmap : iterable(int), optional
            Mapping of the product label positions to the substrates
        external_labels: iterable(int), optional
            Positions in which external labels are supposed to be inserted
        modifiers: iterable(str), optional
            Names of the modifiers. E.g time.
        parameters: iterable(str), optional
            Names of the parameters
        reversible: bool, optional
            Whether the reaction is reversible.
        meta_info : dict, optional
            Meta info of the rate. Allowed keys are
            {common_name, gibbs0, ec, database_links, notes, sbml_function}
        """
        if function is None:
            function = self.base_reactions[rate_name]["function"]
        if stoichiometry is None:
            stoichiometry = self.base_reactions[rate_name]["stoichiometry"]
        if labelmap is None:
            labelmap = self.base_reactions[rate_name]["labelmap"]
        if modifiers is None:
            modifiers = self.base_reactions[rate_name]["modifiers"]
        if parameters is None:
            parameters = self.base_reactions[rate_name]["parameters"]
        if reversible is None:
            reversible = self.base_reactions[rate_name]["reversible"]
        meta = self.meta_info["rates"][rate_name].__dict__
        meta.update(meta_info)

        self.remove_labelmap_reaction(rate_name=rate_name)
        self.add_labelmap_reaction(
            rate_name=rate_name,
            function=function,
            stoichiometry=stoichiometry,
            labelmap=labelmap,
            modifiers=modifiers,
            parameters=parameters,
            reversible=reversible,
        )

    def remove_labelmap_reaction(self, rate_name):
        """Remove all variants of a base reaction.

        Parameters
        ----------
        rate_name : str
            Name of the rate
        """
        self.meta_info["rates"].pop(rate_name)
        base_reaction = self.base_reactions.pop(rate_name)
        for rate in base_reaction["variants"]:
            if rate.startswith(rate_name):
                self.remove_reaction(rate_name=rate)

    def remove_labelmap_reactions(self, rate_names):
        """Remove all variants of a multiple labelmap reactions.

        Parameters
        ----------
        rate_names : iterable(str)

        See Also
        --------
        remove_labelmap_reaction
        """
        for rate_name in rate_names:
            self.remove_labelmap_reaction(rate_name=rate_name)

    # Simulation functions
    def generate_y0(self, base_y0, label_positions=None):
        """Generate y0 for all isotopomers given a base y0.

        Parameters
        ----------
        base_y0 : dict(str: num)
        label_positions: dict(str: num)

        Returns
        -------
        y0 : dict(str: num)

        Examples
        --------
        >>> base_y0 = {"GAP": 1, "DHAP": 0, "FBP": 0}
        >>> generate_y0(base_y0=base_y0, label_positions={"GAP": 0})
        """
        if label_positions is None:
            label_positions = {}
        if not isinstance(base_y0, dict):
            base_y0 = dict(zip(self.label_compounds, base_y0))

        y0 = dict(zip(self.get_compounds(), np.zeros(len(self.get_compounds()))))
        for base_compound, concentration in base_y0.items():
            label_position = label_positions.get(base_compound, None)
            if label_position is None:
                try:
                    y0[self.label_compounds[base_compound]["isotopomers"][0]] = concentration
                except KeyError:  # non label compound
                    y0[base_compound] = concentration
            else:
                if isinstance(label_position, int):
                    label_position = [label_position]
                suffix = "__" + "".join(
                    "1" if idx in label_position else "0"
                    for idx in range(self.label_compounds[base_compound]["num_labels"])
                )
                y0[base_compound + suffix] = concentration
        return y0

    def get_total_fluxes(self, rate_base_name, y, t=0):
        """Get total fluxes of a base rate.

        Parameters
        ----------
        rate_base_name : str
        y : Union(iterable(num), dict(str: num))
        t : Union(num, iterable(num))

        Returns
        -------
        fluxes : numpy.array
        """
        rates = [i for i in self.rates if i.startswith(rate_base_name + "__")]
        return self.get_fluxes_df(y=y, t=t)[rates].sum(axis=1).values

    def _create_label_scope_seed(self, *, initial_labels):
        """Create initial label scope seed.

        Parameters
        ----------
        initial_labels : iterable(str)

        Returns
        -------
        labelled_compounds : set(str)
        """
        initial_labels = [
            self.get_compound_isotopomer_with_label_position(base_compound=base_compound, label_position=label_position)
            for base_compound, label_position in initial_labels.items()
        ]

        # initialise all compounds with 0 (no label)
        labelled_compounds = {compound: 0 for compound in self.get_compounds()}

        # Set all unlabelled compounds to 1
        for compound, cpd_dict in self.label_compounds.items():
            num_labels = cpd_dict["num_labels"]
            labelled_compounds[f"{compound}__{'0' * num_labels}"] = 1
        # Also set all non-label compounds to 1
        for compound in self.nonlabel_compounds:
            labelled_compounds[compound] = 1
        # Set initial label
        for i in initial_labels:
            labelled_compounds[i] = 1
        return labelled_compounds

    def get_label_scope(self, initial_labels):
        """Return all label positions that can be reached step by step.

        Parameters
        ----------
        initial_labels : dict(str: num)

        Returns
        -------
        label_scope : dict{step : set of new positions}

        Examples
        --------
        >>> l.get_label_scope({"x": 0})
        >>> l.get_label_scope({"x": [0, 1], "y": 0})
        """
        labelled_compounds = self._create_label_scope_seed(initial_labels=initial_labels)
        new_labels = set("non empty entry to not fulfill while condition")
        # Loop until no new labels are inserted
        loop_count = 0
        result = {}
        while new_labels != set():
            new_cpds = labelled_compounds.copy()
            for rec, cpd_dict in self.get_stoichiometries().items():
                # Isolate substrates
                cpds = [i for i, j in cpd_dict.items() if j < 0]
                # Count how many of the substrates are 1
                i = 0
                for j in cpds:
                    i += labelled_compounds[j]
                # If all substrates are 1, set all products to 1
                if i == len(cpds):
                    for cpd in self.get_stoichiometries()[rec]:
                        new_cpds[cpd] = 1
                if self.rates[rec]["reversible"]:
                    # Isolate substrates
                    cpds = [i for i, j in cpd_dict.items() if j > 0]
                    # Count how many of the substrates are 1
                    i = 0
                    for j in cpds:
                        i += labelled_compounds[j]
                    # If all substrates are 1, set all products to 1
                    if i == len(cpds):
                        for cpd in self.get_stoichiometries()[rec]:
                            new_cpds[cpd] = 1
            # Isolate "old" labels
            s1 = pd.Series(labelled_compounds)
            s1 = s1[s1 == 1]
            # Isolate new labels
            s2 = pd.Series(new_cpds)
            s2 = s2[s2 == 1]
            # Find new labels
            new_labels = set(s2.index).difference(set(s1.index))
            # Break the loop once no new labels can be found
            if new_labels == set():
                break
            else:
                labelled_compounds = new_cpds
                result[loop_count] = new_labels
                loop_count += 1
        return result

    ##########################################################################
    # Model conversion functions
    ##########################################################################

    def _map_label_compound_to_compound(self, *, compound):
        if compound in self.nonlabel_compounds:
            return compound
        else:
            return compound.rsplit("__")[0]

    def to_model(self):
        """Convert LabelModel to Model."""
        m = Model()
        m.add_parameters(self.parameters)
        m.add_compounds(list(self.label_compounds.keys()))
        m.add_compounds(self.nonlabel_compounds)

        for module_name, module in self.algebraic_modules.items():
            if not module_name.endswith("__total"):
                module = module.copy()
                module["compounds"] = [self._map_label_compound_to_compound(compound=i) for i in module["compounds"]]
                module["derived_compounds"] = [
                    self._map_label_compound_to_compound(compound=i) for i in module["derived_compounds"]
                ]
                module["modifiers"] = [self._map_label_compound_to_compound(compound=i) for i in module["modifiers"]]
                m.add_algebraic_module(module_name=module_name, **module)

        for rate_name, reaction in self.base_reactions.items():
            reaction = reaction.copy()
            reaction["stoichiometry"] = {
                self._map_label_compound_to_compound(compound=k): v for k, v in reaction["stoichiometry"].items()
            }
            reaction["modifiers"] = [self._map_label_compound_to_compound(compound=i) for i in reaction["modifiers"]]
            del reaction["labelmap"]
            del reaction["external_labels"]
            del reaction["variants"]
            m.add_reaction(rate_name=rate_name, **reaction)
        return m

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _add_sbml_compound(self, *, sbml_model, compound_id, common_name, compartment, charge, formula):
        cpd = sbml_model.createSpecies()
        cpd.setId(convert_id_to_sbml(id_=compound_id, prefix="CPD"))
        if common_name is not None:
            cpd.setName(common_name)
        cpd.setConstant(False)
        cpd.setBoundaryCondition(False)
        cpd.setHasOnlySubstanceUnits(False)
        cpd.setCompartment(compartment)

        cpd_fbc = cpd.getPlugin("fbc")
        if charge is not None:
            cpd_fbc.setCharge(int(charge))
        if formula is not None:
            cpd_fbc.setChemicalFormula(formula)

    def _create_sbml_compounds(self, *, sbml_model):
        """Create the compounds for the sbml model.

        Parameters
        ----------
        sbml_model : libsbml.Model
        """
        for base_compound_id, base_compound in self.label_compounds.items():
            compound = self.meta_info["compounds"][base_compound_id]
            common_name = compound.common_name
            charge = compound.charge
            formula = compound.formula
            compartment = compound.compartment

            for compound_id in base_compound["isotopomers"]:
                self._add_sbml_compound(
                    sbml_model=sbml_model,
                    compound_id=compound_id,
                    common_name=common_name,
                    compartment=compartment,
                    charge=charge,
                    formula=formula,
                )

        for compound_id in self.nonlabel_compounds:
            compound = self.meta_info["compounds"][compound_id]
            common_name = compound.common_name
            charge = compound.charge
            formula = compound.formula
            compartment = compound.compartment
            self._add_sbml_compound(
                sbml_model=sbml_model,
                compound_id=compound_id,
                common_name=common_name,
                compartment=compartment,
                charge=charge,
                formula=formula,
            )

    def _create_sbml_reactions(self, *, sbml_model):
        """Create the reactions for the sbml model.

        Parameters
        ----------
        sbml_model : libsbml.Model
        """
        for base_rate_id, base_rate in self.base_reactions.items():
            rate = self.meta_info["rates"][base_rate_id]
            name = rate.common_name
            # function = rate.sbml_function
            reversible = base_rate["reversible"]

            for rate_id in base_rate["variants"]:
                stoichiometry = self.stoichiometries[rate_id]
                rxn = sbml_model.createReaction()
                rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))
                if name:
                    rxn.setName(name)
                rxn.setFast(False)
                rxn.setReversible(reversible)

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

                # if function is not None:
                #     kinetic_law = rxn.createKineticLaw()
                #     kinetic_law.setMath(libsbml.parseL3Formula(function))
