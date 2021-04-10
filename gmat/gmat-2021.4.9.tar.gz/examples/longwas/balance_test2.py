
### Estimate the variances
import numpy as np
import pandas as pd
from gmat.gmatrix import agmat
from gmat.longwas.balance import balance_varcom
import logging

logging.basicConfig(level=logging.INFO)

bed_file = '../data/mouse_long/plink'
out_file = '../data/mouse_long/test'
agmat(bed_file, out_file=out_file, inv=False, small_val=0.001, out_fmt='id_id_val')

data_file = '../data/mouse_long/phe.balance.txt'
id = 'ID'
tpoint = np.array(range(16)) + 1.0
trait = range(2, 18)
kin_file = '../data/mouse_long/test.agrm.id_fmt'
prefix_outfile = '../data/mouse_long/balance_varcom'
res_var = balance_varcom(data_file, id, tpoint, trait, kin_file, prefix_outfile=prefix_outfile)
print(res_var)

### longitudinal GWAS by fixed method

from gmat.longwas.balance import balance_longwas_fixed
var_com = pd.read_csv('../data/mouse_long/balance_varcom.var', header=0, sep='\s+')
prefix_outfile = '../data/mouse_long/balance_longwas_fixed'
res_fixed = balance_longwas_fixed(data_file, id, tpoint, trait, kin_file, bed_file, var_com, snp_lst=None,
                                 prefix_outfile=prefix_outfile)

### longitudinal GWAS by trans method

from gmat.longwas.balance import balance_longwas_trans
var_com = pd.read_csv('../data/mouse_long/balance_varcom.var', header=0, sep='\s+')
prefix_outfile = '../data/mouse_long/balance_longwas_trans'
res_trans = balance_longwas_trans(data_file, id, tpoint, trait, kin_file, bed_file, var_com, snp_lst=None,
                                 prefix_outfile=prefix_outfile)
