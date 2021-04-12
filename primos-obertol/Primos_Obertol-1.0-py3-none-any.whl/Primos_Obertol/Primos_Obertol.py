# Por mas que lo he intentado la libreria de R no me funciona, me dice que no tiene acceso tanto en windows como en Linux

# from rpy2 import robjects

# rpy2.robjects("print('Hola manola')"")

def es_primo(num):
    for n in range(2,num):
        if num % n == 0:
            return False
    return True

numero = input("Dame un numero: ")

for i in range(2,int(numero)):
    if es_primo (i):
        print ("Es primo: ", i)

