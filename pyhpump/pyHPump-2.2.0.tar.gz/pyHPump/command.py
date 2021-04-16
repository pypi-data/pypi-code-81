from .util import *


class Command:
    resolution_mode = 0

    def __init__(self, type: PSDTypes):
        self.type = type

    """
    Zx - Initialize PSD/4, Assign Valve Output to Right
    Yx - Initialize PSD/4, Assign Valve Output to Left
    Wx - Initialize PSD/4, Configure for No Valve
    """

    def initialize(self, drive: str, value=0):
        cmd: str = ''
        if drive == 'Z' or drive == 'Y' or drive == 'W':
            cmd += drive
        else:
            print("Error! Incorrect drive!")
            cmd = 'cmdError'
            return cmd
        if (value == 1) or (value >= 10 and value <= 40):
            cmd += str(value)
        return cmd

    """
    R - Execute Command Buffer
    X - Execute Command Buffer from Beginning
    """

    def executeCommandBuffer(self, type='R'):
        cmd: str = ''
        if type == 'R' or type == 'X':
            cmd += type
        else:
            print("Error! Incorrect type!")
            cmd = 'cmdError'
        return cmd

    """
        Syringe Commands
    """

    def setCounterPosition(self):
        return 'z'

    def absolutePosition(self, value):
        cmd: str = 'A'
        cmd += str(value)
        return cmd

    def relativePickup(self, value: int):
        cmd: str = 'P'
        cmd += str(value)
        return cmd

    def relativeDispense(self, value: int):
        cmd: str = 'D'
        cmd += str(value)
        return cmd

    def returnSteps(self, value: int):
        cmd: str = 'K'
        cmd += str(value)
        return cmd

    def backoffSteps(self, value: int):
        cmd: str = 'k'
        cmd += str(value)
        return cmd

    '''
        Valve Commands
    '''

    def moveValveToInputPosition(self, value=0):
        cmd: str = 'I'
        if value == 0:
            print("Default command!")
        elif 1 <= value <= 8:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Move valve to input position command!")
        return cmd

    def moveValveToOutputPosition(self, value=0):
        cmd: str = 'O'
        if value == 0:
            print("Default command!")
        elif 1 <= value <= 8:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Move valve to output position command!")
        return cmd

    def moveValveToBypass(self):
        return 'B'

    def moveValveToExtraPosition(self):
        return 'E'

    """
        Action commands
    """

    def definePositionInCommandString(self):
        cmd: str = 'g'
        return cmd

    # Gx - Repeat Commands
    def repeatCommands(self, value=0):
        cmd: str = 'G'
        if value == 0:
            print("default value for Repeat Commands")
        elif 1 <= value <= 65535:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Repeat Commands command!")

        return cmd

    # Mx - Delay - performs a delay of x milliseconds.where 5 ≤ x ≤ 30,000 milliseconds.
    def delay(self, value: int):
        cmd: str = 'M'
        if 5 <= value <= 30000:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Delay command!")
        return cmd

    # Hx - Halt Command Execution
    def halt(self, value: int):
        cmd: str = 'H'
        if 0 <= value <= 2:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Halt command!")
        return cmd

    # Jx - Auxiliary Outputs
    def auxiliaryOutputs(self, value: int):
        cmd: str = 'J'
        if 0 <= value <= 7:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Auxiliary Outputs command!")
        return cmd

    # sx - Store Command String
    def storeCommandString(self, location: int, command: str):
        cmd: str = 's'
        if 0 <= location <= 14:
            cmd += str(location)
            cmd += command
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Store Command String command!")
        return cmd

    # ex - Execute Command String in EEPROM Location
    def executeCommandStringInEEPROMLocation(self, location: int):
        cmd: str = 'e'
        if 0 <= location <= 14:
            cmd += str(location)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Execute Command String in EEPROM Location command!")
        return cmd

    def terminateCommandBuffer(self):
        return 'T'

    """
        Motor Commands
    """

    def setAcceleration(self, value: int):
        cmd: str = 'L'
        if 0 <= value <= 20:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for set acceleration command!")
        return cmd

    def setSpeed(self, value: int):
        cmd: str = 'S'
        if 1 <= value <= 40:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for set speed command!")
        return cmd

    def increaseStopVelocityBySteps(self, value: int):
        cmd: str = 'C'
        if 0 <= value <= 25:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for Increase Stop Velocity by Steps command!")
        return cmd

    def setStartVelocity(self, value: int):
        cmd: str = 'v'
        if 50 <= value <= 1000:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for set start velocity command!")
        return cmd

    def setMaximumVelocity(self, value: int):
        cmd: str = 'V'
        if 2 <= value <= 5800:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for set maximum velocity command!")
        return cmd

    def stopVelocity(self, value: int):
        cmd: str = 'c'
        if 50 <= value <= 2700:
            cmd += str(value)
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for stop velocity command!")
        return cmd

    """
        h30001 - Enable h Factor Commands and Queries
        h30000 - Disable h Factor Commands and Queries
    """

    def enableHFactorCommandsAndQueries(self):
        cmd: str = 'h30001'
        return cmd

    def disableHFactorCommandsAndQueries(self):
        cmd: str = 'h30000'
        return cmd

    def resetPSD(self):
        return "h30003"

    def initializeValve(self):
        return "h20000"

    def initializeSyringeOnly(self, speedCode: int):
        cmd: str = 'h'
        cmdValue = 10000
        # permitted values between 0-40
        if 0 <= speedCode <= 40:
            cmdValue += speedCode
        cmd += str(cmdValue)
        return cmd

    def setSyringeMode(self, mode: int):
        cmd: str = 'h'
        cmdValue = 11000
        # permitted values between 0-15
        if 0 <= mode <= 15:
            cmdValue += mode
        cmd += str(cmdValue)
        print("default syringe mode method call")
        print(cmd)
        return cmd

    def enableValveMovement(self):
        cmd: str = 'h20001'
        return cmd

    def disableValveMovement(self):
        cmd: str = 'h20002'
        return cmd

    def setValveType(self, type: int):
        cmd: str = 'h2100'
        # permitted values between 0-6
        if 0 <= type <= 6:
            cmd += str(type)
        return cmd

    def moveValveToSpecificPositionInShortestDirection(self, specificPosition: PositionInShortestDirection):
        cmd: str = 'h2300'
        cmd += str(specificPosition.value)
        return cmd

    def moveValveClockwiseDirection(self, position: int):
        cmd: str = 'h2400'
        # permitted values between 1-8
        if 1 <= position <= 8:
            cmd += str(position)
        return cmd

    def moveValveCounterclockwiseDirection(self, position: int):
        cmd: str = 'h2500'
        # permitted values between 1-8
        if 1 <= position <= 8:
            cmd += str(position)
        return cmd

    def moveValveInShortestDirection(self, position: int):
        cmd: str = 'h2600'
        # permitted values between 1-8
        if 1 <= position <= 8:
            cmd += str(position)
        return cmd

    def valveMovementHelper(self, cmdValue: int, incrementWith: int):
        cmd: str = 'h'
        # permitted values between 0-345 incremented by 15
        if 345 >= incrementWith >= 0 == incrementWith % 15:
            cmdValue += incrementWith
        cmd += str(cmdValue)
        return cmd

    def clockwiseAngularValveMove(self, position: int):
        return self.valveMovementHelper(27000, position)

    def counterclockwiseAngularValveMove(self, position: int):
        return self.valveMovementHelper(28000, position)

    def shortestDirectAngularValveMove(self, position: int):
        return self.valveMovementHelper(29000, position)

    """
        Query Commands
    """

    def commandBufferStatusQuery(self):
        return QueryCommandsEnumeration.BUFFER_STATUS.value

    def pumpStatusQuery(self):
        return QueryCommandsEnumeration.PUMP_STATUS.value

    def firmwareVersionQuery(self):
        return QueryCommandsEnumeration.FIRMWARE_VERSION.value

    def firmwareChecksumQuery(self):
        return QueryCommandsEnumeration.FIRMWARE_CHECKSUM.value

    def startVelocityQuery(self):
        return QueryCommandsEnumeration.START_VELOCITY.value

    def maximumVelocityQuery(self):
        return QueryCommandsEnumeration.MAXIMUM_VELOCITY.value

    def stopVelocityQuery(self):
        return QueryCommandsEnumeration.STOP_VELOCITY.value

    def actualPositionOfSyringeQuery(self):
        return QueryCommandsEnumeration.ACTUAL_SYRINGE_POSITION.value

    def numberOfReturnStepsQuery(self):
        return QueryCommandsEnumeration.NUMBER_OF_RETURN_STEPS.value

    def statusOfAuxiliaryInput1Query(self):
        return QueryCommandsEnumeration.STATUS_AUXILIARY_INPUT_1.value

    def statusOfAuxiliaryInput2Query(self):
        return QueryCommandsEnumeration.STATUS_AUXILIARY_INPUT_2.value

    def returns255Query(self):
        return QueryCommandsEnumeration.RETURNS_255.value

    def numberOfBackoffStepsQuery(self):
        return QueryCommandsEnumeration.NUMBER_OF_BACKOFF_STEPS.value

    def syringeStatusQuery(self):
        return QueryCommandsEnumeration.SYRINGE_STATUS.value

    def syringeModeQuery(self):
        return QueryCommandsEnumeration.SYRINGE_MODE.value

    def valveStatusQuery(self):
        return QueryCommandsEnumeration.VALVE_STATUS.value

    def valveTypeQuery(self):
        return QueryCommandsEnumeration.VALVE_TYPE.value

    def valveLogicalPositionQuery(self):
        return QueryCommandsEnumeration.VALVE_LOGICAL_POSITION.value

    def valveNumericalPositionQuery(self):
        return QueryCommandsEnumeration.VALVE_NUMERICAL_POSITION.value

    def valveAngleQuery(self):
        return QueryCommandsEnumeration.VALVE_ANGLE.value

    def lastDigitalOutValueQuery(self):
        return QueryCommandsEnumeration.LAST_DIGITAL_OUT_VALUE.value