from biopandas.pdb import PandasPdb
import pandas
import math
import numpy

def ReadPDBintoDataFrame(PDBfileNameString):
    t= PandasPdb().read_pdb(PDBfileNameString).df["ATOM"]
    df = pandas.DataFrame(t)
    return df 
def RetreivePDBatomPosition(dataFramePDB, segmentIDstring, residueNumber, atomNameString):
    df1 = dataFramePDB.loc[dataFramePDB["segment_id"]== segmentIDstring]
    df1= df1.loc[dataFramePDB["residue_number"]==residueNumber]
    df1 = df1.loc[dataFramePDB["atom_name"]==atomNameString]
    df1= df1[["x_coord", "y_coord","z_coord"]]
#   return df1.values.tolist()[0]
    return df1.to_numpy()
def PDBsegmentIDset(dataFramePDB):
    segmentSet = set(dataFramePDB["segment_id"])
    return segmentSet
def EuclideanDistance(coords1, coords2):
#   return math.sqrt(sum(map(lambda x: (x[1]-x[0])**2, list(zip(coords1, coords2)))))
    return numpy.linalg.norm(coords1-coords2)
protein_letters = "ACDEFGHIKLMNPQRSTVWY"
extended_protein_letters = "ACDEFGHIKLMNPQRSTVWYBXZJUO"
protein_letters_1to3 = {
    "A": "Ala",
    "C": "Cys",
    "D": "Asp",
    "E": "Glu",
    "F": "Phe",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "K": "Lys",
    "L": "Leu",
    "M": "Met",
    "N": "Asn",
    "P": "Pro",
    "Q": "Gln",
    "R": "Arg",
    "S": "Ser",
    "T": "Thr",
    "V": "Val",
    "W": "Trp",
    "Y": "Tyr",
}
protein_letters_1to3_extended = dict(
    list(protein_letters_1to3.items())
    + list(
        {"B": "Asx", "X": "Xaa", "Z": "Glx", "J": "Xle", "U": "Sec", "O": "Pyl"}.items()
    )
)

protein_letters_3to1 = {x[1]: x[0] for x in protein_letters_1to3.items()}
protein_letters_3to1_extended = {
    x[1]: x[0] for x in protein_letters_1to3_extended.items()
}

def ConvertToOneLetter(seq, custom_map=None, undef_code="X"):

    if custom_map is None:
        custom_map = {"Ter": "*"}
    # reverse map of threecode
    # upper() on all keys to enable caps-insensitive input seq handling
    onecode = {k.upper(): v for k, v in protein_letters_3to1_extended.items()}
    # add the given termination codon code and custom maps
    onecode.update((k.upper(), v) for k, v in custom_map.items())
    seqlist = [seq[3 * i : 3 * (i + 1)] for i in range(len(seq) // 3)]
    return "".join(onecode.get(aa.upper(), undef_code) for aa in seqlist)

def ConvertToThreeLetter(seq, custom_map=None, undef_code="Xaa"):
    if custom_map is None:
        custom_map = {"*": "Ter"}
    # not doing .update() on IUPACData dict with custom_map dict
    # to preserve its initial state (may be imported in other modules)
    threecode = dict(
        list(protein_letters_1to3_extended.items()) + list(custom_map.items())
    )
    # We use a default of 'Xaa' for undefined letters
    # Note this will map '-' to 'Xaa' which may be undesirable!
    return "".join(threecode.get(aa, undef_code) for aa in seq)

def GetHydrogenBondDistances(dataFramePDB, resstart, resstop, segstart, segstop):
    residues2check = numpy.arange(resstart, resstop+1, 2)
    HBondDistances= numpy.zeros((segstop-segstart, len(residues2check)))
    for i in range(segstart, segstop):
        for j in residues2check:
            HN = RetreivePDBatomPosition(dataFramePDB, 'P'+str(i+1),j+1,'HN')
            CO = RetreivePDBatomPosition(dataFramePDB, 'P'+str(i),j,'O')
            HBondDistances[i-1, int(numpy.where(residues2check == j)[0])]=EuclideanDistance(HN, CO)
    return HBondDistances



  