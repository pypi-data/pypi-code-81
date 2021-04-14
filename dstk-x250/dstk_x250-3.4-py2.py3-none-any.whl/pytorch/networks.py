#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèles de réseaux MLP génériques utilisables pour PyTorch

Created on Mon Sep 16 14:42:57 2019

@author: Cyrile Delestre
"""
from typing import Optional, Callable

import numpy as np

from torch import Tensor
from torch.nn import (Module, Linear, LeakyReLU, Dropout, BatchNorm1d,
                      ModuleList)

class MLP(Module):
    """
    Classe MLP de construction automatique en fonction du nombre de hidden
    layers et de la topologie des dimensions.
    
    Parameters
    ----------
    dim_in : int
        dimension d'entrée
    dim_out : int
        dimension de sortie
    dim_first_lay : int
        nombre de neronne de la première couche
    n_layers : int
        nombre de hidden layers
    embed_topo : str
        topologie des dimensions des hidden layers
            - linear: part de in_units et progresse linéairement vers out_unist
            - bottleneck: part de in_units et progresse linéairement vers 
                inter_units puis progresse linéaiement vers out_units
        (par défaut 'linear')
    inter_units : int
        dimension intermédiaire pour l'option
        embed_topo = 'bottleneck', sinon inutile (par défaut 10)
    alpha : float
        coefficient de non-linéarité de la fonction d'activation LeakyReLU
        (par défaut 0.3)
    dropout_prob : float
        proportion de dropout en proba (par défaut 0 <= pas de dropout)
    batchnorm : bool
        utilise la batchnorm (par défaut True)
    dropout : bool
        utilise le dropout (par défaut True)
    batchnorm_last_layer : bool
        applique la batchnormalization sur la dernière couche (par défaut 
        True)
    activation_last_layer : Optional[Callable]
        permet d'envoyer une fonction d'activation sur la dernière couche 
        (logit). Si None, pas de fonction d'activation appliquée.
    dropout_last_layer : bool
        applique ou non le dropout sur la dernière couche (par défaut True)
    
    Returns
    -------
    res : Tensor
        La dimension de sortie est (None, out_units)
    """
    def __init__(self,
                 dim_in: int,
                 dim_out: int,
                 dim_first_lay: int,
                 n_layers: int,
                 embed_topo: str='linear',
                 inter_units: int=10,
                 alpha: float=0.3,
                 dropout_prob: float=0,
                 batchnorm: bool=True,
                 dropout: bool=True,
                 batchnorm_last_layer: bool=True,
                 activation_last_layer: Optional[Callable]=None,
                 dropout_last_layer: bool=True):
        assert embed_topo in ['linear', 'bottleneck'] \
            and dim_in > 0 \
            and dim_out > 0
        super(MLP, self).__init__()
        self.dim_in = dim_in
        self.dim_out = dim_out
        self.dim_first_lay = dim_first_lay
        self.n_layers = n_layers
        self.embed_topo = embed_topo
        self.inter_units = inter_units
        self.alpha = alpha
        self.dropout_prob = dropout_prob
        self.batchnorm = batchnorm
        self.dropout = dropout
        self.batchnorm_last_layer = batchnorm_last_layer
        self.activation_last_layer = activation_last_layer
        self.dropout_last_layer = dropout_last_layer
        self.build()

    def build(self):
        """
        Fonction de construction du réseau de neurones.
        
        Warnings
        --------
        Pour Scikit-Learn, il faut que la fonction d'initialisation soit 
        différente de la fonction de construction.
        """
        if isinstance(self.activation_last_layer, bool):
            raise ValueError(
                "activation_last_layer est un booléen. Ce paramètre doit être "
                "une fonction ou None si aucune activation_last_layer ne doit "
                "être appliquée."
            )

        if self.n_layers > 1:
            if self.embed_topo == 'linear':
                    d_unite = (
                        (self.dim_first_lay-self.dim_out)/(self.n_layers-1)
                    )
                    units_by_lay = [
                        int(self.dim_first_lay-ii*d_unite)
                        for ii in range(self.n_layers)
                    ] 
            elif self.embed_topo == 'bottleneck':
                d_unite_1 = (
                    (self.dim_first_lay-self.inter_units)/
                    np.floor(self.n_layers/2)
                )
                units_dec = [
                    int(self.dim_first_lay-ii*d_unite_1)
                    for ii in range(int(np.floor(self.n_layers/2)))
                ]
                if self.n_layers == 2:
                    units_gro = [self.dim_out]
                else:
                    d_unite_2 = (
                        (self.inter_units-self.dim_out)/
                        np.ceil(self.n_layers/2-1)
                    )
                    units_gro = [
                        int(self.inter_units-ii*d_unite_2)
                        for ii in range(int(np.ceil(self.n_layers/2)))
                    ]
                units_by_lay = units_dec+units_gro
            else:
                raise AttributeError(
                    "Erreur embed_topo not in ['linear', 'bottleneck']"
                )
            units_in = [self.dim_in]+units_by_lay[:-1]
            units_out = units_by_lay
        else:
            units_in = [self.dim_in]
            units_out = [self.dim_out]
        layers = []
        for ii, nn in enumerate(zip(units_in, units_out)):
            n_in, n_out = nn
            layers.append(
                Linear(
                    in_features = n_in,
                    out_features = n_out,
                    bias = (
                        not self.batchnorm 
                        or (ii == self.n_layers-1 
                            and not self.batchnorm_last_layer)
                    )
                )
            )
            if (ii < self.n_layers-1 or self.batchnorm_last_layer) and self.batchnorm:
                layers.append(BatchNorm1d(num_features=n_out))
            if ii < self.n_layers-1:
                layers.append(LeakyReLU(negative_slope=self.alpha))
            if ii == self.n_layers-1 and self.activation_last_layer is not None:
                layers.append(self.activation_last_layer)
            if (ii < self.n_layers-1 or self.dropout_last_layer) and self.dropout:
                layers.append(Dropout(p=self.dropout_prob))
        self.layers = ModuleList(layers)
        return self

    def forward(self, inputs: Tensor):
        """
        Fonction d'appel du MLP
        
        Parameters
        ----------
        inputs : Tensor
            inputs de dimensions (batch_size, feat_size)
        
        Returns
        -------
        x_lay : Tensor
            sortie du MLP
        """
        x_lay = inputs
        for lay in self.layers:
            x_lay = lay(x_lay)
        return x_lay
