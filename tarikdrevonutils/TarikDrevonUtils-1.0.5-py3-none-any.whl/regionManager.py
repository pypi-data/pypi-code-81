'''
Region Manager to assign regions to a 1D mesh and retrieve values
'''
import numpy as np
from . import materialManager as matMg

######
def set_region1D(x,xlims,**kwargs):
    '''define a 1D region from a 1D mesh x with boundaries xlims
    - x : 1D mesh (np.1darray)
    - xlims : region boundaries (do not need to lie within mesh)
    - kwargs : optional associated properties such as name, doping
    returns :\n
    - region : dict containing region info kwargs
        - x[region['idx']] : coordinates of region
        - region['lims']   : boundaries of region
    '''
    id0 = abs(x-xlims[0]).argmin()
    id1 = abs(x-xlims[1]).argmin()

    idx = slice(id0,id1+1)#(x[id1] in x))
    xlims = x[[id0,id1]]

    region = {'idx':idx,'lims':xlims}
    region.update(kwargs)
    return region

def get_region_params(reg,keys,T=300):
    '''Get region parameters
    Note : mat_name must exist for this
    Fetch from materialManager if keys not found in reg.keys()
    '''
    reg_keys = [k for k in keys if k in reg.keys()]
    mat_keys = list(np.setdiff1d(keys,reg_keys+['mat_name']))
    mat_vals = matMg.get_params(reg['mat_name'],T,mat_keys)
    reg_vals = [reg[k] for k in reg_keys]
    vals = dict(zip(mat_keys+reg_keys, list(mat_vals)+reg_vals))
    values = [vals[k] for k in keys]
    return values

def set_regions_arrays(x,regions,keys,T=300):
    '''Set properties arrays from regions info
    Inputs :\n
    - x : mesh
    - regions : list of region dictionaries
    - keys : The properties(Eg,Xi,...) to fill the arrays with
    - T : temperature
    Note : At the moment the values are assumed constants per region
    Returns : \n
    - reg_arrays : list of arrays filled with region values
    '''
    nkeys = len(keys)
    reg_arrays = [np.zeros(x.shape) for k in range(nkeys)];
    for reg in regions:
        #print('\t'+reg['mat_name'])
        values = get_region_params(reg,keys,T)
        idx = reg['idx']
        for reg_a,val in zip(reg_arrays,values):
            reg_a[idx] = val
    return reg_arrays
