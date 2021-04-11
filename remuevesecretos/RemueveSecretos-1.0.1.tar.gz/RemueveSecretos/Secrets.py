from RemueveSecretos.ManejadorDeArchivos import isExists
import json
from colorama import Fore, init, Style
init(autoreset = True)
class ClsSecrets:
    def __init__(self, secretosLista):
        if secretosLista != '':
            data = json.loads(secretosLista)
            try:
                self.rutaRepositorio = data['rutaRepositorio']
            except Exception as e:
                self.rutaRepositorio = ''
            try:
                self.listaSecretos = data['listaSecretos']
            except Exception as e:
                self.listaSecretos = []
        else:
            self.rutaRepositorio = ''
            self.listaSecretos = []
    def ValidaRuta(self):
        if self.rutaRepositorio != '':
            return True
        return False
    def ValidaListas(self):
        if len(self.listaSecretos) != 0:
            return True
        return False
    def leeRuta(self):
        correcto = True
        while correcto:
            ruta = self.IngresaRuta()
            correcto = self.PreguntaRepet(Fore.YELLOW + f'La ruta ingresada es {ruta} ¿Confirmar ruta? (S/SI) o (N/NO)')
        self.rutaRepositorio = ruta
    def leeSecretos(self):
        lssecretos = []
        correcto = True
        while correcto:
            lssecretos = self.IngresarSecretos()
            correcto = self.PreguntaRepet(Fore.YELLOW + f'Los secretos ingresados son {lssecretos} ¿Confirmar secretos? (S/SI) o (N/NO)')
        self.listaSecretos.extend(lssecretos)
    def IngresaRuta(self):
        ruta = input('Insgresa ruta del repositorio: ')
        if not isExists(ruta):
            print(Fore.RED + 'La ruta no es correcta')
            self.IngresaRuta()
        return ruta
    def IngresarSecretos(self):
        lssecretos = []
        addmore = False
        while not addmore:
            lssecretos.append(self.addSecret())
            addmore = self.PreguntaRepet(Fore.YELLOW + '¿Agregar otro secreto más? (S/SI) o (N/NO)')
        return lssecretos
    def addSecret(self):
        campo = input('Nombre del Secreto: ')
        valor = input('Ingresa el valor: ')
        return { 'Llave': campo.upper(), 'Valor': valor}
    def PreguntaRepet(self,texto):
        pregunta = input(texto)
        if pregunta.upper() == 'S' or pregunta.upper() == 'SI':
            return False
        elif pregunta.upper() == 'N' or pregunta.upper() == 'NO':
            return True
        else:
            self.PreguntaRepet(texto)
    def SaveSecrets(self):
        data = {}
        data['rutaRepositorio'] = self.rutaRepositorio
        data['listaSecretos'] = self.listaSecretos
        with open('secrets.dll', 'w') as outfile:
            json.dump(data, outfile, indent=4)
