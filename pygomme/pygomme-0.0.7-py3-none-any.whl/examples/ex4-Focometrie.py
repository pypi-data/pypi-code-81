#!/usr/bin/env python3
"""
Focométrie
"""

import numpy as np  
import pygomme as pg

xA = pg.MeasureB(label="x_A/m",
                title="Position de l'objet",
                value=0.112,
                half_width=2e-3,
                distribution=np.random.uniform,)

xAp = pg.MeasureB(label="x_A'/m",
                title="Position de l'image",
                value=1.122,
                half_width=2e-3,
                distribution=np.random.uniform,)

xO = pg.MeasureB(label="x_O/m",
                title="Position de la lentille",
                value=0.352,
                half_width=4e-3,
                distribution=np.random.uniform,)

def focometrie(xA,xAp,xO):
    fp = 1/(1/(xAp-xO)-1/(xA-xO))
    return fp

fp = pg.Propagation(label="f'/m",
                title="Distance focale",
                function=focometrie,
                argument=[xA,xAp,xO],
                n_sim=int(1e6))  

# Création des graphiques :
fp.report(file="Fp-report.png")
fp.report_partial(file="Fp-report_partial.png")
