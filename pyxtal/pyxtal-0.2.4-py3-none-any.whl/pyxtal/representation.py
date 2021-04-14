"""
structure representation
"""

from rdkit.Chem.rdMolTransforms import CanonicalizeConformer
from rdkit import Chem
from operator import itemgetter

# Standard Libraries
class representation():
    """
    Class for handling molecular crystal representation
    
    Args: 
        xtal: pyxtal object
    """

    def __init__(self, xtal):

        self.struc = xtal
        self.rep_cell = xtal.lattice.get_para(degree=True)
        self.rep_molecule = []
        for mol_site in xtal.mol_sites:
            rep = list(mol_site.position) 
            rep += list(mol_site.)

            self.rep_molecule.append(rep)

    def to_vector(self):


    def to_pyxtal(self):
        """
        rebuild the pyxtal from the 1D representation
        """
        new_struc = self.struc.copy()
        lattice = new_struc.lattice
        diag = new_struc.diag
        ori = 
        for i, site in enumerate(new_struc.mol_sites()):
            pos0 = np.array(self.rep_molecule[i][:3])
            ori = 
            
            mol_site(_mol, pos0, ori, wp, lattice, diag)


    def fit():

# zmatrix2xyz
# xyz2zmatrix
# compute rotation: https://github.com/charnley/rmsd

