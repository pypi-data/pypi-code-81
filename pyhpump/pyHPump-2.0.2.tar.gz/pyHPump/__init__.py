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

def communicationInitialization(port, baudrate):
    init_serial(port, baudrate)


def executeCommand(pump, command, waitForPump=False):
    send_command(pump.asciiAddress, command, waitForPump)


def definePump(address: str, type: util.PSDTypes, baudRate=9600, resolutionMode=0):
    if len(pumps) < pumpLength:
        newPump = PSD(address, type, baudRate, resolutionMode)
        send_command(newPump.asciiAddress, newPump.command.hEnableFactorCommands(True) + newPump.command.executeCommandBuffer())
        result = send_command(newPump.asciiAddress, newPump.command.syringeModeQuery(), True)
        resolution = result[3:4]
        newPump.setResolution(int(resolution))
        pumps.append(newPump)





