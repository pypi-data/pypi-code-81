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
            if contenido.find(secret['Valor']) != -1:
                val = secret['Valor']
                Mensaje += f'\t{file} - Secreto encontrado: {val}\n'
                contenido = contenido.replace(secret['Valor'], secret['Llave'])
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
def HideSecrets():
    print(Style.BRIGHT + Fore.CYAN + '1. - Verifica si existen secretos configurados')
    secretos = readFile('secrets.dll')
    if len(secretos) == 0:
        print('No hay secretos configurados')
        Secretos = ClsSecrets('')
        if not Secretos.ValidaRuta():
            Secretos.leeRuta()
        if not Secretos.ValidaListas():
            Secretos.leeSecretos()
        Secretos.SaveSecrets()
        print(Style.BRIGHT + Fore.CYAN + '2. - Inicia flujo para ocultar secretos')
        IniciaFlujoSecretos(Secretos)
        print(Style.BRIGHT + Fore.CYAN + '3. - Fin de secretos')
    else:
        print(Style.BRIGHT + Fore.CYAN + '2. - Valida si existe ruta para el repositorio y secretos')
        Secretos = Secrets.ClsSecrets(secretos)
        if Secretos.rutaRepositorio == '':
            print(Style.BRIGHT + Fore.CYAN + '2.1. - Inserta Ruta')
            if not Secretos.ValidaRuta():
                Secretos.leeRuta()
        if Secretos.listaSecretos == []:
            print(Style.BRIGHT + Fore.CYAN + '2.2. - Inserta Secretos')
            if not Secretos.ValidaListas():
                Secretos.leeSecretos()
        Secretos.SaveSecrets()
        print(Style.BRIGHT + Fore.CYAN + '3. - Inicia flujo para ocultar secretos')
        IniciaFlujoSecretos(Secretos)
        print(Style.BRIGHT + Fore.CYAN + '4. - Fin de secretos')
