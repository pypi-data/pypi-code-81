#-------------------------------------------------------------------------------
# Name:        PyMV
# Author:      d.fathi
# Created:     10/04/2021
# Copyright:   (c) d.fathi 2021
# Version:     0.0.0
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#https://stackoverflow.com/questions/6560354/how-would-i-create-a-custom-list-class-in-python
'''
class PyMV(list):
    def __init__(self, *args):
        super().__init__()
        print(len(args))
    def __str__(self):
        return "PyMV V:0.0.0"
'''


def main():
    from PyVM import PyVM
    a = PyVM((1,2,3), 35, 22)
    a+=[[4,2,3]]
    print(type(a))
    print(a)


if __name__ == '__main__':
    main()
