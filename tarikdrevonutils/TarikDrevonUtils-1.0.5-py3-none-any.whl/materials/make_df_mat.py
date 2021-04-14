import numpy as np
import pandas as pd
import pickle,os


from GaAs import mat as GaAs
from InAs import mat as InAs
from AlAs import mat as AlAs
from Si import mat as Si
from Ge import mat as Ge

##add materials here
mats = {'GaAs':GaAs,'AlAs':AlAs,'InAs':InAs, 'Si':Si,'Ge':Ge}

sc_cond   = ['Eg','Xi','eps','Nc','Nv']
masses    = ['me','mh','mhh','mlh','mso']
lattice   = ['a0']
luttinger = ['g1','g2','g3']
stiffness = ['C11','C12','C44']
optical   = ['n_ref']
other     = ['a','b','d']

cols = sc_cond+masses+lattice+luttinger+stiffness+optical+other
df = pd.DataFrame(columns=cols)

for mat_name,mat in mats.items():
    df.loc[mat_name] = [np.nan]*len(cols)
    for k,v in mat.items():df.loc[mat_name][k]=v

filename = os.path.dirname(__file__)+'/materials.pkl'
df.to_pickle(filename)
print(filename+ ' saved')
