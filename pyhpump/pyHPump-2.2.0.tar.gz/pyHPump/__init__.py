from .psd import *
from .communication import *
from .util import *
from .command import *
from .commandPSD4 import *
from .commandPSD4SmoothFlow import *
from .commandPSD6 import *
from .commandPSD6SmoothFlow import *


#List of pumps. Initially the list is empty
pumps = []
pumpLength = 16

def connect(port, baudrate):
    initializeSerial(port, baudrate)

def disconnect():
    disconnectSerial()

def executeCommand(pump, command, waitForPump=False):
    if pump.checkValidity(command):
        sendCommand(pump.asciiAddress, command, waitForPump)

def definePump(address: str, type: util.PSDTypes, baudRate=9600, resolutionMode=0):
    if len(pumps) < pumpLength:
        newPump = PSD(address, type, baudRate, resolutionMode)
        print("Enable h Factor Commands and Queries")
        sendCommand(newPump.asciiAddress, newPump.command.enableHFactorCommandsAndQueries() + newPump.command.executeCommandBuffer())
        result = sendCommand(newPump.asciiAddress, newPump.command.syringeModeQuery(), True)
        resolution = result[3:4]
        newPump.setResolution(int(resolution))
        pumps.append(newPump)