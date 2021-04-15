#!/usr/bin/env python3

import pygomme as pg
import numpy as np  

"""
Premier exemple : Type A

Création d'un objet pygomme.MeasureA à partir de données expérimentales (bidonnées)
L'utilisateur indique la fonction de distribution qu'il veut utiliser. Celle-ci aura la même moyenne et le même écart-type que les données.
"""
measures = [4.534e3,4.524e3,4.555e3,4.566e3,4.514e3,4.508e3,4.535e3,4.507e3,
            4.534e3,4.574e3,4.576e3,4.535e3,4.584e3,4.594e3,4.524e3,4.556e3,]

re = pg.MeasureA(label="R/\Omega",       # label utilisé uniquement pour les graphiques
                title="Résistance $R$",  # idem
                experimental_data=measures, # listes des mesures (doit être itérables)  
                distribution=np.random.normal, # fonction de distribution utilisée
                )

re.histogram(n=int(1e5),    # Nombre de points utilisés pour le graphique
             file="Re-normal.png", # Nom du fichier graphique créé
             )

"""
Utilisation des mêmes données, mais avec une autre fonction de distribution.
"""
re.distribution = np.random.uniform # fonction de distribution utilisée

re.histogram(n=int(1e6),    # Nombre de points utilisés pour le graphique
             file="Re-uniform.png", # Nom du fichier graphique créé
             )

"""
Mesure de la vitesse du son. Exemple emprunté à M. Champion
"""

d = np.array([10, 13, 17, 20, 22, 26, 30, 33, 37, 40 ])*1e-2
tau = np.array([0.27, 0.38, 0.50, 0.59, 0.66, 0.73, 0.90, 0.96, 1.09, 1.15])*1e-3

c_exp = d/tau

c = pg.MeasureA(label="\\frac{c}{m/s}",
                title="Vitesse des ondes sonores",
                experimental_data=c_exp,
                )

print(f"La vitesse des ondes est {c} m/s.")

c.histogram(file="Celerite-1.png")

"""
Utilisation d'un second jeux de données.
"""
c.experimental_data = np.array([343.8, 339.2, 343.0, 343.9, 
                                340.5, 335.8, 344.3, 341.0, 
                                346.5, 337.9, 345])

c.histogram(file="Celerite-2.png")

print(f"La vitesse des ondes est {c} m/s.")

