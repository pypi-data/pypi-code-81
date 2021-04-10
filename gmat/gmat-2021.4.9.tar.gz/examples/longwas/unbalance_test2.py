import numpy as np
import pandas as pd
from gmat.gmatrix import agmat
from gmat.longwas.unbalance import unbalance_varcom
import logging

logging.basicConfig(level=logging.INFO)

bed_file = '../data/mouse_long/plink'
# agmat(bed_file, out_file='../data/mouse_long/test', out_fmt='id_id_val')
data_file = '../data/mouse_long/phe.unbalance.txt'
id = 'ID'
tpoint = 'weak'
trait = 'trait'
agmat_file = '../data/mouse_long/test'
tfix = 'Sex'
prefix_outfile = '../data/mouse_long/unbalance_varcom'
# res_var = unbalance_varcom(data_file, id, tpoint, trait, agmat_file, tfix="Sex", out_file=prefix_outfile)
# print(res_var)

var_com = pd.read_csv("../data/mouse_long/unbalance_varcom.var", sep='\s+', header=0)

"""
from gmat.longwas.unbalance import unbalance_longwas_fixed
prefix_outfile = '../data/mouse_long/unbalance_longwas_fixed'
res_fixed = unbalance_longwas_fixed(data_file, id, tpoint, trait, bed_file, agmat_file, var_com,
 tfix=None, fix="Sex", forder=3, aorder=3, porder=3, na_method='omit', prefix_outfile=prefix_outfile)


from gmat.longwas.unbalance import unbalance_condition_longwas_fixed
prefix_outfile = '../data/mouse_long/unbalance_condition_longwas_fixed'
res_fixed = unbalance_condition_longwas_fixed(data_file, id, tpoint, trait, bed_file, agmat_file, var_com, condition_snp="UNC30664376", tfix=None, fix="Sex", 
                             prefix_outfile=prefix_outfile)



from gmat.longwas.unbalance import unbalance_longwas_trans
prefix_outfile = '../data/mouse_long/unbalance_longwas_trans'
res_trans = unbalance_longwas_trans(data_file, id, tpoint, trait, bed_file, agmat_file, var_com, tfix="Sex",
                                    prefix_outfile=prefix_outfile)
"""
from gmat.longwas.unbalance import unbalance_condition_longwas_trans

prefix_outfile = '../data/mouse_long/unbalance_condition_longwas_trans'
res_trans = unbalance_condition_longwas_trans(data_file, id, tpoint, trait, bed_file, agmat_file, var_com, condition_snp="UNC30664376", tfix="Sex", fix="Sex",
                                    prefix_outfile=prefix_outfile)
"""
from gmat.longwas.unbalance import unbalance_longwas_fixed_permutation
prefix_outfile = '../data/mouse_long/unbalance_longwas_fixed_permutation'
unbalance_longwas_fixed_permutation(data_file, id, tpoint, trait, bed_file, agmat_file, var_com, permutation_lst=range(10),
            snp_lst=None, tfix="Sex", fix=None, forder=3, aorder=3, porder=3, na_method='omit',
                             prefix_outfile=prefix_outfile)


from gmat.longwas.unbalance import unbalance_longwas_trans_permutation
prefix_outfile = '../data/mouse_long/unbalance_longwas_trans_permutation'
unbalance_longwas_trans_permutation(data_file, id, tpoint, trait, bed_file, agmat_file, var_com, permutation_lst=range(10), snp_lst=None,
            tfix="Sex", fix=None, forder=3, aorder=3, porder=3, na_method='omit',
                             prefix_outfile=prefix_outfile)
"""
