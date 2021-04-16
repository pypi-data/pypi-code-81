"""The featurizer module defines the core `Featurizer` abstract base class.

A `Featurizer` is a functional transform on training data.

Example:

    literal blocks::

        ohe = deepbio.feat.OHE()

        dl = deepbio.data.DataLoader(genomic_data,
            featurizer=ohe)
        for sample in dl:
            print(sample)
"""

from abc import ABCMeta, abstractmethod
from typing import Any, Iterable


class Featurizer(metaclass=ABCMeta):
    """Abstract Base Class that defines an interface for featurizing data.

    Defines a data model that is easily extensible vis-a-vis
    [open-closed](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)
    philosophy.

    This is thus a formal implementation of an object interface. Developers
    need only to implement the `featurize` method (without explicit
    inheritance) in a custom object and their
    code will play nicely with the extended DeepBio ecosystem.
    """

    @abstractmethod
    def featurize(self, X: Any, log: bool = False) -> Iterable[Any]:
        """Featurize data.

        Note that you only need to implement logic to featurize a _single
        sample_. Mapping this logic over a batch is handled automatically using
        DeepBio `DataLoader` + `Dataset` pairs.

        Args:
            X (Iterable[Any]): An iterator that contains data.
            log (bool): A flag to indicate logging during featurization.

        Returns:
            Iterable[Any]: An iterator that contains featurized data.
        """
        raise NotImplementedError

    def __call__(self, datapoints: Iterable[Any], log: bool = False):
        """Featurize data.

        Args:
            X (Iterable[Any]): An iterator that contains data.
            log (bool): A flag to indicate logging during featurization
        """

        return self.featurize(datapoints, log)

    @classmethod
    def __subclasshook__(cls, C):
        """Asserts that objects implementing ABC have correct behavior."""
        if cls is Featurizer:
            # https://stackoverflow.com/questions/2010692/what-does-mro-do
            if any("featurize" and "_featurize" in B.__dict__ for B in C.__mro__):
                return True
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Memory representation.

        Returns:
          str: Memory representation of self.
        """

        raise NotImplementedError

    @abstractmethod
    def __unicode__(self) -> str:
        """String representation

        Returns:
          str: String representation of self.
        """

        raise NotImplementedError
