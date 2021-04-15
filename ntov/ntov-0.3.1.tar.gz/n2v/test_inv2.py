import n2v
from inverter2 import Inverter


if __name__ == "__main__":

    param = {"mol"   : """He""", 
             "basis" : "cc-pvdz", 
             "aux"   : "cc-pvdz"}

    inv = Inverter( **param )

