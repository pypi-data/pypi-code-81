"""Mixin for stoichiometries."""

# Standard Library
import warnings

# Third party
import numpy as np
import pandas as pd

# Local code
from .utils import convert_id_to_sbml, warning_on_one_line

warnings.formatwarning = warning_on_one_line


class StoichiometricMixin:
    """Mixin for stoichiometries."""

    def __init__(self, rate_stoichiometries=None):
        self.stoichiometries = {}
        self.stoichiometries_by_compounds = {}
        if rate_stoichiometries is not None:
            self.add_stoichiometries(rate_stoichiometries=rate_stoichiometries)

    ##########################################################################
    # Stoichiometries
    ##########################################################################

    def add_stoichiometry(self, rate_name, stoichiometry):
        """Add the stoichiometry of a rate to the model.

        Parameters
        ----------
        rate_name : str
            Name of the rate
        stoichiometries : dict(str: int)
            Dictionary containing the compound:stoichiometry pair(s)

        Examples
        --------
        add_stoichiometry(rate_name="v1", stoichiometry={"x": 1})
        """
        if rate_name in self.stoichiometries:
            warnings.warn(f"Overwriting stoichiometry for rate {rate_name}")
            self.remove_rate_stoichiometry(rate_name=rate_name)

        # Stoichiometries
        self.stoichiometries[rate_name] = stoichiometry

        # Stoichiometries by compounds
        for compound, factor in stoichiometry.items():
            self.stoichiometries_by_compounds.setdefault(compound, {})[rate_name] = factor

    def add_stoichiometry_by_compound(self, compound, stoichiometry):
        """Add the stoichiometry of compound to the model.

        Parameters
        ----------
        compound : str
        stoichiometry : dict(str: int)
            Dictionary containing the {rate_name:stoichiometry}

        Examples
        --------
        add_stoichiometry_by_compoundcompound="x", stoichiometry={"v1": 1})
        """
        if compound in self.stoichiometries_by_compounds:
            warnings.warn(f"Overwriting stoichiometry for compound {compound}")
            self.remove_compound_stoichiometry(compound=compound)

        self.stoichiometries_by_compounds[compound] = stoichiometry

        for rate, factor in stoichiometry.items():
            self.stoichiometries.setdefault(rate, {})[compound] = factor

    def add_stoichiometries(self, rate_stoichiometries):
        """Add the stoichiometry of multiple rates.

        Parameters
        ----------
        rate_stoichiometries : dict(str: dict(str: int))
            Dictionary containing the {rate_name:{compound:stoichiometry}} pair(s)

        Examples
        --------
        add_stoichiometries(
            rate_stoichiometries={
                "v1": {"x": -1, "y": 1},
                "v2": {"x": 1, "y": -1}
            }
        )
        """
        for rate_name, stoichiometry in rate_stoichiometries.items():
            self.add_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)

    def add_stoichiometries_by_compounds(self, compound_stoichiometries):
        """Add the stoichiometry of multiple compounds to the model.

        Parameters
        ----------
        compound_stoichiometries : dict(str: dict(str: int))
            Dictionary containing the {compound:{rate_name:stoichiometry}} pair(s)

        Examples
        --------
        add_stoichiometries_by_compounds(
            compound_stoichiometries={
                "x": {"v1": -1, "v2": 1},
                "y": {"v1": 1, "v2": -1}
            }
        )
        """
        for compound, stoichiometry in compound_stoichiometries.items():
            self.add_stoichiometry_by_compound(compound=compound, stoichiometry=stoichiometry)

    def remove_rate_stoichiometry(self, rate_name):
        """Remove a rate stoichiometry from the model.

        Parameters
        ----------
        rate_name : str
            Name of the rate
        """
        compounds = self.stoichiometries.pop(rate_name)
        for compound in compounds:
            del self.stoichiometries_by_compounds[compound][rate_name]
            if not bool(self.stoichiometries_by_compounds[compound]):
                del self.stoichiometries_by_compounds[compound]

    def remove_rate_stoichiometries(self, rate_names):
        """Remove multiple rate stoichiometries from the model.

        Parameters
        ----------
        rate_names : iterable(str)
            Names of the rates
        """
        for rate_name in rate_names:
            self.remove_rate_stoichiometry(rate_name=rate_name)

    def remove_compound_stoichiometry(self, compound):
        """Remove stoichiometry of a compound.

        Parameters
        ----------
        compound : str
            Name of the compound
        """
        rates = self.stoichiometries_by_compounds.pop(compound)
        for rate in rates:
            del self.stoichiometries[rate][compound]
            if not bool(self.stoichiometries[rate]):
                del self.stoichiometries[rate]

    def remove_compound_stoichiometries(self, compounds):
        """Remove stoichiometry of multiple compounds.

        Parameters
        ----------
        compounds : iterable(str)
            Names of the compounds
        """
        for compound in compounds:
            self.remove_compound_stoichiometry(compound=compound)

    def get_rate_stoichiometry(self, rate_name):
        """Get stoichiometry of a rate.

        Parameters
        ----------
        rate_name : str

        Returns
        -------
        stoichiometries : dict(str: int)
        """
        return dict(self.stoichiometries[rate_name])

    def get_compound_stoichiometry(self, compound):
        """Get stoichiometry of a compound.

        Parameters
        ----------
        rate_name : str

        Returns
        -------
        stoichiometries : dict(str: int)
        """
        return dict(self.stoichiometries_by_compounds[compound])

    def get_stoichiometries(self):
        """Return stoichiometries ordered by reactions.

        Returns
        -------
        stoichiometries : dict(str: dict(str: int))
            Stoichiometries sorted by reactions
        """
        return dict(self.stoichiometries)

    def get_stoichiometries_by_compounds(self):
        """Return stoichiometries ordered by compounds.

        Returns
        -------
        stoichiometries : dict(str: dict(str: int))
            Stoichiometries sorted by compounds
        """
        return dict(self.stoichiometries_by_compounds)

    def get_stoichiometric_matrix(self):
        """Return the stoichiometric matrix.

        Returns
        -------
        stoichiometric_matrix : numpy.ndarray
        """
        compound_indexes = {v: k for k, v in enumerate(sorted(self.get_compounds()))}
        M = np.zeros(shape=[len(self.get_compounds()), len(self.stoichiometries)])
        for stoich_idx, rate_name in enumerate(sorted(self.stoichiometries)):
            cpd_stoich = self.stoichiometries[rate_name]
            for cpd, stoich in cpd_stoich.items():
                M[compound_indexes[cpd], stoich_idx] = stoich
        return M

    def get_stoichiometric_df(self):
        """Return the stoichiometric matrix as a pandas DataFrame.

        Returns
        -------
        stoichiometric_matrix : pandas.DataFrame
        """
        return pd.DataFrame(
            data=self.get_stoichiometric_matrix(),
            index=sorted(self.get_compounds()),
            columns=sorted(self.stoichiometries),
        )

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_stoichiometries_source_code(self):
        """Generate modelbase source code for stoichiometries.

        This is mainly used for the generate_model_source_code function.

        Returns
        -------
        stoichiometries_modelbase_code : str
            Code generating the modelbase objects

        See Also
        --------
        generate_model_source_code
        """
        return f"m.add_stoichiometries(rate_stoichiometries={repr(self.stoichiometries)})"

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_stoichiometries(self, *, sbml_model):
        """Create the reactions for the sbml model.

        Parameters
        ----------
        sbml_model : libsbml.Model
        """
        for rate_id, stoichiometry in self.stoichiometries.items():
            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))

            for compound_id, factor in stoichiometry.items():
                if factor < 0:
                    sref = rxn.createReactant()
                else:
                    sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound_id, prefix="CPD"))
                sref.setStoichiometry(abs(factor))
                sref.setConstant(True)
