from dataclasses import dataclass


@dataclass
class GlobalSystemConstants():

    @classmethod
    def getAllStages(self) -> list:
        """
        You need to subclass this class and add stages (e.g. DEV, Pre-Quality, Production).
        :return:
        """
        return []
