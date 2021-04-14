#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe de wrapping Scikit-Learn pour PyTorch

Created on Mon Oct 21 14:42:57 2019

@author: Cyrile Delestre
"""
import uuid
import pickle as pkl
from typing import (Optional, ByteString, Union, Callable, Dict, Any, List,
                    Tuple)
from collections import OrderedDict
from warnings import warn

import numpy as np
from sklearn.base import BaseEstimator
import torch
from torch.nn.functional import l1_loss
from torch.utils.data import DataLoader, Dataset

from dstk.pytorch import (check_tensor, CallbackInterface, CallbackHandler,
                          FitState, FitControl, DEFAULT_CALLBACKS,
                          StochasticWeightAveraging)
from dstk.utils.errors import DivergenceError

class BaseEnvironnement(BaseEstimator):
    r"""
    Classe d'environnement PyTorch pour être compatible Scikit-Learn.
    
    Notes
    -----
    Les attributs constituant BaseEnvironnement :
        dtype : 
            type attendu en entrée du réseau (par défaut np.float32)

    Les méthodes constituant BaseEnvironnement :
        set_dtype : 
            définition du type PyTorch des données (par défaut float32)
        save_weights : 
            sauvegarde du modèle via Pickle
        load_weights : 
            chargement des poids via Pickle. Si modèle non buildé, build le 
            modèle
        load_model :
            chargement d'un modèle à partir du Pickle au format save_weights
        fit :
            fonction d'apprentissage avec prototypage compatible avec 
            Scikit-Learn

    Les méthodes qui doivent être implémentées dans la classe du réseau :
        __init__ : 
            avec seulement les hyper-paramètres du réseau, afin de pouvoir 
            modifier les hyper-paramètres avec la méthode set_params de 
            BaseEstimator.
        build : 
            fonction d'implémentation des éléments du réseau PyTorch ainsi 
            que de l'attribut optimizer contenant l'optimizer du réseau
        forward :
            fonction PyTorch d'éxécution du réseau
        predict :
            fonction de prédiction, au prototypage Scikit-Learn 
            predict(X, **kargs) :
                - classifier : doit sortir une classe
                - regresseur : doit sortir une régression
        predict_proba : (optionnel)
            pour les classifier uniquement. Permet de sortir la probabilité 
            d'une observation dans chaqu'une des classes
        score : (optionnel) 
            au format de prototype Scikit-Learn. Si cette méthode n'est pas 
            implémentée par l'utilisateur, ce sont alors les méthodes par 
            défaut dans Scikit-Learn qui seront utilisées, à savoir dans le 
            cas d'un Regressor, R^2, et dans le cas de Classifier, l'accuracy.
    """ 
    dtype = None

    def build(self):
        r"""
        Méthode d'erreur si la fonction build n'a pas été implémentée dans 
        la classe modèle de l'utilisateur.
        """
        raise NotImplementedError(
            "La méthode build n'a pas été implémentée dans la classe "
            f"{self.__name__}. Se reporter à la documentation de "
            "BaseEnvironnement pour connaître les commodités d'implémentation "
            "de cette dernière."
        )

    def forward(self):
        r"""
        Méthode de forward du module de réseau profond PyTorch (voir la
        documention PyTorch).
        """
        raise NotImplementedError(
            "La méthode forward n'a pas été implémentée dans la classe "
            f"{self.__name__}. Se reporter à la documentation de "
            "BaseEnvironnement et PyTorch pour connaître les commodités "
            "d'implémentation de cette dernière."
        )

    def number_of_parameters(self, learn_params: bool=True):
        r"""
        Méthope retournant le nombre de paramètres présent dans le modèle.

        Parameters
        ----------
        learn_params : bool (=True)
            Compte les paramètres qui permettent l'apprentissage du modèle. 
            Sinon compte tous les paramètres (ceux qui sont dérivables et 
            non dérivables).
        """
        if learn_params:
            model_parameters = filter(
                lambda p: p.requires_grad, self.parameters()
            )
        else:
            model_parameters = self.parameters()
        return sum([np.prod(p.shape) for p in model_parameters])

    def gpu(self, device: Optional[Union[int, torch.device]] = None):
        r"""
        Permet de mettre le modèle sur GPU en utilisant la méthode "cuda"
        interne au module Module de PyTorch.

        Parameters
        ----------
        device : Optional[Union[int, torch.device]] (=None)
            Permet de préciser le divice si la machine est équipé de plusieurs 
            GPU. Sinon envoit vers le GPU par défaut.

        Warnings
        --------
        Pour mettre un réseau sur GPU afin de réaliser un apprentissage il 
        faut dans un premier temps initialiser les poids du réseau et dans un 
        second instancier l'optimizer. En effet, certain optimizer initialise 
        des attribues importants pour l'éxécution de l'apprentissage dans 
        leurs __init__. Si l'envoit vers le GPU ce fait après l'initialisation 
        de l'optimizer une erreur ce produira (ceci est vrai que pour certain 
        optimizer, la majorité fonctionneront même si le réseau a été envoyé 
        dans un second temps).
        """
        self.cuda(device)
        self.optimizer = self.optimizer.__class__(
            self.parameters(),
            **self.optimizer.defaults
        )
        return self

    def set_dtype(self, dtype: torch.dtype):
        r"""\
        Méthode permettant de définir le type de Tensor dans PyTorch

        Parameters
        ----------
        dtype : torch.dtype
            Type du Tensor PyTorche.
        """
        if not isinstance(dtype, torch.dtype):
            raise AttributeError(
                "Le type dtype doit être de type torch.dtype et non de type "
                f"{type(dtype)}."
            )
        self.dtype = dtype
        parameters = self.state_dict()
        for ii in parameters:
            parameters[ii] = ii.type(dtype)
        self.load_state_dict(parameters);
        return self

    def save_weights(self,
                     path: Optional[str]=None,
                     save_optimizer_state: bool=False,
                     attr_list: Optional[Union[List[str], Tuple[str]]]=None,
                     **kargs_dump):
        r"""
        Méthode permettant de sauvegarder simplement les paramètres et les
        poids du modèle (sans la structure de réseau). Utilise Pickle.

        Parameters
        ----------
        path : Optional[str]
            path directory du modèle, si None retourne les données binaires de 
            Pickle.dumps()
        save_state_optimizer : bool
            booléen de sauvegarde de l'état de l'optimizer (par défaut False).
        attr_list : Optional[Union[List[str], Tuple(str)]]
            liste d'attributs à sauvegarder (par défaut None).
        **kargs_dump : 
            paramètres attachés à Pickle.dump(obj, file, **kargs_dump) si 
            path est un chemin ou a Pickles.dump(obj, **kargs_dump) si None.
        """
        # get_params est hérité de BaseEstimator
        params = self.get_params()
        state_dict = self.state_dict()
        if save_optimizer_state:
            state_optimizer = self.optimizer.state_dict()
        else:
            state_optimizer = None
        if attr_list:
            state_attribut = {
                attr: getattr(self, attr) for attr in attr_list
            }
        else:
            state_attribut = None
        if isinstance(path, str):
            pkl.dump(
                obj = [
                    params,
                    state_dict,
                    state_optimizer,
                    state_attribut
                ],
                file = open(path, 'bw'),
                **kargs_dump
            )
            return self
        elif path is None:
            return pkl.dumps(
                obj = [
                    params,
                    state_dict,
                    state_optimizer,
                    state_attribut
                ],
                **kargs_dump
            )
        else:
            raise AttributeError(
                "L'argument path doit être None ou un str et non de type "
                f"{type(path)}."
            )

    def load_weights(self, 
                     path_or_bytes: Union[str, ByteString],
                     **kargs_load):
        r"""
        Méthode permettant de charger les poids et les paramètres du modèle
        via Pickle.

        Parameters
        ----------
        path_or_bytes : Union[str, ByteString]
            path directory du modèle ou bytes représentant le modèles
        **kargs_load :
            paramètres attachés à Pickle.load(file, **kargs_load) si path ou 
            Pickle.loads(data, **kargs_load) si bytes.
        """
        if not hasattr(self, 'build'):
            raise NotImplementedError(
                "Le modèle PyTorch n'a pas de méthode build (réf. doc de la "
                "classe)."
            )
        self.build()
        if isinstance(path_or_bytes, str):
            _, state_dict, state_optimizer, state_attribut = pkl.load(
                file = open(path_or_bytes, 'br'),
                **kargs_load
            )
        elif isinstance(path_or_bytes, bytes):
            _, state_dict, state_optimizer, state_attribut = pkl.loads(
                data = open(path_or_bytes, 'br'),
                **kargs_load
            )
        else:
            raise AttributeError(
                "path_or_bytes doit être soit de type str ou bytes et non "
                f"de type {type(path_or_bytes)}."
            )
        self.load_state_dict(state_dict);
        if state_optimizer:
            self.optimizer.load_state_dict(state_optimizer)
        if state_attribut:
            for key, item in state_attribut.items():
                setattr(self, key, item);
        self.eval()
        return self

    @classmethod
    def load_model(cls,
                   path_or_bytes: Union[str, ByteString],
                   **kargs_load):
        r"""
        Fonction permettant de charger un modèle à partir d'une sauvegarde au
        format Pickle issue de save_weights(path).

        Parameters
        ----------
        path_or_bytes : Union[str, ByteString]
            path directory du modèle ou bytes représentant le modèles
        **kargs_load : 
            paramètres attachés à Pickle.load(file, **kargs_load) si path ou 
            Pickle.loads(data, **kargs_load) si bytes.

        Returns
        -------
        model : BaseEnvironnement
            modèle chargé
        """
        if isinstance(path_or_bytes, str):
            params, state_dict, state_optimizer, state_attribut = pkl.load(
                file = open(path_or_bytes, 'br'),
                **kargs_load
            )
        elif isinstance(path_or_bytes, bytes):
            params, state_dict, state_optimizer, state_attribut = pkl.loads(
                data = path_or_bytes,
                **kargs_load
            )
        else:
            raise AttributeError(
                "path_or_bytes doit être soit de type str ou bytes et non "
                f"de type {type(path_or_bytes)}."
            )
        model = cls(**params)
        if not hasattr(model, 'build'):
            raise NotImplementedError(
                "Le modèle PyTorch n'a pas de méthode build (réf. doc de la "
                "classe)."
            )
        model.build();
        model.load_state_dict(state_dict);
        if state_optimizer:
            model.optimizer.load_state_dict(state_optimizer)
        if state_attribut:
            for key, item in state_attribut.items():
                setattr(model, key, item)
        model.eval()
        return model

    def _extract_state(self, model):
        r"""
        Méthode privée qui extrait les paramètres du modèle et clone les 
        tensors PyTorch.

        Parameters
        ----------
        model :
            un modèle
        """
        return OrderedDict(
            (kk, vv.detach().clone()) for kk, vv in model.state_dict().items()
        )

    def _divergence(self, loss: float):
        r"""
        Méthode interne d'alerte de divergence du modèle pendant sa phase 
        d'apprentissage.
        """
        if np.isnan(loss) or np.isinf(loss):
            raise DivergenceError(
                """Verger ! L'algorithme à dit "verger" !"""
            )

    def _mod(self, n, mod):
        r"""
        Méthode interne permettant de calculer le modulo.
        """
        if mod:
            return n % mod
        else:
            return None

    def _train_step(self,
                    data: List[Dict[str, Any]],
                    field_target: str,
                    loss_fn: Callable,
                    kargs_loss: Dict[str, Any]):
        r"""
        Méthode privée d'une étape de backpropagation du gradient.

        Parameters
        ----------
        data : List[Dict[str, Any]]
            Liste de dictionnaires sur les données d'un mini-batch.
        field_target : str
            Nom du champs de la target.
        loss_fn : Callable
            Fonction coût PyTorch.
        kargs_loss : Dict[str, Any]
            Dictionnaire d'arguments à utiliser dans la fonction de coût 
            loss_fun.

        Returns
        -------
        loss : Valeur de la fonction coût au travers du mini-batch.
        """
        self.train()
        self.optimizer.zero_grad()
        output = self.forward(**data)
        target = check_tensor(data[field_target])
        loss_ = loss_fn(output, target, **kargs_loss)
        loss_.backward()
        self.optimizer.step()
        loss = loss_.detach()
        self._divergence(loss)
        return loss

    def _eval_step(self,
                   data: List[Dict[str, Any]],
                   field_target: str,
                   loss_fn: Callable,
                   kargs_loss: Dict[str, Any]):
        r"""
        Méthode privée d'une étape deévaluation.

        Parameters
        ----------
        data : List[Dict[str, Any]]
            Liste de dictionnaires sur les données d'un mini-batch.
        field_target : str
            Nom du champs de la target.
        loss_fn : Callable
            Fonction coût PyTorch.
        kargs_loss : Dict[str, Any]
            Dictionnaire d'arguments à utiliser dans la fonction de coût 
            loss_fun.

        Returns
        -------
        loss : Valeur de la fonction coût au travers du mini-batch.
        """
        self.eval()
        with torch.no_grad():
            output = self.forward(**data)
            target = check_tensor(data[field_target])
            loss = loss_fn(output, target, **kargs_loss)
        loss = loss.detach()
        self._divergence(loss)
        return loss

    def _iter_eval(self,
                   eval_dataset: DataLoader,
                   field_target: str,
                   loss_fn: Callable,
                   kargs_loss: Optional[Dict[str, Any]],
                   state: FitState,
                   control: FitControl,
                   list_callbacks: List[CallbackInterface]):
        r"""
        Méthode interne exécutant la phase d'évaluation durant l'apprentissage.
        Cette étape peut être appelé à la fin d'une époque ou durant 
        l'éxécution de l'époque (dépend de l'arguement iter_eval de la méthode 
        :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).

        Parameters
        ----------
        eval_dataset : DataLoader
            Dataset d'évaluation au format DataLoeader généré dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`.
        field_target : str
            Nom du champs target.
        loss_fn : Callable
            Fonction coût à minimiser (utiliser les fonctions présentes dans 
            torch.nn.functional). Si la fonction est une fonction custom, elle 
            doit avoir le prototypage suivant :
                - loss_fn(y_estim, y_true, reduction='sum', **kargs)
            avec une implémentation de réduction 'sum' pour les phases 
            d'évaluation et 'mean' pour les phases d'apprentissage.
        kargs_loss : Optional[Dict[str, Any]]
            Dictionnaire d'arguments à utiliser dans la fonction de coût 
            loss_fun.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancé dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        list_callbacks : List[CallbackInterface]
            Liste des callback permettant de contôler l'apprentissage durant 
            la phase d'évaluation.
        """
        list_callbacks.begin_eval(
            model=self,
            data=eval_dataset,
            state=state,
            control=control,
            res_loss=None
        )
        loss_eval = 0
        for jj, eval_batch in enumerate(eval_dataset):
            list_callbacks.begin_eval_step(
                model=self,
                data=eval_batch,
                state=state,
                control=control,
                res_loss=loss_eval/(jj+1)
            )
            try:
                loss_eval += self._eval_step(
                    data=eval_batch,
                    field_target=field_target,
                    loss_fn=loss_fn,
                    kargs_loss=kargs_loss
                )
            except DivergenceError as error:
                control.diverge = True
                warn(error.msg)
                break
        list_callbacks.end_eval(
            model=self,
            data=eval_dataset,
            state=state,
            control=control,
            res_loss=loss_eval/(jj+1)
        )

    def fit(self,
            X: Union[List[Dict[str, Any]], Dataset, DataLoader],
            y: Optional[List[Union[int, float]]]=None,
            eval_set: Optional[Union[List[Dict[str, Any]], Dataset]]=None,
            nb_epoch: int=5,
            iter_eval: Optional[int]=None,
            collate_fn: Optional[Callable]=None,
            loss_fn: Callable=l1_loss,
            kargs_loss: Dict[str, Any]=dict(),
            field_target: str='target',
            dataloader: bool=True,
            batch_size: int=32,
            shuffle: bool=True,
            drop_last: bool=False,
            num_workers: int=0,
            num_threads: Optional[int]=None,
            callbacks: List[CallbackInterface]=DEFAULT_CALLBACKS,
            swa_module: Optional[StochasticWeightAveraging]=None,
            rebuild: bool=False):
        r"""
        X : Union[List[Dict[str, Any]], Dataset, DataLoader]
            Dataset PyTorch contenant dans un dictionnaire les infos 
            nécessaires pour l'apprentissage du modèle.
        y : Optional[List[Union[int, float]]] (=None)
            Pour être ISO avec Scikit-learn. L'ensemble de l'apprentissage
            passera via X et le système DataSet et DataLoader de PyTorch.
        eval_set : Optional[Union[List[Dict[str, Any]], Dataset]] (=None)
            Dataset PyTorch contenant les observations et les targets 
            d'évaluation. Si eval_set est None alors pas de early stopping 
            et évaluation des performances sur les données d'entrainement 
            (déconseillé car très fort risque d'overfitting).
        nb_epoch : int (=5)
            Nombre d'époques max de l'apprentissage.
        iter_eval : Optional[int] (=None)
            Nombre d'itération entre deux évaluations. Actif seulement si 
            eval_set est non None. Si iter_eval est à None (définit par 
            défaut) les évaluations du modèle seront à la fin des époques. 
            Si un entier positif est renseigné les évaluations auront lieu 
            tous les iter_eval itérations d'apprentissage.
        collate_fn : Optional[Callable] (=None)
            Fonction de sortie de DataLoader permettant la concaténation en 
            batch des différentes observations du mini-batch.
        loss_fn : Optional[Callable] (=None)
            Fonction coût à minimiser (utiliser les fonctions présentes dans 
            torch.nn.functional). Si la fonction est une fonction custom, elle 
            doit avoir le prototypage suivant :
                - loss_fn(y_estim, y_true, reduction='sum', **kargs)
            avec une implémentation de réduction 'sum' pour les phases 
            d'évaluation et 'mean' pour les phases d'apprentissage.
        kargs_loss : Dict[str, Any] (=dict())
            Dictionnaire d'arguments à utiliser dans la fonction decoût 
            loss_fun. Si il n'y a pas d'arguments, mettre un dictionnaire 
            vide.
        field_target : str (='target')
            Nom du champ contenu dans X de la target. Par défaut "target". 
            Attention l'implémentation de la foction collate_fn, peut faire 
            changer le nom de la target.
        dataloader : bool (=True)
            Indique si la donnée X sera transformée en DataLoader ou non. Par 
            défaut True.
        batch_size : int (=32)
            taille du mini-batch. Pris en compte seulement si dataloader = 
            True.
        shuffle : bool (=True)
            Permet de mélanger à chaque époque les observations. Pris en 
            compte seulement si dataloader = True.
        drop_last : bool (=False)
            Drop les dernières observations si le rapport entre le nombre 
            d'observations et la taille du mini-batch est non entier. Pris en 
            compte seulement si dataloader = True.
        num_workers : int (=0)
            Nombre de process du DataLoader. Par défaut 0 correspondant à du 
            mono-thread. Pris en compte seulement si dataloader = True.
                - Attention :
                    1 -> mono-threadé mais isolé de l'environnement 
                    (Picklelisé). Si le DataLoader est utilisé dans un 
                    environnement Sciki-Learn multi-processing (par exemple 
                    pour un RandomizedSearchCV) il est très important de 
                    mettre cet argument à 0 pour que la DataLoader tourne 
                    dans l'environnement principale de Python. Dans le cas 
                    contraire le processus plantera.
        num_threads : Optional[int] (=None)
            Nombre de process des étapes d'inférence et de backpropagation des 
            gradients :
                - Si y est not None :
                    forcé à 1 ;
                - Si None :
                    utilise automatiquement le nombre de processeurs 
                    (et pas le nombre de threads) ;
                - Si un entier :
                    utilise le nombre de processus indiqué.
        callbacks : List[CallbackInterface] (=DEFAULT_CALLBACKS)
            Liste de callback intervenant aux différentes étapes de 
            l'entraînement et de l'évaluation. Pour avoir la liste des 
            différents callbacks implémentés par défaut voir 
            :func:`~dstk.pytorch._callback`. Par défaut utilise les 
            DEFAULT_CALLBACKS.
        swa_module : Optional[StochasticWeightAveraging] (=None)
            module permettant d'appliquer l'approche 
            `Stochastic Weight Averaging (SWA)`_. Voir la classe 
            :mod:`~dstk.pytorch._swa.StochasticWeightAveraging`.
        rebuild : bool (=False)
            Permet de reconstruire le réseau si, entre la définition de la 
            classe et le fit, il y a changement d'hyper-paramètres (exemple : 
            RandomizedSearchCV ou toute autre fonction Scikit-learn pouvant 
            utiliser set_params).

        Warnings
        --------
        Si le but du modèle est d'être utilisé avec d'autre module 
        Scikit-Learn il ne faut pas que le type de X soit un DataLoader 
        (les autres types reste valide). De manière général, pour la méthode 
        fit, il est conseillé d'utiliser le type DataSet PyTorch comme type 
        d'entré à X.

        Notes
        -----
        Pour le moment l'apprentissage sur GPU n'est pas pris en compte dans 
        où la fonction fit est appelé par un module Scikit-Learn (comme 
        RandomizedSearchCV par exemple).

        .. _Stochastic Weight Averaging (SWA): https://arxiv.org/abs/1803.05407
        """
        if not hasattr(self, 'optimizer'):
            raise NotImplementedError(
                "L'estimateur ne possède par d'objet 'optimizer'. Cette "
                "attribue doit être un objet d'otimisation de type PyTorch : "
                "torch.optim.(SGD, ADAM, etc.). Il faut le déclarer dans "
                "la construction de la classe modèle."
            )

        if iter_eval is not None and iter_eval < 0:
            raise AttributeError(
                "iter_eval doit être soit None ou un entier positif."
            )

        if swa_module:
            if not isinstance(swa_module, StochasticWeightAveraging):
                raise AttributeError(
                    "swa_module doit être de type StochasticWeightAveraging "
                    f"et non de type {type(swa_module).__name__}."
                )
            swa_module = swa_module.copy()

        list_callbacks = CallbackHandler(callbacks)
        list_callbacks.copy()

        id_processes = str(uuid.uuid1())

        # Si y est non None c'est que le processes passe par un search de
        # Scikit-Learn.
        if y is not None:
            torch.set_num_threads(1)
            num_workers = 0
            rebuild = True
        elif num_threads is not None:
            torch.set_num_threads(num_threads)
        else:
            torch.set_num_threads(torch.get_num_threads())

        if rebuild:
            self.build()

        if isinstance(X, dict):
            X = [X]

        if swa_module:
            X = swa_module.cut_dataset(
                dataset=X,
                field_target=field_target
            )

        if dataloader and not isinstance(X, DataLoader):
            dataset = DataLoader(
                dataset=X,
                collate_fn=collate_fn,
                shuffle=shuffle,
                drop_last=drop_last,
                batch_size=batch_size,
                num_workers=num_workers
            )
        else:
            dataset = X

        if eval_set:
            eval_dataset = DataLoader(
                dataset=eval_set,
                collate_fn=collate_fn,
                shuffle=False,
                drop_last=False,
                batch_size=16,
                num_workers=num_workers
            )
        else:
            eval_dataset = None

        state = FitState(
            id_process=id_processes,
            nb_epoch=nb_epoch,
            epoch_max_steps=len(dataset),
            eval_max_steps=len(eval_dataset) if eval_dataset else 0,
            loss_name=loss_fn.__name__
        )
        control = FitControl()

        list_callbacks.begin_train(self, dataset, state, control, None)
        for n_epoch in range(nb_epoch):
            state.n_epoch = n_epoch
            loss_epoch = 0
            list_callbacks.begin_epoch(
                model=self,
                data=dataset,
                state=state,
                control=control,
                res_loss=loss_epoch
            )
            for ii, batch in enumerate(dataset):
                state.n_iter = ii

                if (
                    eval_dataset and
                    self._mod(n_epoch*state.epoch_max_steps+ii, iter_eval) == 0
                ):
                    self._iter_eval(
                        eval_dataset=eval_dataset,
                        field_target=field_target,
                        loss_fn=loss_fn,
                        kargs_loss=kargs_loss,
                        state=state,
                        control=control,
                        list_callbacks=list_callbacks
                    )
                    if control.diverge or control.training_stop:
                        break

                list_callbacks.begin_step(self, batch, state, control, None)
                try:
                    loss_step = self._train_step(
                        data=batch,
                        field_target=field_target,
                        loss_fn=loss_fn,
                        kargs_loss=kargs_loss
                    )
                    loss_epoch += loss_step
                    list_callbacks.end_step(
                        model=self,
                        data=batch,
                        state=state,
                        control=control,
                        res_loss=loss_step
                    )
                except DivergenceError as error:
                    control.diverge = True
                    warn(error.msg)
                    break
            loss_epoch /= (ii+1)
            list_callbacks.end_epoch(self, dataset, state, control, loss_epoch)

            if eval_dataset and iter_eval is None:
                self._iter_eval(
                    eval_dataset=eval_dataset,
                    field_target=field_target,
                    loss_fn=loss_fn,
                    kargs_loss=kargs_loss,
                    state=state,
                    control=control,
                    list_callbacks=list_callbacks
                )
            if control.diverge or control.training_stop:
                break

        list_callbacks.end_train(self, dataset, state, control, None)

        if swa_module and not control.diverge:
            control.training_stop = False
            res_loss = loss_epoch
            if eval_dataset:
                early = [
                    ii for ii in list_callbacks.callbacks
                    if hasattr(ii, 'old_res_loss')
                ]
                if len(early) == 1:
                    res_loss = early[0].old_res_loss
            swa_module.init(
                model=self,
                res_loss=res_loss
            )
            swa_module.fit(
                model=self,
                eval_dataset=eval_dataset,
                loss_fn=loss_fn,
                kargs_loss=kargs_loss,
                field_target=field_target,
                iter_eval=iter_eval,
                collate_fn=collate_fn,
                batch_size=batch_size,
                shuffle=shuffle,
                drop_last=drop_last,
                num_workers=num_workers,
                state=state,
                control=control
            )
        return self
