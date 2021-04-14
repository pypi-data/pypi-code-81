from typing import Iterator, List

from . import DesignValues


class Designs:
    """
    Class containing a lot of designs to be simulated
    """

    def __init__(self, designs: List[DesignValues] = None):
        self.__designs = []

        if designs is not None:
            self.__designs = designs.copy()

    def __iter__(self) -> Iterator[DesignValues]:
        return iter(self.get_designs())

    def get_designs(self) -> List[DesignValues]:
        return self.__designs.copy()
