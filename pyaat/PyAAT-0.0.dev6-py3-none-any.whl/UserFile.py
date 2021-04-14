"""
Python Aerospace Analysis Toolbox - PyAAT
Copyright (c) 2021 Kenedy Matiasso Portella
Distributed under MIT License

This is the user file.
"""

from system import system
from atmosphere import atmosCOESA
from aircraft import Aircraft
from propulsion import SimpleModel
from gravity import NewtonGravity
from control import equilibrium, doublet, step

from tools import printInfo
from tools import plotter

from numpy.linalg import eig

atm = atmosCOESA()
prop = SimpleModel()
airc = Aircraft()
grav = NewtonGravity()
cont = equilibrium()

Mysys = system(atmosphere =atm, propulsion = prop, aircraft = airc, gravity=grav)


#from performance import Envelope
#Envelope(Mysys, plot = True, limits = [0,400], )


Xe, Ue = Mysys.trimmer(condition='turn', HE = 5000, VE= 150, dPS = 2, BTA =0)
"""

printInfo(Xe, Ue, frame ='body')
printInfo(Xe, Ue, frame ='aero')
printInfo(Xe, Ue, frame='controls')


doub = doublet()
doub.command = 'elevator'
doub.amplitude = 3
doub.T = 1
doub.t_init = 2

doub2 = doublet()
doub2.command = 'rudder'
doub2.amplitude = 3
doub2.T = 1
doub2.t_init = 2

st =step()
st.command = 'aileron'
st.amplitude = 1
st.t_init = 2

#solution, control = Mysys.propagate(Xe, Ue, TF =10, perturbation=True, state={'alpha': 5, 'beta':2})
#solution, control = Mysys.propagate(Xe, Ue, TF =100, perturbation=True, control = [doub, doub2, st])
solution, control = Mysys.propagate(Xe, Ue, TF = 180, perturbation = False)

pltr = plotter()
pltr.states = solution
pltr.time = Mysys.time
pltr.control = control

pltr.LinVel(frame = 'body')
pltr.LinVel(frame = 'aero')
pltr.LinPos()
pltr.Attitude()
pltr.AngVel()
pltr.Controls()
pltr.LinPos3D()
pltr.linPos2D()
"""

A, B = Mysys.e(Xe, Ue)
Ald, Bld = Mysys.LinearLatero(Xe,Ue)
Al, Bl =Mysys.LinearLong(Xe,Ue)
wld, vld = eig(Ald)
wl, vl = eig(Al)

print('--------------------------------')
print('Eigenvalues longitudinal')
print(wl)

Asp, Bsp = Mysys.shortPeriod(Xe, Ue)
wsp, vsp = eig(Asp)
print('--------------------------------')
print('Eigenvalues short period')
print(wsp)

Aph, Bph = Mysys.phugoid(Xe, Ue)
wph, vph = eig(Aph)

print('--------------------------------')
print('Eigenvalues phugoid')
print(wph)