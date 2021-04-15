#!/usr/bin/env python3
"""
Calorimétrie

Exemple repris de 
https://www.ac-paris.fr/portail/jcms/p2_2334447/ressources-numeriques-mesures-et-incertitudes-bcpst-n1?cid=p1_2333951&portal=piapp1_59010
"""
import numpy as np  
import pygomme as pg

at = 0.1 # Demi-étendue pour les températures T1 et T2
atf = 1 # Demi-étendue pour la température Tf
am = 0.5 # Demi-étendue pour les masses

t1 = pg.MeasureB(label="T_1/°C",
                 title="Température de l'eau froide",
                 value=20.2,
                 half_width=at,
                 distribution=np.random.uniform)

t2 = pg.MeasureB(label="T_2/°C",
                 title="Température de l'eau chaude",
                 value=47.3,
                 half_width=at,
                 distribution=np.random.uniform)

tf = pg.MeasureB(label="T_f/°C",
                 title="Température finale",
                 value=31.2,
                 half_width=atf,
                 distribution=np.random.triangular)

m1i = pg.MeasureB(label="m_{1i}/\mathrm{g}",
                  title="Masse du bécher 1 plein",
                  value=153,
                  half_width=am,
                  distribution=np.random.uniform)

m1f = pg.MeasureB(label="m_{1f}/\mathrm{g}",
                  title="Masse du bécher 1 vide",
                  value=99,
                  half_width=am,
                  distribution=np.random.uniform)

m2i = pg.MeasureB(label="m_{2i}/\mathrm{g}",
                  title="Masse du bécher 2 plein",
                  value=176,
                  half_width=am,
                  distribution=np.random.uniform)

m2f = pg.MeasureB(label="m_{2f}/\mathrm{g}",
                  title="Masse du bécher 2 vide",
                  value=119,
                  half_width=am,
                  distribution=np.random.uniform)

def capacite(t1,t2,tf,m1i,m1f,m2i,m2f):
    c = 4.185*((m2i-m2f)*(t2-tf)/(tf-t1)+(m1f-m1i))
    return c

c_cal = pg.Propagation(label="C_{cal}/(J/K)",
                       title="Capacité thermique du calorimètre",
                       function=capacite,
                       argument=[t1,t2,tf,m1i,m1f,m2i,m2f],
                       n_sim = int(1e6),
                       )

c_cal.report("Ccal-report.png")
c_cal.report_partial("Ccal-report_partial.png")
