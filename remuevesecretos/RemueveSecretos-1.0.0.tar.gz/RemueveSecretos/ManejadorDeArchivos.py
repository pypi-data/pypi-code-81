from os import listdir
from os import path
import codecs
def ls(lista = [], ruta = '.'):
    for arch in listdir(ruta):
        if path.isfile(ruta + '/' + arch):
            lista.append(ruta + '/' + arch)
        elif path.isdir(ruta + '/' + arch):
            if (ruta + '/' + arch).find('__pycache__') == -1:
                ls(lista, ruta + '/' + arch)
    return lista
def isExists(ruta):
    if path.exists(ruta):
        return True
    return False
def readFile(ruta, byline = False):
    if path.exists(ruta):
        file = codecs.open(ruta, 'r', encoding = 'utf-8', errors = 'ignore')
        if byline:
            lineas = file.readlines()
            file.close()
            return lineas
        else:
            contenido = file.read()
            file.close()
            return contenido
    if byline:
        return []
    else:
        return ''
def writeFile(ruta, contenido):
    if path.exists(ruta):
        file = codecs.open(ruta, 'w', encoding = 'utf-8')
        file.write(contenido)
        file.close()
