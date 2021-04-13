#!/usr/bin/env python
# coding: utf-8

import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
from openseespy.postprocessing.Get_Rendering import *

ops.wipe()

#Creación del modelo 
ops.model("BasicBuilder", "-ndm", 2, "-ndf", 3)

#Datos de la estructura
H_col=1.5 #float(input("Ingrese las dimensiones tranversal de la columna, altura: "))
B_col=1.5 #float(input("Ingrese las dimensiones tranversal de la columna, base: "))
h=12 #float(input("Ingrese la altura de la columna: "))
fuer_apli=8000 #float(input("Ingrese la fuerza aplicada a la columna: "))
fc=21000 #float(input("Ingrese la resistencia a la compresión: "))
pes_esp_hor=23.56
peso_ele=pes_esp_hor*H_col*B_col*h
peso_estru=peso_ele+fuer_apli
g=9.81
masa=peso_estru/g
masa_1=masa-323.896
Area=H_col*B_col
I=(1/12)*B_col*H_col**3
E=20000000

#Definir los nodos de la estructura

ops.node(1, 0, 0)
ops.node(2, 0, h)

#Restricciones    
ops.fix(1, 1, 1, 1)


#Definir la masa en la cabeza de la columna
ops.mass(2, masa, 1e-8, 1e-8)

# resistencia nominal a la compresión del hormigón
fc1=fc
Ec=E

# Definir la sección de columna
My_col=130000
Phi_Y_col=0.65e-4
EI_col_crack=My_col/Phi_Y_col
b=0.01

ops.uniaxialMaterial("Steel01", 2, My_col, EI_col_crack, b)
ops.uniaxialMaterial("Elastic", 3, Ec*Area)
ops.section("Aggregator", 1, 3, "P", 2, "Mz")

#Definir la transformacion de coordenadas
ops.geomTransf("PDelta", 1)
num_intgr_pts=5
ops.element("nonlinearBeamColumn", 1, 1, 2, num_intgr_pts, 1, 1)

# Propiedades del hormigón y acero
fc1=fc
Ec=E
fy=420000
fyh=420000
Es=200000000
shr=0.003

#Columnas
dia_bar_long=16
diametro=dia_bar_long/1000
num_arr_abajo=8
num_izq_der=4
dia_est=10
estribo=dia_est/1000
num_ram_Y=2
num_ram_X=2
recubrimiento=4
rec=recubrimiento/100
sep_est=0.1

# Definir el modelo de mander
eco=0.002
epss=0.004
esm=0.1
sp=sep_est*estribo
rs=(num_ram_X*estribo**2*(np.pi/4)*(B_col-2*rec)+num_ram_Y*estribo**2*(np.pi/4)*(H_col-2*rec))/((B_col-2*rec)*(H_col-2*rec)*sep_est)
area_var=diametro**2*(np.pi/4)
area_con=(B_col-2*rec)*(H_col-2*rec)
rcc=area_var*(num_arr_abajo+num_izq_der)/area_con
wi=0.2
ke=((1-wi**2/(6*area_con))*(1-sep_est/(2*B_col))*(1-sep_est/(2*H_col)))/(1-rcc)
fpl=1/(2*ke*rs*fyh)
fpcc=(-1.254+2.254*(1+7.94*fpl/fc1)**0.5-2*fpl/fc1)*fc1
ecc=eco*(1+5*(fpcc/(fc1-1)))
Esec=fpcc/ecc
r=Ec/(Ec-Esec)
ecu=1.5*(0.004+1.4*rs*fyh*(esm/fpcc))
x=ecu/ecc
fcu=fpcc*x*r/(r-1+x**r)

#Definir los materiales de la columna
#Concreto incofinado
ops.uniaxialMaterial("Concrete01", 4, -fc1, -eco, 0, -epss)

#Acero longitudinal
ops.uniaxialMaterial("Steel01", 5, fy, Es, shr)

#Concreto cofinado
ops.uniaxialMaterial("Concrete01", 6, -fpcc, -ecc, -fcu, -ecu)
ops.uniaxialMaterial("Elastic", 7, Ec)

#Creacion de las secciones
y0=B_col/2
y1=y0-rec
z0=H_col/2
z1=z0-rec
num_div_Z=16
num_div_Y=16
num_div_rec=2
ops.section("Fiber", 10)

# Definir los parches para recubriento lateral

crdsI=[-y0, -z0]
crdsJ=[-y1, -z0]
crdsK=[-y1, +z0]
crdsL=[-y0, +z0]

ops.patch("quad", 4, num_div_rec, (num_div_Z+2*num_div_rec), *crdsI, *crdsJ, *crdsK, *crdsL)

crdsI=[y1, -z0]
crdsJ=[y0, -z0]
crdsK=[y0, +z0]
crdsL=[y1, +z0]

ops.patch("quad", 4, num_div_rec, (num_div_Z+2*num_div_rec), *crdsI, *crdsJ, *crdsK, *crdsL)

# Definir los parches para recubriento inferior y superior
crdsI=[-y1, -z0]
crdsJ=[y1, -z0]
crdsK=[y1, -z1]
crdsL=[-y1, -z1]

ops.patch("quad", 4, num_div_Y, num_div_rec, *crdsI, *crdsJ, *crdsK, *crdsL)

crdsI=[-y1, -z1]
crdsJ=[y1, -z1]
crdsK=[y1, +z0]
crdsL=[-y1, +z0]

ops.patch("quad", 4, num_div_Y, num_div_rec, *crdsI, *crdsJ, *crdsK, *crdsL)

# Definir los parches para hormigon confinado
crdsI=[-y1, -z1]
crdsJ=[y1, -z1]
crdsK=[y1, z1]
crdsL=[-y1, z1]

ops.patch("quad", 6, num_div_Y, num_div_rec, *crdsI, *crdsJ, *crdsK, *crdsL)

# Acero superior e inferior
ops.fiber(0, z1, ((num_arr_abajo/2)*area_var), 5)
ops.fiber(0, -z1, ((num_arr_abajo/2)*area_var), 5)

# Acero superior e inferior
ops.fiber(y1, 0, ((num_izq_der/2)*area_var), 5)
ops.fiber(y1, 0, ((num_izq_der/2)*area_var), 5)

ops.section("Aggregator", 2, 7, "Vy", "-section", 10)

#Definir los recorders
ops.recorder("Node", "-file", "Despla_nodo_2.out", "-time", "-node", 2, "-dof", 1, 2, 3, "disp")
ops.recorder("Node", "-file", "Despla_nodo_1.out", "-time", "-node", 1, "-dof", 1, 2, 3, "disp")
ops.recorder("Node", "-file", "Reacc_Base.out", "-time", "-node", 1, "-dof", 1, 2, 3, "reaction")
ops.recorder("Element", "-file", "Fuerzas_Col.out", "-time", "-ele", 1, "globalForce")
ops.recorder("Element", "-file", "Fuerzas_Col_sec.out", "-time", "-ele", 1, "section", 10, "force")
ops.recorder("Element", "-file", "Defor_col_sec.out", "-time", "-ele", 1, "section", 10, "deformation")
ops.recorder("Element", "-file", "Fuerzas_Col_sec_num_intgr_pts.out", "-time", "-ele", 1, "section", num_intgr_pts, "force")
ops.recorder("Element", "-file", "Defor_Col_sec_num_intgr_pts.out", "-time", "-ele", 1, "section", num_intgr_pts, "force")

#Definir las actuantes sobre la columna
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
ops.eleLoad("-ele", 1, "-type", "-beamUniform", -masa)

#Parametros de analisis estatico
ops.constraints("Transformation")
ops.numberer("RCM")
ops.system("BandGeneral")
ops.test("EnergyIncr", 1e-8, 10, 0)
ops.algorithm("ModifiedNewton")
ops.integrator("Newmark", 0.5, 0.25)
ops.analysis("Transient")

#Analisis modal
Num_modos=1 #int(input("Ingrese el numero de modos a calcular: "))
OmegaSq=ops.eigen("-fullGenLapack", Num_modos)
OmegaSq=np.array(OmegaSq)
Omega=OmegaSq**0.5
Periodo=(2*np.pi)/Omega

for i in range(Num_modos):
    print("Modo", i+1, "T= ", Periodo[i], "s")
    
#Definir análisis dinamico
ops.loadConst("-time", 0)
Factor_x=0.01
Factor_y=0.01
dt=0.01
Npuntos=400
AccelDataFile_x="AAM2_201604162359_E_100.txt"
AccelDataFile_y="AAM2_201604162359_N_100.txt"
Dir_x=1
Dir_y=2
T_max=10
ops.timeSeries("Path", 2, "-dt", dt, "-filePath", AccelDataFile_x, "-factor", Factor_x)
ops.pattern("UniformExcitation", 2, Dir_x, "-accel", 2)

ops.timeSeries("Path", 3, "-dt", dt, "-filePath", AccelDataFile_y, "-factor", Factor_y)
ops.pattern("UniformExcitation", 3, Dir_y, "-accel", 3)

#Parametros de analisis estatico

ops.constraints("Plain")
ops.numberer("RCM")
ops.system("UmfPack")
ops.test("NormDispIncr", 1.0e-8, 10)
ops.algorithm("Newton")
ops.integrator("Newmark", 0.5, 0.25)
ops.analysis("Transient")
ops.analyze(Npuntos, dt)

Mek=np.loadtxt("Despla_nodo_2.out")
plt.figure()
plt.plot(Mek[:,0], Mek[:,1])
plt.ylabel('Desplazamiento horizontal (m)')
plt.xlabel('Tiempo (s)')
plt.savefig('DESPLAZAMIENTO NODO 2 VS TIEMPO.jpeg')
plt.show()

