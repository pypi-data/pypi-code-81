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
H_col=2 #float(input("Ingrese las dimensiones tranversal de la columna, altura: "))
B_col=2 #float(input("Ingrese las dimensiones tranversal de la columna, base: "))
h=12 #float(input("Ingrese la altura de la columna: "))
fuer_apli=15000 #float(input("Ingrese la fuerza aplicada a la columna: "))
#fc=float(input("Ingrese la resistencia a la compresión: "))
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

#Definir la masa de la estructura

ops.mass(2, masa_1, 0, 0)

#Definir las restricciones
ops.fix(1, 1, 1, 1)

#Definir la transformacion geometrica
ops.geomTransf("Linear", 1)

#Definir elemento de la columna
ops.element("elasticBeamColumn", 1, 1, 2, Area, E, I, 1)

#Definir los recorders
ops.recorder("Node", "-file", "despla_col.out", "-time", "-node", 2, "-dof", 1, 2, 3, "disp")


#Definir las actuantes sobre la columna
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
ops.load(2, 0, (-1*masa*g), 0)


#Definir análisis dinamico
ops.loadConst("-time", 0)
Factor=0.01
dt=0.01
Npuntos=14000
AccelDataFile="AAM2_201604162359_E_100.txt"
Dir=1
ops.timeSeries("Path", 2, "-dt", dt, "-filePath", AccelDataFile, "-factor", Factor)
ops.pattern("UniformExcitation", 2, Dir, "-accel", 2)


#Parametros de analisis estatico

ops.constraints("Plain")
ops.numberer("RCM")
ops.system("UmfPack")
ops.test("NormDispIncr", 1.0e-8, 10)
ops.algorithm("Newton")
ops.integrator("Newmark", 0.5, 0.25)
ops.analysis("Transient")
ops.analyze(Npuntos, dt)

    
Mek=np.loadtxt("despla_col.out")
plt.figure()
plt.plot(Mek[:,0], Mek[:,1])
plt.ylabel('Desplazamiento horizontal (m)')
plt.xlabel('Tiempo (s)')
plt.savefig('DESPLAZAMIENTO NODO 2 VS TIEMPO.jpeg')
plt.show()



nodo=[1, 2]
dof=[1, 2, 3]

nodo1=nodo[0]
nodo2=nodo[1]

gra_liber1=dof[0]
gra_liber2=dof[1]
gra_liber3=dof[2]

#Resultados
print("El desplazamiento en el nodo:", nodo2, "para el grado de libertad:", gra_liber1, "es:", ops.nodeDisp(2, 1), "m" )
print("El desplazamiento en el nodo:", nodo2, "para el grado de libertad:", gra_liber2, "es:", ops.nodeDisp(2, 2), "m" )
print("El desplazamiento en el nodo:", nodo2, "para el grado de libertad:", gra_liber2, "es:", ops.nodeDisp(2, 3), "rad/s" )


