"""
Calculate the additive genomic relationship matrix


"""

import logging
import os
from gmat.gmatrix import agmat
from gmat.gmatrix import agmat_dosage
from gmat.gmatrix import pca


logging.basicConfig(level=logging.INFO)

bed_file = '../data/mouse/plink'
out_file = '../data/mouse/test'

# matrix form
agmat0 = agmat(bed_file, out_file, inv=True, small_val=0.001, out_fmt='mat')

# row-column-value form, which can be used by asreml

# id-id-value form
agmat2 = agmat(bed_file, out_file, inv=True, small_val=0.001, out_fmt='id_id_val')

out_file = '../data/mouse/test2'
geno_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/mouse/geno.txt'
agmat_dosage(geno_file, out_file, inv=True, out_fmt='id_id_val', npart=10, small_val=0.001)


# PCA and heatmap
pca("../data/mouse/test")
