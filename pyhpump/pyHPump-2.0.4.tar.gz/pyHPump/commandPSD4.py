from .command import *


class CommandPSD4(Command):
    def __init__(self, type):
        super().__init__(type)
        self.resolution_mode = 0

    def setSyringeMode(self, mode: int):
        cmd = super().setSyringeMode(mode)
        if mode == 0 or mode == 1:
            self.resolution_mode = mode
        return cmd

    def absolutePosition(self, value: int):
        # absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        bResult = False
        cmd: str = 'A'

        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Wrong parameter value PSD4 for absolute position command!")
            cmd = 'cmdError'
        return cmd

    def absolutePositionWithReadyStatus(self, value: int):
        # absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'a'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Wrong parameter value PSD4 for absolute position with ready status command!")
            cmd = 'cmdError'
        return cmd

    def relativePickup(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'P'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Wrong parameter value for relative pickup command!")
            cmd = 'cmdError'
        return cmd

    def relativePickupWithReadyStatus(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'p'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Wrong parameter value for relative pickup with ready status command!")
            cmd = 'cmdError'
        return cmd

    def relativeDispense(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'D'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Wrong parameter value for relative dispense command!")
            cmd = 'cmdError'
        return cmd

    def relativeDispenseWithReadyStatus(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'd'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Wrong parameter value for relative dispense with ready status command!")
            cmd = 'cmdError'
        return cmd

    def returnSteps(self, value: int):
        # Return Steps x where 0 ≤ x ≤ 100 in standard mode or 0 ≤ x ≤ 800 in high resolution mode
        cmd: str = 'K'
        if self.checkValueInInterval(self, value, 100, 800):
            cmd += str(value)
        else:
            print("Wrong parameter value for return steps command!")
            cmd = 'cmdError'
        return cmd

    def backoffSteps(self, value: int):
        # Back-off Steps x where 0 ≤ x ≤ 200 in standard mode and 0≤ x ≤ 1,600
        cmd: str = 'k'
        if self.checkValueInInterval(self, value, 200, 1600):
            cmd += str(value)
        else:
            print("Wrong parameter value for backoff steps command!")
            cmd = 'cmdError'
        return cmd

    """
        Motor Commands
    """
    def standardHighResolutionSelection(self, mode: int):
        # x=0 for standard resolution mode
        # x=1 for high resolution mode
        cmd: str = 'N'
        if mode == 0 or mode == 1:
            cmd += str(mode)
            self.resolution_mode = mode
            print("Resolution mode set on: " + str(mode) + " using PSD4 st/hg resolution selection")
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for standard/high resolution selection command!")
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

    def checkValueInInterval(self, value: int, valueST: int, valueHG: int):
        bVal: bool = False
        # if standard mode
        if self.resolution_mode == 0 and 0 <= value <= valueST:
            bVal = True
        elif self.resolution_mode == 1 and 0 <= value <= valueHG:
            bVal = True
        else:
            print("Error - value out of range !!!")
        return bVal

    def syringeHomeSensorStatusQuery(self):
        return QueryCommandsEnumeration.SYRINGE_HOME_SENSOR_STATUS.value