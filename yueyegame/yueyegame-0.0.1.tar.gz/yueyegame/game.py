from time import*
from turtle import*
from os import*
def stamp(something,speed = 0.1,FT = 1):
    for i in something:
        print(i,end='')
        sleep(speed)
    if FT == 1:
        print()
    sleep(0.5)
def clear():
    print("\033[4J""")
    print("\033[99999A")
def loadto(a):
    b = 0
    for i in range(a):
        clear()
        b = 0
        print("\033[47m",str(i+1),"%\033[0m")
        sleep(0.1)
def loadfor(a):
    run = ["-","\\","|","/"]
    n = 0
    for i in range(a*5):
        if n == 4:
            clear()
            n = 0
            print(run[n])
            sleep(0.1)
        else:
            clear()
            print(run[n])
            n += 1
            sleep(0.1)
def load():
    run = ["-","\\","|","/"]
    n = 0
    for i in range(10*5):
        if n == 4:
            clear()
            n = 0
            print(run[n])
            sleep(0.1)
        else:
            clear()
            print(run[n])
            n += 1
            sleep(0.1)
def showlogo(a):
    for i in range(len(a)):
        if a[i] == "0":
            print("\033[0m ",end="")
        elif a[i] == "1":
            print("\033[41m ",end="")
        elif a[i] == "2":
            print("\033[42m ",end="")
        elif a[i] == "3":
            print("\033[43m ",end="")
        elif a[i] == "4":
            print("\033[44m ",end="")
        elif a[i] == "5":
            print("\033[45m ",end="")
        elif a[i] == "6":
            print("\033[46m ",end="")
        elif a[i] == "7":
            print("\033[47m ",end="")
        elif a[i] == "a":
            print("\033[30m",end="")
        elif a[i] == "b":
            print("\033[31m",end="")
        elif a[i] == "c":
            print("\033[32m",end="")
        elif a[i] == "d":
            print("\033[33m",end="")
        elif a[i] == "e":
            print("\033[34m",end="")
        elif a[i] == "f":
            print("\033[35m",end="")
        elif a[i] == "g":
            print("\033[36m",end="")
        elif a[i] == "h":
            print("\033[37m",end="")
        else:
            print(a[i],end="")
    print("\033[0m")
def steap(something1,speed1 = 0.1,ft = 1):
    clear()
    stamp(something1,speed1,ft)
def turprint(some,size,place):
    pen = Turtle()
    pen.hideturtle()
    pen.penup()
    write(some,align=place,font=("微软雅黑", size,"normal"))
def playmp4(mpf):
    system(mpf)