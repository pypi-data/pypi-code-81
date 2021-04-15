#!/usr/bin/env python3
"""
Régression linéaire.

Exemple emprunté à Maxime Champion.
"""
import numpy as np  
import pygomme as pg

frequences = np.array([11.825,10.111,8.210,7.4129,6.8838])*100
u_frequences = np.array([2.3,1.7,1.1,0.91,0.79])

ec = np.array([2.40,1.69,0.91,0.57,0.35])
u_ec = 0.05

frequence = pg.MeasureB(label="\\frac{\\nu}{THz}",
                        title="Fréquence",
                        value=frequences,
                        scale =u_frequences,
                        distribution = np.random.normal,
                        )

energie = pg.MeasureB(label="\\frac{E_c}{eV}",
                      title="Énergie cinétique",
                      value=ec,
                      scale=u_ec,
                      distribution = np.random.normal,
                      )

lf = pg.LinearFit(x=frequence,
                  y=energie,
                  n=int(1e3))

print(lf)
print(lf.a)
print(lf.b)

lf.a.label = "a"
lf.a.histogram(file="a-hist.png")
lf.b.histogram(file="b-hist.png")
lf.report(file="Planck-report.png")

"""
Étude sans tenir compte de la corrélation entre a et b
"""

def constante_de_planck(a):
    h = a*1.602e-19*1e-12
    return h

def frequence_seuil(a,b):
    fs = -b/a
    return fs

h = pg.Propagation(label="h/(Js)",
                   title="Constante de Planck",
                   function=constante_de_planck,
                   argument=(lf.a,),
                   n_sim=int(1e5))

fs1 = pg.Propagation(label="\\frac{\\nu_1}{THz}",
                   title="Fréquence seuil sans corrélation",
                   function=frequence_seuil,
                   argument=(lf.a,lf.b),
                   n_sim=int(1e5))

h.histogram(file="h-hist.png")
fs1.report(file="fs-hist.png")

print(f"La constante de Planck est {h} J/s.")
print(f"La fréquence seuil est {fs1} THz.")

"""
Étude en tenant compte de la corrélation entre a et b
"""

ab = lf.ab
ab.a_label = "a"
ab.b_label = "b"
ab.scatter(file="ab-scatter.png")

fs_cor = -ab.b/ab.a

fs2 = pg.MeasureA(label="\\frac{\\nu_2}{THz}",     
                title="avec corrélation",  
                experimental_data=fs_cor, 
                distribution=np.random.normal,
                )

print(f"La fréquence seuil est {fs2} THz.")

cfs = fs1 // fs2

cfs.report(file="frequence-seuil-12.png")

"""
Étude en créant un objet pygomme.correlation
"""

data_a = lf.a.experimental_data
data_b = lf.b.experimental_data

ab2 = pg.Correlation(labels=["$a$","$b$"],
                titles=["pente","ordonnées à l'origine"],
                keys=['a','b'],
                color="gray",
                values=[data_a,data_b],)

ab2.compute_cov()

print(ab2.cov)

ab2.create_samples(n=int(1e5))

#print(ab2.samples['a'])

ab2.scatter(x=ab2.quantity['a'].samples(),
           y=ab2.quantity['b'].samples(),
           file="ab2-scatter.png")

def frequence_seuil(x,y):
    fs = -y/x
    return fs

fs3 = pg.Propagation(label="\\frac{\\nu_3}{THz}",
                   title="Fréquence seuil avec pygomme.correlation",
                   function=frequence_seuil,
                   argument=(ab2.quantity['a'],ab2.quantity['b']),
                   n_sim=int(1e6))

print(f"La fréquence seuil est {fs3} THz.")

cfs13 = fs1 // fs3

cfs13.report(file="frequence-seuil-13.png")

cfs23 = fs2 // fs3

cfs23.report(file="frequence-seuil-23.png")

