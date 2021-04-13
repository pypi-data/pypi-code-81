# Standard Library
from abc import ABC, abstractmethod
from collections import defaultdict

# Local code
from . import ratefunctions


def _pack_stoichiometries(substrates, products):
    new_stoichiometries = defaultdict(int)
    for arg in substrates:
        new_stoichiometries[arg] -= 1
    for arg in products:
        new_stoichiometries[arg] += 1
    return dict(new_stoichiometries)


class BaseRateLaw(ABC):
    def __init__(self):
        self.substrates = []
        self.products = []
        self.modifiers = []
        self.parameters = []
        self.stoichiometry = {}
        self.reversible = False

    @abstractmethod
    def get_sbml_function_string(self):
        """Write me."""

    @abstractmethod
    def get_rate_function(self):
        """Write me."""


class Constant(BaseRateLaw):
    def __init__(self, product, k):
        super().__init__()
        self.products = [product]
        self.parameters = [k]
        self.stoichiometry = {product: 1}

        self.k = k

    def get_sbml_function_string(self):
        return f"{self.k}"

    def get_rate_function(self):
        return ratefunctions.constant


class MassAction(BaseRateLaw):
    def __init__(self, substrates, products, k_fwd):

        super().__init__()
        self.substrates = list(substrates) if not isinstance(substrates, str) else [substrates]
        self.products = list(products) if not isinstance(products, str) else [products]
        self.parameters = [k_fwd]
        self.stoichiometry = _pack_stoichiometries(substrates, products)

        self.k_fwd = k_fwd

    def get_sbml_function_string(self):
        return f"{self.k_fwd} * {' * '.join(self.substrates)}"

    def get_rate_function(self):
        try:
            return getattr(ratefunctions, f"mass_action_{len(self.substrates)}")
        except AttributeError:
            return ratefunctions.mass_action_variable


class ReversibleMassAction(BaseRateLaw):
    def __init__(self, substrates, products, k_fwd, k_bwd):
        super().__init__()
        self.substrates = list(substrates) if not isinstance(substrates, str) else [substrates]
        self.products = list(products) if not isinstance(products, str) else [products]
        self.parameters = [k_fwd, k_bwd]
        self.stoichiometry = _pack_stoichiometries(substrates, products)
        self.reversible = True

        self.k_fwd = k_fwd
        self.k_bwd = k_bwd

    def get_sbml_function_string(self):
        return f"{self.k_fwd} * {' * '.join(self.substrates)} - {self.k_bwd} * {' * '.join(self.products)}"

    def get_rate_function(self):
        try:
            return getattr(
                ratefunctions,
                f"reversible_mass_action_{len(self.substrates)}_{len(self.products)}",
            )
        except AttributeError:
            return getattr(
                ratefunctions,
                f"reversible_mass_action_variable_{len(self.substrates)}",
            )


class MichaelisMenten(BaseRateLaw):
    def __init__(self, S, P, vmax, km):

        super().__init__()
        self.substrates = [S]
        self.products = [P]
        self.parameters = [vmax, km]
        self.stoichiometry = {S: -1, P: 1}

        self.S = S
        self.vmax = vmax
        self.km = km

    def get_sbml_function_string(self):
        return f"{self.S} * {self.vmax} / ({self.S} + {self.km})"

    def get_rate_function(self):
        return ratefunctions.michaelis_menten


class ReversibleMichaelisMenten(BaseRateLaw):
    def __init__(self, S, P, vmax_fwd, vmax_bwd, km_fwd, km_bwd):
        super().__init__()
        self.substrates = [S]
        self.products = [P]
        self.parameters = [vmax_fwd, vmax_bwd, km_fwd, km_bwd]
        self.stoichiometry = {S: -1, P: 1}
        self.reversible = True

        self.S = S
        self.P = P
        self.vmax_fwd = vmax_fwd
        self.vmax_bwd = vmax_bwd
        self.km_fwd = km_fwd
        self.km_bwd = km_bwd

    def get_sbml_function_string(self):
        return (
            f"({self.vmax_fwd} * {self.S} / {self.km_fwd} - {self.vmax_bwd} * {self.P} / {self.km_bwd})"
            + f" / (1 + {self.S} / {self.km_fwd} + {self.P} / {self.km_bwd})"
        )

    def get_rate_function(self):
        return ratefunctions.reversible_michaelis_menten


class ReversibleMichaelisMentenKeq(BaseRateLaw):
    def __init__(self, S, P, vmax_fwd, km_fwd, km_bwd, k_eq):

        super().__init__()
        self.substrates = [S]
        self.products = [P]
        self.parameters = [vmax_fwd, km_fwd, km_bwd, k_eq]
        self.stoichiometry = {S: -1, P: 1}
        self.reversible = True

        self.S = S
        self.P = P

        self.vmax_fwd = vmax_fwd
        self.km_fwd = km_fwd
        self.km_bwd = km_bwd
        self.k_eq = k_eq

    def get_sbml_function_string(self):
        return (
            f"{self.vmax_fwd} / {self.km_fwd} * ({self.S} - {self.P} / {self.k_eq})"
            + f"/ (1 + {self.S} / {self.km_fwd} + {self.P} / {self.km_bwd})"
        )

    def get_rate_function(self):
        return ratefunctions.reversible_michaelis_menten_keq
