def es_primo(num, n=2):
    if n >= num:
        print("Es primo")
        return True
    elif num % n != 0:
        return es_primo(num, n + 1)
    else:
        print("No es primo, el numero", n, "es divisor")
        return False
    

num = int(input('Escribe un numero: '))
resultado = es_primo(num)