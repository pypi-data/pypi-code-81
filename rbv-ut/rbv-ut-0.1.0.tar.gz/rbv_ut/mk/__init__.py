from .fe import FE
from .fhisip import FHISIP
from .fkip import FKIP
from .fst import FST
from .pascasarjana import PASCASARJANA


MK = FE + FHISIP + FKIP + FST + PASCASARJANA

__all__ = ["FE", "FHISIP", "FKIP", "FST", "PASCASARJANA", "MK"]
