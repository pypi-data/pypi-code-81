from time import *
from os import*
def stamp(something,speed = 0.1,FT = 1):
    for i in something:
        print(i,end='')
        sleep(speed)
    if FT == 1:
        print()
    sleep(0.5)
def clear():
    print("\033[2J""")
    print("\033[99999A")
def clean():
    system("clear")
def cout(*a):
    if type(a) == list and len(a) > 1:
        for i in a:
            b = str(i)
            print(",",end = "")
            for j in b:
                print(j,end = "")
                sleep(0.1)
    else:
        for f in a:
            c = str(f)
            for h in c:
                print(h,end = "")
                sleep(0.1)
def showhclogo():
    print("\033[47m")
    print("\033[47m         \033[0m")
    print("\033[47m             \033[0m")
    print("\033[47m         \033[0m   \033[47m \033[0m")
    print("\033[47m             \033[0m")
    print("\033[47m         \033[0m")
    print("\033[0m \033[47m       \033[0m")
    print("\033[41m\033[33m")
    print("©红茶工作室 红茶工作室·月夜工作组 版权所有")
    print("\033[0m")
    print("\033[1;33m红茶系统：代码运行结束")
    print("\033[8m")
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
        elif a[i] == "b":
            print("\033[30m",end="")
        elif a[i] == "r":
            print("\033[31m",end="")
        elif a[i] == "g":
            print("\033[32m",end="")
        elif a[i] == "y":
            print("\033[33m",end="")
        elif a[i] == "b":
            print("\033[34m",end="")
        elif a[i] == "p":
            print("\033[35m",end="")
        elif a[i] == "c":
            print("\033[36m",end="")
        elif a[i] == "w":
            print("\033[37m",end="")
        else:
            print(a[i],end="")
    print("\033[0m")
def say(a):
    with open("asd.vbs","w") as f:
        f.write('CreateObject("SAPI.SpVoice").Speak"%s"'%a)
    system("asd.vbs")