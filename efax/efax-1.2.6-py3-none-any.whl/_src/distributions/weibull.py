from __future__ import annotations

from typing import Optional

import jax
import jax.numpy as jnp
from chex import Numeric
from tjax import Generator, RealArray, Shape
from tjax.dataclasses import dataclass

from ..expectation_parametrization import ExpectationParametrization
from ..natural_parametrization import NaturalParametrization
from ..parameter import ScalarSupport, distribution_parameter
from ..samplable import Samplable

__all__ = ['WeibullNP', 'WeibullEP']


@dataclass
class WeibullNP(NaturalParametrization['WeibullEP']):
    concentration: Numeric = distribution_parameter(ScalarSupport(), fixed=True)
    # eta = -1 / scale^concentration
    # scale = -1 / eta^(1/concentration)
    eta: RealArray = distribution_parameter(ScalarSupport())

    # Implemented methods --------------------------------------------------------------------------
    def shape(self) -> Shape:
        return self.eta.shape

    def log_normalizer(self) -> RealArray:
        return -jnp.log(-self.eta) - jnp.log(self.concentration)

    def to_exp(self) -> WeibullEP:
        return WeibullEP(self.concentration, -1.0 / self.eta ** (1.0 / self.concentration))

    def carrier_measure(self, x: RealArray) -> RealArray:
        return (self.concentration - 1.0) * jnp.log(x)

    def sufficient_statistics(self, x: RealArray) -> WeibullEP:
        return x ** self.concentration


@dataclass
class WeibullEP(ExpectationParametrization[WeibullNP], Samplable):
    concentration: Numeric = distribution_parameter(ScalarSupport(), fixed=True)
    scale: RealArray = distribution_parameter(ScalarSupport())

    # Implemented methods --------------------------------------------------------------------------
    def shape(self) -> Shape:
        return self.scale.shape

    def to_nat(self) -> WeibullNP:
        return WeibullNP(self.concentration, -1.0 / self.scale ** self.concentration)

    def expected_carrier_measure(self) -> RealArray:
        return jnp.zeros(self.shape())

    def sample(self, rng: Generator, shape: Optional[Shape] = None) -> RealArray:
        if shape is not None:
            shape += self.shape()
        else:
            shape = self.shape()
        return jax.random.weibull_min(rng.key, self.scale, self.concentration, shape)
