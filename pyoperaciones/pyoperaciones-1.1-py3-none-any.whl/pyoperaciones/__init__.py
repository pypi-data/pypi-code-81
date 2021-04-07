#Programa mediante el cual se calculan todos los números primos que encontramos entre 1 y el valor "n" proporcionado por el usuario.

def numerosPrimos(numero):

    numero = int(input("Ingrese un número entero positivo: "))

    if numero > 0:

        for i in range (2, numero+1):

            creciente = 2

            esPrimo = True
     
            while esPrimo and creciente < i:

                if i % creciente == 0:

                    esPrimo = False
            
                else:
                
                    creciente += 1

            if esPrimo:

                print(i, "es primo.")
        
                            
    else:
        
        print("El número ingresado no es correcto. Inténtelo de nuevo")