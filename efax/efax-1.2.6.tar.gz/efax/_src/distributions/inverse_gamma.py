from __future__ import annotations

from typing import Optional

from tjax import Array, Generator, RealArray, Shape
from tjax.dataclasses import dataclass

from ..samplable import Samplable
from ..transformed_parametrization import (TransformedExpectationParametrization,
                                           TransformedNaturalParametrization)
from .gamma import GammaEP, GammaNP

__all__ = ['InverseGammaNP', 'InverseGammaEP']


@dataclass
class InverseGammaNP(TransformedNaturalParametrization[GammaNP, GammaEP, 'InverseGammaEP'],
                     Samplable):
    gamma_np: GammaNP

    # Implemented methods --------------------------------------------------------------------------
    def base_distribution(self) -> GammaNP:
        return self.gamma_np

    def create_expectation(self, expectation_parametrization: GammaEP) -> InverseGammaEP:
        return InverseGammaEP(expectation_parametrization)

    def sample_to_base_sample(self, x: Array) -> RealArray:
        return 1.0 / x

    def sample(self, rng: Generator, shape: Optional[Shape] = None) -> RealArray:
        y = self.gamma_np.sample(rng, shape)
        return 1.0 / y  # Convert base sample to sample.


@dataclass
class InverseGammaEP(TransformedExpectationParametrization[GammaEP, GammaNP, InverseGammaNP]):
    gamma_ep: GammaEP

    # Implemented methods --------------------------------------------------------------------------
    def base_distribution(self) -> GammaEP:
        return self.gamma_ep

    def create_natural(self, natural_parametrization: GammaNP) -> InverseGammaNP:
        return InverseGammaNP(natural_parametrization)
