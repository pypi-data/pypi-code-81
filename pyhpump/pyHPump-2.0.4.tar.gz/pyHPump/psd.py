from .commandPSD4 import *
from .commandPSD6 import *
from .commandPSD4SmoothFlow import *
from .commandPSD6SmoothFlow import *


class PSD:
    # default address in case that psd has address pin set on 0
    asciiAddress = "1"
    # default value id DIP switch bit 3 is OFF
    baudRate = 9600
    # standard resolution has value 0 = 3000 steps
    resolutionMode = 0

    def __init__(self, address: str, type: PSDTypes, baudRate=9600, resolutionMode=0):
        self.setAddress(address)
        self.type = type
        self.baudRate = baudRate
        self.resolutionMode = resolutionMode
        self.setCommandObj()

    def setCommandObj(self):
        if self.type == PSDTypes.psd6.value:
            self.command = CommandPSD6(type)
        elif self.type == PSDTypes.psd4.value:
            self.command = CommandPSD4(type)
        elif self.type == PSDTypes.psd4SmoothFlow.value:
            self.command = CommandPSD4SmoothFlow(type)
        elif self.type == PSDTypes.psd6SmoothFlow.value:
            self.command = CommandPSD6SmoothFlow(type)
        else:
            self.command = Command(type)

    def setAddress(self, address):
        translateAddress = {
            '0': "1",
            '1': "2",
            '2': "3",
            '3': "4",
            '4': "5",
            '5': "6",
            '6': "7",
            '7': "8",
            '8': "9",
            '9': ":",
            'A': ";",
            'B': "<",
            'C': "=",
            'D': ">",
            'E': "?",
            'F': "@",
        }
        self.asciiAddress = translateAddress.get(address)

    def setResolution(self, newResolutionMode: int):
        self.resolutionMode = newResolutionMode
        self.command.resolution_mode = newResolutionMode

    def setValve(self):
        #give permision for query commands
        pass
        #read DIP switch bits 4-6

    def print(self):
        print("Address: " + self.asciiAddress)
        print("Type: " + str(self.type))
        print("Baudrate: " + str(self.baudRate))
        print("Resolution mode: " + str(self.resolutionMode))
        print("Command object: " + str(self.command))

    def checkValidity(self):
        print("g_counter: " + str(self.command.command_g_counter))
        print("G_counter: " + str(self.command.command_G_counter))
        #TODO
        '''
        if (self.command.command_g_counter != 0 and (self.command.command_g_counter <= self.command.command_G_counter < self.command.command_g_counter + 1)):
            print("correct command")
        else:
            print("incorrect")
        '''

