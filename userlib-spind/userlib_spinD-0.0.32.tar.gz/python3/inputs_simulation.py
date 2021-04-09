import numpy as np
import sys
from python3.shell_commands import *

class InputPhys():

    def __init__(self, system=None, file=None):
        if file:
            self.load_inp(file)
        elif system == 'PdFeIr_fcc':
            self.load_PdFeIr()
        else:
            self.load_empty()


    def load_PdFeIr(self):
        self.exc = [14.4046e-3,
                    -2.48108e-3,
                    -2.68507e-3,
                    0.520605e-3,
                    0.73757e-3,
                    0.277615e-3,
                    0.160881e-3,
                    -0.57445e-3,
                    -0.212654e-3]
        self.dmi = [1.0e-3]
        self.ani = [-0.7e-3]
        self.sp3 = [0.0]
        self.sp4 = [0.0]
        self.biq = [0.0]

    def load_empty(self):
        self.exc = [0]
        self.dmi = [0]
        self.ani = [0]
        self.sp3 = [0]
        self.sp4 = [0]
        self.biq = [0]


    def load_inp(self, file):
        self.exc = []
        self.dmi = []
        self.sp3 = []
        self.sp4 = []
        self.biq = []
        self.ani = []
        with open(file, 'r') as f :
            while True:
                buf = f.readline()
                if not buf:
                    break
                words = buf.split()
                for word in words:

                    # check magnetic field
                    if word == 'H_ext': self.H_ext = [float(words[1]), float(words[2]), float(words[3])]
                    elif word == 'J_1' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_2' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_3' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_4' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_5' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_6' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_7' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_8' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_9' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_10' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_11' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_12' : self.exc.append(float(words[1][:-3])*1e-3)
                    elif word == 'J_B' : self.biq.append(float(words[1][:-3])*1e-3)
                    elif word == 'K_1' : self.sp4.append(float(words[1][:-3])*1e-3)
                    elif word == 'Y_1' : self.sp3.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_ani' : self.ani.append(float(words[1][:-3])*1e-3)
                    # check DMI constants
                    elif word == 'D_1' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_2' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_3' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_4' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_5' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_6' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_7' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_8' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_9' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_10' : self.dmi.append(float(words[1][:-3])*1e-3)
                    elif word == 'D_11' : self.dmi.append(float(words[1][:-3])*1e-3)
