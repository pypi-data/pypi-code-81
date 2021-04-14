import numpy as np
import pandas as pd
import os
from .physicsConstants import kB,eV
from . import glob_colors as colors

materials = pd.read_pickle(os.path.dirname(__file__)+'/materials/materials.pkl')
_key_cols = materials.columns.values.tolist()
_key_funcs = ['Ncv','Ni','Neff']
_keys = _key_cols+_key_funcs


## functions to compute new properties from existing entries
get_NcNv = lambda mat,T: np.sqrt(mat['Nc']*mat['Nv'])
get_Ni   = lambda mat,T: get_NcNv(mat,T)*np.exp(-mat['Eg']/(2*(kB*T/eV)))
get_Neff = lambda mat,T: 2.5e19*mat['me']**1.5*(T/300)**1.5
funcs = dict(zip(_key_funcs,[get_NcNv,get_Ni,get_Neff]))

def get_params(mat_name,T,keys):
    ''' get properties of a material
    matName : str - Material name
    T       : Temperature (K)
    keys    : properties as available in materialManager._keys
    '''
    kT = kB*T/eV
    mat = materials.loc[mat_name]
    key_funcs = [k for k in keys if k in _key_funcs ]#;print(key_funcs)
    for kf in key_funcs : mat[kf] = funcs[kf](mat,T)
    values = mat[keys].values
    return values

def update_materials():
    import subprocess
    mat_path = os.path.dirname(__file__)+'/materials/'
    out=subprocess.check_output("python3 %smake_df_mat.py" %mat_path,shell=True).decode()
    print(colors.green+out+colors.black)
    materials = pd.read_pickle(mat_path+'materials.pkl')
# class Material:
#     def __init__(self,name):
#         vals = materials.loc[name].values
#         self.__dict__=dict(zip(cols,vals))
# get_NcNv = lambda mat: np.sqrt(mat.Nc*mat.Nv)
# get_Ni   = lambda mat: np.sqrt(mat.Nc*mat.Nv)*np.exp(-mat.Eg/(2*mat.kT))
# get_Neff = lambda mat: 2.5*e19*pow(mat.me,1.5)*pow(mat.T/300,1.5)

def computeIntrinsicDensity(Nc,Nv,Eg,T):
    Ni2 = Nc*Nv*np.exp(-Eg/(kB*T/eV))
    return np.sqrt(Ni2)

# def doping(x,Nd,Na):
#     N = len(x)
#     Ndx = np.zeros((N))
#     Nax = np.zeros((N))
#     for i in range(0,N):
#         if x[i]>0:
#             Ndx[i] = Nd
#         if x[i]<0:
#             Nax[i] = Na
#     return Ndx,Nax
#
# def computeEffectiveDensity(mc,T=300):
#     Neff = 2.5*e19*pow(me,1.5)*pow(T/300,1.5);
#     return Neff

linear_interp = lambda x,v1,v2 : x*v1 + (1-x)*v2
def getTernaryAlloy(mat1,mat2,x,keys=None,T=300):
    if not keys : keys = ['Eg','a0', 'g1','g2','g3', 'C11','C12','C44', 'a','b','d']
    mat1 = get_params(mat1,T,keys)
    mat2 = get_params(mat2,T,keys);#print(mat2)
    values = [linear_interp(x,v1,v2) for v1,v2 in zip(mat1,mat2)]
    return values


########################################################################
# tests
########################################################################
def _testTernaryAlloys(mat1='GaAs',mat2='AlAs',x=0.5):
    keys = ['Eg','a0', 'g1','g2','g3', 'C11','C12','C44', 'a','b','d']
    vals = getTernaryAlloy(mat1,mat2,x,keys)
    print('\n\t'+'AlGaAs\n',dict(zip(keys,vals)))

def _test_get_params(mat_name='GaAs',T=300):
    print('\n\t'+mat_name)
    keys=['Nc','Ni','Neff']; print(dict(zip(keys,get_params(mat_name,T,keys))))
    keys=['Eg','eps','Xi',]; print(dict(zip(keys,get_params(mat_name,T,keys))))

if __name__=='__main__':
    name = 'GaAs'
    _test_get_params(name)
    _testTernaryAlloys()
