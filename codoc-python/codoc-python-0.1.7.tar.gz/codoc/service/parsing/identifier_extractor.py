#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod
from typing import Set


class IdentifierExtractor(metaclass=ABCMeta):
    @abstractmethod
    def get_identifiers(self) -> Set[str]:
        ...
