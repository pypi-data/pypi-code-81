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