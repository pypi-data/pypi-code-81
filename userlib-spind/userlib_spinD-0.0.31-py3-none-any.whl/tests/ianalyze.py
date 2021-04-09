# -*- coding: utf-8 -*-
r"""
abstract base class for analyzing the test results
"""
from abc import ABC, abstractmethod


class IAnalyzer(ABC):
    r"""
    Abstract base class for evaluating and analyzing test results.
    """
    @abstractmethod
    def __call__(self, *args, **kwargs) -> bool:
        r"""
        Analyzes the test

        Returns:
            A boolean whether this test failed
        """