#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fonctions de statistiques
^^^^^^^^^^^^^^^^^^^^^^^^^

Created on Tue Nov 24 12:32:10 2020

@author: Cyrile Delestre
"""

from typing import Optional

import numpy as np

def weighted_avg_and_std(x: np.ndarray,
                         sample_weight: Optional[np.ndarray]=None,
                         axis: Optional[int]=0):
    """
    Retourne la moyenne de l'écart-type avec un poids sur chaque mesure.
    
    Parameters
    ----------
    x : np.ndarray
        variable aléatoire.
    sample_weight : Optional[np.ndarray]
        poids sur les samples. Doit avoir la même dimension que x un vecteur
        colonne.
    axis : Optional[int]
        dimension de l'opération. Si None fait sur toutes les dimensions.
    
    Returns
    -------
    mean : Union[np.ndarray, float]
        moyenne pondérée, scalaire si axis = None, sinon 
        (n1 x ... x ni x ... nq) si axis = i
    std : Union[np.ndarray, float]
        écart-type pondéré, scalaire si axis = None, sinon 
        (n1 x ... x ni x ... nq) si axis = i
    
    Notes
    -----
    Cette fonction retourne également la moyenne car elle en as besoin pour 
    le calcul de la variance. Il s'agit également de la moyenne pondérée.
    """
    # Obligé de faire un reshape sinon la sortie peut ne pas préserver les 
    # dimensions.
    ind_reshape = [-1]*len(x.shape)
    ind_reshape[axis] = 1
    mean = np.average(
        a = x,
        weights = sample_weight,
        axis = axis
    ).reshape(*ind_reshape)
    var = np.average(
        a = (x-mean)**2,
        weights = sample_weight,
        axis = axis
    ).reshape(*ind_reshape)
    return (mean, np.sqrt(var))
