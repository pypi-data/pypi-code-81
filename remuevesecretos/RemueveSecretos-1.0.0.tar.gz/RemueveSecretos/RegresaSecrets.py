#!/usr/bin/python
from progress.bar import Bar, ChargingBar
from colorama import Fore, init, Style
init(autoreset = True)
from RemueveSecretos.ManejadorDeArchivos import readFile, writeFile, ls, readFile
from RemueveSecretos.Secrets import ClsSecrets
def IniciaFlujoSecretos(Secretos):
    lista = []
    lista = ls(lista,Secretos.rutaRepositorio)
    barra = ChargingBar(Fore.GREEN + 'Escaneando: ', max=len(lista))
    resultado = []
    for file in lista:
        contenido = readFile(file)
        Cambios = False
        Mensaje = ''
        for secret in Secretos.listaSecretos:
            if contenido.find(secret['Llave']) != -1:
                val = secret['Llave']
                Mensaje += f'\t{file} - Secreto encontrado: {val}\n'
                contenido = contenido.replace(secret['Llave'], secret['Valor'])
                Cambios = True
        if Cambios:
            writeFile(file, contenido)
            Mensaje += f'\tSecretos guardados en {file}'
        if Mensaje != '':
            resultado.append(Mensaje)
            Mensaje = ''
        barra.next()
    barra.finish()
    for msg in resultado:
        print(Fore.YELLOW + msg)
def ShowSecrets():
    print(Style.BRIGHT + Fore.CYAN + '1. - Verifica si existen secretos configurados')
    secretos = readFile('secrets.dll')
    if len(secretos) == 0:
        print(Fore.RED + 'No cuenta con los secretos requeridos para este proyecto')
    else:
        Secretos = ClsSecrets(secretos)
        if Secretos.listaSecretos != []:
            print(Style.BRIGHT + Fore.CYAN + '2. - Inicia flujo de obtencion de secretos')
            IniciaFlujoSecretos(Secretos)
            print(Style.BRIGHT + Fore.CYAN + '3. - Fin de secretos')
        else:
            print(Fore.RED + 'El archivo de secretos no cuenta con secretos a obtener')
