# Librairie de fonctions utiles
# @author : Pauline Delpierre <pauline.delpierre@univ-lille.fr>,
#           Oliver Irwin <oliver.irwin.etu@univ-lille.fr>
# @date : 12/04/2021

import matplotlib.pyplot as plt
import pandas as pd
from typing import *

def day_night_cycle(ax, alpha = 0.15, border = True, bcolor = 'k') :
    """
    Ajoute un cadre pour les jours et les nuits

    :param ax: La figure sur laquelle ajouter
    :type ax: matplotlib.axes._subplots.AxesSubplot
    :param alpha: l'opacité de la nuit
    :type alpha: float
    :param border: s'il faut ajouter des bordures aux nuits
    :type border: bool
    :param bcolor: couleur des bordures
    :type bcolor: char

    :note: Mettre les limites avant d'appeler la fonction
    """

    limits = ax.get_xlim()
    timeInterval = limits[1]

    nbDays = int(timeInterval // 24)

    for i in range(nbDays) :
        nightStart = (24 * i) + 12
        nightEnd   = 24 * (i + 1)
        ax.axvspan(nightStart, nightEnd, facecolor = 'k', alpha = alpha)

        # If we need a border
        if border :
            ax.axvline(x = nightStart, linewidth = 0.5, color = bcolor)
            ax.axvline(x = nightEnd, linewidth = 0.5, color = bcolor)

def add_days_to_df(df : pd.Dataframe, nb_days : int = 2) -> pd.DataFrame :
    """
    Ajoute des jours de manière periodique à un jeu de données

    :param df: Le jeu de données
    :type df: pd.Dataframe
    :param nb_days: le nombre de jours, defaults to 2
    :type nb_days: int, optional
    :return: Le nouveau jeu de données
    :rtype: pd.Dataframe
    """

    init  = df.copy()
    final = df.copy()

    for i in range(nb_days) :
        # Copier l'original
        tmp = init.copy()

        # Ajouter les jours
        tmp["Time"] = tmp["Time"].apply(lambda x : x + ((i + 1) * 24))

        # Ajouter le jeu de données à la suite
        final.append(tmp)
    
    # Régler les indices
    final.reset_index(drop = True, inplace = True)

    return final

