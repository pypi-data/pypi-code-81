import numpy as np
import psi4

from qcelemental.models import Molecule

from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple, Union, cast



class Inverter():

    print("I'll initialize the inverter")

    def __init__(self, molecule: str, basis:str, aux_basis:str = "None") -> None:


        #Acquire molecule
        self.mol       = psi4.core.Molecule(molecule)
        # self.mol       = Molecule.from_data( molecule )
        self.basis_str = basis
        self.basis     = psi4.core.BasisSet.build(self.mol, "ORBITAL", basis, True)
        self.nbf       = 


        self.basis_str = basis,

        self.pbs = self.basis, 

    # def set_molecule(self, ):


    # @classmethod()
    # def from_wfn(self, )


