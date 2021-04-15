#!/usr/bin/env python3
"""
Troisième exemple : Utilistation d'un multimètre.

La precision est donnée par le constructeur, avec en général, une contribution absolue (digit) et une contribution relative.
"""

import pygomme as pg
#import numpy as np  

u = pg.MeasureMultimeter(label="U/\mathrm{V}",   # pour les graphiques
                        title="Tension mesurée", # idem
                        value=5.184,             # valeur lue : 5.184 V 
                        precision_digit=8e-2,    # precision : 0.08 V
                        precision_relative=5e-3, # precision : 0.5 %
                        )

i = pg.MeasureMultimeter(label="I/\mathrm{A}",
                        title="Intensité mesurée",
                        value=0.1234,            # Valeur lue : 0.1234 A
                        precision_digit=10e-3,   # precision : 1 mA
                        precision_relative=1e-2) # precision : 1 % 

def ohm(u,i) :
    return u/i

r = pg.Propagation(label="R/\Omega",
                title="résistance $R$",
                function=ohm,
                argument=(u,i),
                n_sim = int(1e5))

# Création des graphiques
r.report(file="R-report.png")
r.report_partial(file="R-report_partial.png",gaussian=True)
