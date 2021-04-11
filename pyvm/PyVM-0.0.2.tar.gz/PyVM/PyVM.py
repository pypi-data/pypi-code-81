#-------------------------------------------------------------------------------
# Name:        PyVM
# Author:      d.fathi
# Created:     10/04/2021
# Copyright:   (c) d.fathi 2021
# Version:     0.0.0.1
# Licence:     <your licence>
#-------------------------------------------------------------------------------



class PyVM(list):
    def __init__(self, *args):
        super().__init__()
        print(len(args))
    def __str__(self):
        return "PyVM V:0.0.1"


def main():
    a = PyVM((1,2,3), 35, 22)
    a+=[[4,2,3]]
    print(type(a))
    print(a)


if __name__ == '__main__':
    main()
