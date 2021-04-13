
class Saludo():

    nombre = "Darwin Calle"
    
    def __init__(self, nombre):
        self.nombre = nombre
        print(f"Hola Mundo desde Python: {self.nombre} , paquete.")

    def saludar(self):
        print(f"Hola : {self.nombre} desde funcion.")
    
    