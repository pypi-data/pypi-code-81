"""RemueveSecretos - Remueve o muestra secretos para desarrollo evitando filtrar informacion no deseada en nube"""
from RemueveSecretos.RemueveSecrets import HideSecrets
from RemueveSecretos.RegresaSecrets import ShowSecrets
import os
__version__ = '1.0.0'
__author__ = 'FrEaKAlL <sercal0121@gmail.com>'
__all__ = ['Opcion']

def Opcion():
    print('Que desea hacer');
    opcion = input('Oprimir O o escribir ocultar para ocultar los secretos o M o Mostrar para revelar los secretos')
    if (opcion.upper() == 'O' or opcion.upper() == 'OCULTAR'):
        HideSecrets()
    elif(opcion.upper() == 'M' or opcion.upper() == 'MOSTRAR'):
        ShowSecrets()
    else:
        cotinuar = input('La opcion es incorrecta volver a intentar (S/SI) o (N/NO)')
        if (cotinuar.upper() == 'S' or cotinuar.upper() == 'SI'):
            Opcion()
        else:
            os.exit()
