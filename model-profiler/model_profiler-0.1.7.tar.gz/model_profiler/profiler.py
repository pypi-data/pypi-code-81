# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 17:45:33 2021

@author: Talha
"""

from model_profiler.utils import get_available_gpus, get_param, keras_model_memory_usage, count_flops, mem_for_storing_weights
#%
import numpy as np
from tabulate import tabulate


Batch_size = 1
units = ['GPU IDs', 'BFLOPs', 'GB', 'Million', 'MB']

Profile = ['Selected GPUs', 'No. of FLOPs', 'GPU Memory Requirement',
           'Model Parameters', 'Memory Required by Model Weights']


def model_profiler(model, Batch_size, profile=Profile, use_units=units, verbose=0):
    '''
    Parameters
    ----------
    model : a keras/tensorflow compiled or uncompiled model
    Batch_size : an int default to 1.
    Profile : a list of profile characterstics
    use_units : units for those characterstics
    verbose: whether to print out the model profile or not [verbose > 0] will 
            print out the profile
    Returns
    -------
    profile: a ordered pretty string table containing model profile 
            alos prints out the model profile

    '''
    
    gpus = get_available_gpus()
    flops = count_flops(use_units[1], model, Batch_size)
    mem = keras_model_memory_usage(use_units[2], model, Batch_size)
    param = get_param(use_units[3], model)
    mem_req = mem_for_storing_weights(use_units[4], model)
    
    values = [gpus, flops, mem, param, mem_req]
    
    full_profile = np.concatenate((
                                np.asarray(Profile).reshape(-1,1),
                                np.asarray(values).reshape(-1,1),
                                np.asarray(use_units).reshape(-1,1)
                                )
                            , 1)
    profile = tabulate(
                    np.ndarray.tolist(full_profile),
                    headers = ["Model Profile", "Value", "Unit"],
                    tablefmt="github"
                    )
    if verbose > 0:
        print(profile)
    
    return profile


