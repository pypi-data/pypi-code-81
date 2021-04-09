from time import *
from turtle import *
from os import*
def stamp(something,speed = 0.1,FT = 1):
    for i in something:
        print(i,end='')
        sleep(speed)
    if FT == 1:
        print()
    sleep(0.5)
def turprint(some,size,place):
    pen = Turtle()
    pen.hideturtle()
    pen.penup()
    write(some,align=place,font=("微软雅黑", size,"normal"))
def clear():
    print("\033[2J""")
    print("\033[99999A")
def clean():
    system("clear")
def steap(something1,speed1 = 0.1,ft = 1):
    clear()
    stamp(something1,speed1,ft)
def playmp4(mpf):
    system(mpf)