#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modules callback.

Created on Sat Jan  9 10:42:31 2021

@author: Cyrile Delestre
"""

import os
import sys
from abc import abstractmethod
from copy import deepcopy
from typing import List, Dict, Optional, Callable, Any, NewType
from dataclasses import dataclass, field

import numpy as np
from torch import Tensor
from tqdm import tqdm

from dstk.utils.meta_interface import SuperclassDocstring

# Permet d'éviter une initialisation circulaire via l'import de
# BaseEnvironnement
PyTorchEstimators = NewType('PyTorchEstimators', Any)

@dataclass
class FitState:
    r"""
    Classe contenant les informations sur l'apprentissage.

    Parameters
    ----------
    id_process : str
        Identifiant du processus.
    nb_epoch : int
        Nombre d'époques du processus d'apprentissage.
    epoch_max_steps : int
        Nombre d'itérations à l'intérieur d'une époque.
    eval_max_steps : int
        Nombre d'itérations à l'intérieur de la phase d'évaluation.
    loss_name : str
        Nom de la fonction coût.
    n_iter : int (=0)
        Numéro de l'itération en cours.
    n_epoch : int (=0)
        Numéro de l'époque en cours.
    n_iter_swa : int (=0)
        Numéro de l'itération en cours durant le processus SWA.
    n_epoch_swa : int (=0)
        Numéro de l'époque en cours durant le processus SWA.
    nb_epoch_swa : int (=0)
        Nombre d'époques pour le processus SWA.
    """
    id_process: str
    nb_epoch: int
    epoch_max_steps: int
    eval_max_steps: int
    loss_name: str
    n_iter: int = 0
    n_epoch: int = 0
    n_iter_swa: int = 0
    n_epoch_swa: int = 0
    nb_epoch_swa: int = 0

@dataclass
class FitControl:
    r"""
    Classe permettant de contôler le flux d'appretissage.

    Parameters
    ----------
    training_stop : bool
        Booléen indiquant si le processus d'apprentissage doit stopper ou non.
    diverge : bool
        Booléen indiquant si le processus d'apprentissage a divergé ou non.
    """
    training_stop: bool = False
    diverge: bool = False

class CallbackInterface:
    r"""
    Classe interface permettant de définir des modules utilisés durant 
    l'apprentissage de la méthode 
    :func:`~dstk.pytorch._base.BaseEnvironnement.fit` du module 
    :mod:`~dstk.pytorch._base.BaseEnvironnement`. Cette interface permet de 
    personnaliser facilement un callback.

    Notes
    -----
    Les méthodes qui sont appelées durant l'apprentissage :
        begin_train :
            au début de train : avant toute itération d'entrainement
        end_train :
            à la fin de train : après toute itération de récupération du 
            meilleur modèle
        begin_step :
            au début d'un batch d'apprentissage à chaque itération d'une 
            époque
        end_step :
            à la fin d'un batch d'apprentissage à chaque itération d'une 
            époque
        begin_epoch :
            au début d'une époque d'apprentissage
        end_epoch :
            à la fin d'une époque d'apprentissage
        begin_eval :
            au début d'une évaluation à la fin d'une époque
        end_eval :
            à la fin d'une évaluation à la fin d'une époque
        begin_eval_step :
            au début d'un batch d'évaluation à chaque itération d'une époque 
            d'évaluation

    Warnings
    --------
    Classe en cours de dév et non utilisée dans la méthode d'apprentissage 
    :func:`~dstk.pytorch._base.BaseEnvironnement.fit`.
    """
    def copy(self):
        r"""
        Créer une copie de l'objet.
        """
        return deepcopy(self)

    @abstractmethod
    def begin_train(self,
                    model: PyTorchEstimators,
                    data: List[Dict[str, Tensor]],
                    state: FitState,
                    control: FitControl,
                    res_loss: None,
                    **kwargs) -> None:
        r"""
        Méthode appelée au début de train : avant toute itération 
        d'entrainement.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def end_train(self,
                  model: PyTorchEstimators,
                  data: List[Dict[str, Tensor]],
                  state: FitState,
                  control: FitControl,
                  res_loss: None,
                  **kwargs) -> None:
        r"""
        Méthode appelée à la fin de train : après toute itération de 
        récupération du meilleur modèle.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def begin_epoch(self,
                    model: PyTorchEstimators,
                    data: List[Dict[str, Tensor]],
                    state: FitState,
                    control: FitControl,
                    res_loss: float,
                    **kwargs) -> None:
        r"""
        Méthode appelée au début d'une époque d'apprentissage.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def end_epoch(self,
                  model: PyTorchEstimators,
                  data: List[Dict[str, Tensor]],
                  state: FitState,
                  control: FitControl,
                  res_loss: float,
                  **kwargs) -> None:
        r"""
        Méthode appelée à la fin d'une époque d'apprentissage.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def begin_step(self,
                   model: PyTorchEstimators,
                   data: List[Dict[str, Tensor]],
                   state: FitState,
                   control: FitControl,
                   res_loss: None,
                   **kwargs) -> None:
        r"""
        Méthode appelée au début d'une étape d'apprentissage.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def end_step(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
        r"""
        Méthode appelée à la fin d'un étape d'apprentissage.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def begin_eval(self,
                   model: PyTorchEstimators,
                   data: List[Dict[str, Tensor]],
                   state: FitState,
                   control: FitControl,
                   res_loss: None,
                   **kwargs) -> None:
        r"""
        Méthode appelée au début d'une évaluation à la fin d'une époque.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def end_eval(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
        r"""
        Méthode appelée à la fin d'un évaluation à la fin d'une époque.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

    @abstractmethod
    def begin_eval_step(self,
                        model: PyTorchEstimators,
                        data: List[Dict[str, Tensor]],
                        state: FitState,
                        control: FitControl,
                        res_loss: float,
                        **kwargs) -> None:
        r"""
        Méthode appelée au début d'une étape de validation.

        Parameters
        ----------
        model : PyTorchEstimators
            Référence au modèle sur lequel l'apprentissage se déroule.
        data : Iterable
            Data sous forme de liste ou d'un DataLoader.
        state : FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control : FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        res_loss : float
            Valeur de la fonction coût.
        """
        pass

class CallbackHandler(CallbackInterface):
    r"""
    Classe handler permettant de gérer simplement une liste de callbacks.
    """
    def __init__(self, callbacks: Optional[List[CallbackInterface]]):
        type_cb = list(
            map(lambda x: isinstance(x, CallbackInterface), callbacks)
        )
        if not all(type_cb):
            list_name = [
                cb.__class__.__name__ for ii, cb in enumerate(callbacks)
                if not type_cb[ii]
            ]
            raise AttributeError(
                f"Les callbacks {', '.join(list_name)} ne sont pas de type "
                "CallbackInterface."
            )
        order = [
            0 if cc.__class__.__name__=='ProgressBarCallback' else ii
            for ii, cc in zip(range(1, len(callbacks)+1), callbacks)
        ]
        callbacks = list(
            map(
                lambda x: x[1],
                sorted(zip(order, callbacks), key=lambda x: x[0])
            )
        )
        self.callbacks = callbacks

    def copy(self):
        self.callbacks = [cb.copy() for cb in self.callbacks]

    def begin_train(self,
                    model: PyTorchEstimators,
                    data: List[Dict[str, Tensor]],
                    state: FitState,
                    control: FitControl,
                    res_loss: float,
                    **kwargs) -> None:
        self.call('begin_train', model, data, state, control, res_loss, **kwargs)

    def end_train(self,
                  model: PyTorchEstimators,
                  data: List[Dict[str, Tensor]],
                  state: FitState,
                  control: FitControl,
                  res_loss: float,
                  **kwargs) -> None:
        self.call('end_train', model, data, state, control, res_loss, **kwargs)

    def begin_epoch(self,
                    model: PyTorchEstimators,
                    data: List[Dict[str, Tensor]],
                    state: FitState,
                    control: FitControl,
                    res_loss: float,
                    **kwargs) -> None:
        self.call('begin_epoch', model, data, state, control, res_loss, **kwargs)

    def end_epoch(self,
                  model: PyTorchEstimators,
                  data: List[Dict[str, Tensor]],
                  state: FitState,
                  control: FitControl,
                  res_loss: float,
                  **kwargs) -> None:
        self.call('end_epoch', model, data, state, control, res_loss, **kwargs)

    def begin_step(self,
                   model: PyTorchEstimators,
                   data: List[Dict[str, Tensor]],
                   state: FitState,
                   control: FitControl,
                   res_loss: float,
                   **kwargs) -> None:
        self.call('begin_step', model, data, state, control, res_loss, **kwargs)

    def end_step(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
        self.call('end_step', model, data, state, control, res_loss, **kwargs)

    def begin_eval(self,
                   model: PyTorchEstimators,
                   data: List[Dict[str, Tensor]],
                   state: FitState,
                   control: FitControl,
                   res_loss: float,
                   **kwargs) -> None:
        self.call('begin_eval', model, data, state, control, res_loss, **kwargs)

    def end_eval(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
        self.call('end_eval', model, data, state, control, res_loss, **kwargs)

    def begin_eval_step(self,
                        model: PyTorchEstimators,
                        data: List[Dict[str, Tensor]],
                        state: FitState,
                        control: FitControl,
                        res_loss: float,
                        **kwargs) -> None:
        self.call('begin_eval_step', model, data, state, control, res_loss, **kwargs)

    def call(self,
             step: str,
             model: PyTorchEstimators,
             data: List[Dict[str, Tensor]],
             state: FitState,
             control: FitControl,
             res_loss: float,
             **kwargs) -> None:
        for cb in self.callbacks:
            getattr(cb, step)(model, data, state, control, res_loss, **kwargs);

@dataclass
class PrintCallback(CallbackInterface):
    r"""
    Callback simple permettant d'afficher la performance du modèle en cours 
    d'apprentissage après l'évaliation.
    """
    def end_eval(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
        print(
            f"\nid : {state.id_process}\n"
            f"Epoch : {state.n_epoch+1}/{state.nb_epoch}, "
            f"{state.loss_name} : {res_loss:.4f}\n",
            flush=True
        )

@dataclass
class EarlyStoppingCallback(CallbackInterface, metaclass=SuperclassDocstring):
    r"""
    Callback de gestion du early-stopping. Permet de sauvegarder la meilleure 
    itération durant l'apprentissage. Si un early_stopping_rounds est donné 
    alors l'apprentissage se stoppe si la performance n'a pas été meilleure au 
    bout de ces early_stopping_rounds itérations.

    Parameters
    ----------
    path_early_stopping : Optional[str] (=None)
        Chemin (absolu ou relatif) où le modèle par early stopping sera 
        préservé. Si None, les paramètres seront sauvegardés en RAM. 
        Cependant il est déconseillé de le faire car les réseaux profonds 
        peuvent être très gourmands en espace RAM. De même, en cas de 
        plantage, un état du réseau pouvant être satisfaisant est préservé 
        sur le disque dur.
    early_stopping_rounds : Optional[int] (=None)
        Nombre d'itérations (epoch) sans amélioration. Si None pas de 
        early stopping, le modèle sauvegardé sera donc le meilleur modèle 
        durant l'ensemble des époques.
    minimize : bool (=True)
        Indique si l'objectif est de minimiser la fonciton coût (True) ou 
        de la maximiser (False).
    verbose : bool (=False)
        Indique les informations de gain de performance.
    """
    path_early_stopping: Optional[str] = None
    early_stopping_rounds: Optional[int] = None
    minimize: bool = True
    verbose: bool = False

    def __post_init__(self):
        self.old_res_loss = (np.inf if self.minimize else -np.inf)
        self.iter_stop: int = 0
        self.best_epoch: int = 0
        self.best_iter: int = 0

    def end_eval(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
            if (
                    res_loss < self.old_res_loss 
                    if self.minimize else 
                    res_loss > self.old_res_loss
            ):
                if self.verbose:
                    print(
                        "\nGain de performance époque/itération : "
                        f"{state.n_epoch+1}/{state.n_iter+1} ;\n"
                        f"Gain de performance {state.loss_name} :\n"
                        f"{self.old_res_loss} -> {res_loss}.\n",
                        flush=True
                    )
                self.iter_stop = 0
                self.old_res_loss = res_loss
                self.best_epoch = state.n_epoch
                self.best_iter = state.n_iter
                if self.path_early_stopping is None:
                    self.state_dict = model._extract_state(model)
                else:
                    model.save_weights(
                        f"{self.path_early_stopping}/{state.id_process}.model"
                    )
            elif (
                    self.early_stopping_rounds is not None and 
                    (
                        res_loss >= self.old_res_loss 
                        if self.minimize else
                        res_loss <= self.old_res_loss
                    )
            ):
                self.iter_stop += 1
                if self.iter_stop >= self.early_stopping_rounds:
                    control.training_stop = True

    def end_train(self,
                  model: PyTorchEstimators,
                  data: List[Dict[str, Tensor]],
                  state: FitState,
                  control: FitControl,
                  res_loss: float,
                  **kwargs) -> None:
        if self.verbose:
            print(
                f"\nMeilleure époque/iteration : {self.best_epoch+1}/"
                f"{self.best_iter+1}\n"
                f"Meilleure performance {state.loss_name} : "
                f"{self.old_res_loss}.\n",
                flush=True
            )
        if self.path_early_stopping is None:
            model.load_state_dict(self.state_dict)
        else:
            model.load_weights(
                f"{self.path_early_stopping}/{state.id_process}.model"
            )
            os.remove(f"{self.path_early_stopping}/{state.id_process}.model")

@dataclass
class LRSchedulerCallback(CallbackInterface, metaclass=SuperclassDocstring):
    r"""
    Classe de gestion du learning rate. Ce callback ne met à jour le 
    learning rate que durant les périodes d'évaluation.

    Parameters
    ----------
    lr_scheduler : Callable
        Classe non instanciée d'un planificateur de learning rate. Les 
        planificateurs de learning rate se situent dans 
        torch.optim.lr_scheduler et permettent de contrôler le lerning rate au 
        travers des époques.
    scheduler_kwargs : Dict[str, Any] (=dict())
        Argument d'entrée de scheduler (en dehors de l'optimizer qui doit 
        être inclu à l'intérieur de la classe du réseau). Explicitement 
        l'instanciation sera faite dans la méthode fit sera du type :
            lr_scheduler(self.optimizer, **scheduler_kwargs)
    verbose : bool (=True)
        Permet d'affichier le lerning rate initial et les évolutions du 
        learning rate quand ils ont lieu. Par défaut cette argument est 
        à True car la sortie n'est pas très verbeuse.

    Notes
    -----
    Si l'entrainement ne possède pas de dataset d'évaluation aucune mise à 
    jour de learning rate ne sera fait durant l'entrainement par 
    l'intermédiaire de ce callback.
    """
    lr_scheduler: Callable
    scheduler_kwargs: Dict[str, Any] = field(default_factory=dict)
    verbose: bool = True

    def begin_train(self,
                    model: PyTorchEstimators,
                    data: List[Dict[str, Tensor]],
                    state: FitState,
                    control: FitControl,
                    res_loss: float,
                    **kwargs) -> None:
        self.scheduler = self.lr_scheduler(
            model.optimizer,
            **self.scheduler_kwargs
        )
        if self.verbose:
            self.old_lr = model.optimizer.state_dict()['param_groups'][0]['lr']
            print(
                f"A l'initialisation le lr = {self.old_lr}\n",
                flush=True
            )

    def end_eval(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
        if self.lr_scheduler.__name__ == "ReduceLROnPlateau":
            self.scheduler.step(res_loss)
        else:
            self.scheduler.step()
        if self.verbose:
            lr = model.optimizer.state_dict()['param_groups'][0]['lr']
            if self.old_lr != lr:
                print(
                    f"\nA l'époque {state.n_epoch+1} itération "
                    f"{state.n_iter+1} le learning rate a évolué :\n"
                    f"{self.old_lr} -> {lr}.\n",
                    flush=True
                )
                self.old_lr = lr

@dataclass
class ProgressBarCallback(CallbackInterface, metaclass=SuperclassDocstring):
    r"""
    Barre de progression TQDM sur les époques et les évaluations.

    mininterval : float
        Temps en seconde entre les intervalles de raffraichissement de la 
        barre de progression. Par défaut 0.5.
    bar_epoch : bool
        Indication si la barre de progression sera exécutée sur une époque 
        d'apprentissage durant l'entrainement. Par défaut True.
    bar_eval : bool
        Indication si la barre de progression sera exécutée sur une époque 
        d'évaluation durant l'entrainement. Par défaut False.
    """
    mininterval: float = 0.5
    bar_epoch: bool = True
    bar_eval: bool = False
    _swa_process: bool = False

    def begin_epoch(self,
                    model: PyTorchEstimators,
                    data: List[Dict[str, Tensor]],
                    state: FitState,
                    control: FitControl,
                    res_loss: float,
                    **kwargs) -> None:
        if self.bar_epoch:
            self.epoch_bar = tqdm(
                total=state.epoch_max_steps,
                desc=(
                    f"Epoque {state.n_epoch_swa+1}/{state.nb_epoch_swa}"
                    if self._swa_process else
                    f"Epoque {state.n_epoch+1}/{state.nb_epoch}"
                ),
                mininterval=self.mininterval,
                leave=True,
                file=sys.stdout
            )

    def end_epoch(self,
                  model: PyTorchEstimators,
                  data: List[Dict[str, Tensor]],
                  state: FitState,
                  control: FitControl,
                  res_loss: float,
                  **kwargs) -> None:
        if self.bar_epoch:
            self.epoch_bar.refresh()
            self.epoch_bar.close()

    def begin_step(self,
                   model: PyTorchEstimators,
                   data: List[Dict[str, Tensor]],
                   state: FitState,
                   control: FitControl,
                   res_loss: float,
                   **kwargs) -> None:
        if self.bar_epoch:
            self.epoch_bar.update(1)

    def begin_eval(self,
                   model: PyTorchEstimators,
                   data: List[Dict[str, Tensor]],
                   state: FitState,
                   control: FitControl,
                   res_loss: None,
                   **kwargs) -> None:
        if self.bar_eval:
            self.eval_bar = tqdm(
                total=state.eval_max_steps,
                desc="Evaluation",
                mininterval=self.mininterval
            )

    def end_eval(self,
                 model: PyTorchEstimators,
                 data: List[Dict[str, Tensor]],
                 state: FitState,
                 control: FitControl,
                 res_loss: float,
                 **kwargs) -> None:
        if self.bar_eval:
            self.epoch_bar.refresh()
            self.eval_bar.close()

    def begin_eval_step(self,
                        model: PyTorchEstimators,
                        data: List[Dict[str, Tensor]],
                        state: FitState,
                        control: FitControl,
                        res_loss: float,
                        **kwargs) -> None:
        if self.bar_eval:
            self.eval_bar.update(1)

DEFAULT_CALLBACKS = [
    ProgressBarCallback(),
    PrintCallback(),
    EarlyStoppingCallback()
]
