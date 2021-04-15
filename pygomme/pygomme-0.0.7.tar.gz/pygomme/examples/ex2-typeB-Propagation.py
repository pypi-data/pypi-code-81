#!/usr/bin/env python3
"""
Second exemple : Type B et propagation.

Création de plusieurs objets pygomme.MeasureB, avec différentes fonctions de distribution.
Création de deux objets pygomme.Propagation pour étudier la propagation des erreurs en utilisant la méthode CdL.
"""
import pygomme as pg
import numpy as np  

r1 = pg.MeasureB(label="R_1/\Omega",      # label pour les graphiques
                title="Résistance $R_1$", # idem
                value=9.8e3,              # valeur moyenne 
                half_width=0.2e3,         # demi-largeur de la distribution
                distribution=np.random.uniform, # choix d'une distribution uniforme
                )

r2 = pg.MeasureB(label="R_2/\Omega", 
                title="Résistance $R_2$",
                value=15.3e3,       # valeur moyenne
                scale=0.2e3,        # déviation standard 
                distribution = np.random.normal, # choix d'une loi normale
                )

# Création des fichiers contenant les courbes
r1.histogram(gaussian=True, # Affichage d'une gaussienne de même moyenne et écart-type
             n=int(1e4),  # Nombre de points pour l'histogramme
             file="R1-hist.png",  # Fichier de sortie
             )
r2.histogram(gaussian=True, n=int(1e4), file="R2-hist.png")

# Fonction ancillaire pour l'étude de la propagation des erreurs.
# Cette fonction doit être vectorisée et être utilisable avec des paramètres
# de type numpy.ndarray
def parallele(ra,rb):
    r = ra*rb/(ra+rb)
    return r

# 
rp = pg.Propagation(label="R_p/\Omega", # Utilisé pour le graphiques
                    title="Résistance $R_p$", # idem
                    function=parallele,  # fonction de propagation des erreurs
                    argument=[r1,r2],   # objets pygomme
                    n_sim=int(1e5),  # Nombre de points pour la simulation CdL
                    )

# Tracé d'une figure avec la distribution pour les deux résistances R1 et R2
# et pour la résistance de l'association parrallèle.
rp.histogram(file="Rp.png",
             gaussian=True)

# Les valeurs moyenne et l'écart-type de Rp sont accessibles :
print("La valeur moyenne de Rp est {:.0f} Ω".format(rp.average()))

print("L'écart-type de Rp est {:.0f} Ω".format(rp.deviation()))

# Mais on peut aussi utiliser directement la fonction print() :
print(rp)

# La méthode report permet de créer une figure avec l'histogramme
# de distribution des trois résistances.
rp.report(file="Rp.png")

#
# Propagation d'erreurs avec une grandeur de type A et une de type B
#
rpp = pg.Propagation(label="R_p'/\Omega", # Utilisé pour le graphiques
                    title="Résistance $R_p'$", # idem
                    function=parallele,  # fonction de propagation des erreurs
                    argument=[r1,r2],   # objets pygomme
                    n_sim=int(1e6),  # Nombre de points pour la simulation CdL
                    )

rpp.report(file="Rpp.png")
rpp.report_partial(file="Rpp-partial.png")

# On ajoute deux autres résisances.
r3 = pg.MeasureB(label="R_3/\Omega",
                title="Résistance $R_3$",
                value=12.5e3 ,
                half_width=0.5e3 ,
                distribution=np.random.triangular,)

r4 = pg.MeasureB(label = "R_4/\Omega",
                title="Résistance $R_4$",
                value = 11.3e3,
                scale = 0.4e3,
                distribution = np.random.normal,)

# Association des quatre résistances.
def parallele_serie(r1,r2,r3,r4):
    r = r1*r2/(r1+r2) + r3*r4/(r3+r4)
    return r

rps = pg.Propagation(label = "R_{ps}/\Omega",
                    title="Résistance $R_{ps}$",
                    function=parallele_serie,
                    argument=[r1,r2,r3,r4],
                    n_sim=int(1e5))

# Figure avec les histogrammes des cinq résistances.
rps.report(file="Rps.png")

# Figure qui permet d'évaluer l'influence des différents paramètres.
# Pour les quatre premières courbes, la simulation CdL est faite en n'utilisant
# que la distribution d'une des quatre résistances, les autres étant prises égales à
# leur valeur moyenne.
rps.report_partial(file="Rps-partial.png")

# Calcul et écriture de l'écart normalisé entre Rp et Rps:
print(rps-rp)
# que l'on utilisera correctement:
print("L'écart normalisé est {:.2f}".format(rps-rp))

# Création d'une grandeur de référence :
r_ref = pg.Reference(label = "R_{réf}/\Omega",
                     title="Résistance $R_{réf}$",
                     value=11.8e3)

# Affichage de l'écart normalisé entre Rps et R_ref :
print("L'écart normalisé est {:.2f}".format(rps-r_ref))

# Création d'un objet pygomme.Compare qui permet de comparer les 
# histogrammes de deux objets pygomme.
d = rps // r_ref
d.report(file="D-report.png",n=int(2e5))
d.report(file="D-report-lr.png",n=int(2e3))

# Création d'une nouvelle mesure Rt
rt = pg.MeasureB(label = "R_t/\Omega",
                title="Résistance $R_t$",
                value = 11.3e3 ,
                scale = 0.4e3 ,
                distribution = np.random.normal,
                )

# Calcul et écriture de l'écart normalisé entre Rps et Rt:
print(rps-rt)

# Création d'un objet pygomme.Compare
c = rps // rt
# une syntaxe équivalente : C = pg.Compare(A=Rps,B=Rt)
# 
# Affichage des histogrammes :
c.report(file="C-report.png",n=int(2e5))
c.report(file="C-report-lr.png",n=int(2e3))
