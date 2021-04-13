#!/usr/bin/python

import threading
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import logging
import time
from colr import color

BUSRECOVERYTIME = 0.5

class ModbusConnection:     #Singleton
    __instance__ = None
    __connectionErrorCounter__ = None
    __connectionCounter__ = None
    __modbusConnection__ = None
    __modbusClient__ = None
    __mutex__ = threading.Lock()

    @staticmethod
    def instance():
        """ Static access method. """
        if ModbusConnection.__instance__ == None:
            with ModbusConnection.__mutex__:
                ModbusConnection()
        return ModbusConnection.__instance__

    def __init__(self):
        """ Virtually private constructor. """
        if ModbusConnection.__instance__ != None:
            raise Exception("[ModbusConnection] This class is a singleton! Instance already created")
        else:
            ModbusConnection.__instance__ = self

        self.__connectionErrorCounter__ = dict()
        self.__connectionCounter__ = dict()
        self.__modbusClient__ = ModbusClient(method = "rtu", port="/dev/ttyUSB0", stopbits = 1, bytesize = 8, parity = 'N', baudrate= 9600, timeout=0.2, retry_on_empty=True, retry_on_invalid=True)

    def __increaseModbusErrorCounter__(self, nodeId):
        try:
            self.__connectionErrorCounter__[nodeId] = self.__connectionErrorCounter__[nodeId] + 1
        except:
            self.__connectionErrorCounter__[nodeId] = 1
        
        logging.debug("[ModbusConnection] Node " + str(nodeId) + ": Communication error. Total errors: " + str(self.__connectionErrorCounter__[nodeId]))
        counter = self.__connectionErrorCounter__[nodeId]
        return counter

    def getModbusErrorCounter(self, nodeId):
        try:
            return self.__connectionErrorCounter__[nodeId]
        except:
            self.__connectionErrorCounter__[nodeId] = 0
            return 0

    def getModbusErrorRate(self, node):
        try:
            self.__connectionErrorCounter__[node]
        except:
            return 0

        try:
            return round(self.__connectionErrorCounter__[node] / self.__connectionCounter__[node], 2)
        except:
            logging.warning("[ModbusConnection] Node " + str(node) + ": Cannot calculate error rate.")
            return None

    def resetCounters(self, nodeId):
        with self.__mutex__:
            try:
                self.__connectionErrorCounter__[nodeId] = 0
                self.__connectionCounter__[nodeId] = 0
            except Exception as e:
                logging.error("[ModbusConnection] Node " + str(node) + ": Error resetting counters. " + str(e))

    def __connectSocket__(self):
        if self.__modbusClient__.socket == None:
            logging.debug("[ModbusConnection] Modbus not connected. Connecting...")
            try:
                self.__modbusConnection__ = self.__modbusClient__.connect()
                if(self.__modbusConnection__ != True):
                    logging.error("[ModbusConnection] Cannot connect modbus. Check modbus module.")
            except Exception as e:
                logging.error("[ModbusConnection] Unknown modbus connection error: " + str(e))
        return self.__modbusConnection__

    def checkmodbusconnection(self):
        return self.__modbusConnection__

    def writeregister(self, node, registerId, value):
        result = None
        with self.__mutex__:
            logging.debug("[ModbusConnection] Node " + str(node) + ": writing register " + str(registerId) +" with value "+ str(value))
            try:
                self.__connectionCounter__[node] += 1
            except:
                self.__connectionCounter__[node] = 1
            if self.__modbusClient__ != None:
                if(self.__connectSocket__()):
                    try:
                        result = self.__modbusClient__.write_register(registerId, value, unit = node)
                        if result.isError():
                            raise Exception(str(result))
                    except Exception as e:
                        logging.warning("[ModbusConnection] Modbus Write Error: " + str(e))
                        self.__increaseModbusErrorCounter__(node)
                        result = None
                else:
                    logging.warning("[ModbusConnection] Cannot write to node " + str(node) + ".")
        return result

    def readregisters(self, node, startAddress = 1000, registersToRead = 1):
        return self.__readregisters__(node, startAddress, registersToRead, "holding")

    def __readregisters__(self, node, startAddress, registersToRead, type="holding"):
        with self.__mutex__:
            logging.debug("[ModbusConnection] Node " + str(node) + ": Reading " + str(registersToRead) + " " + str(type) + "-registers starting with register "+ str(startAddress))
            try:
                self.__connectionCounter__[node] += 1
            except:
                self.__connectionCounter__[node] = 1
            
            if self.__modbusClient__ != None:
                if(self.__connectSocket__()):
                    registers = dict()
                    try:
                        if type == "input":
                            modbus_response = self.__modbusClient__.read_input_registers(startAddress, registersToRead, unit=node)
                        else:
                            modbus_response = self.__modbusClient__.read_holding_registers(startAddress, registersToRead, unit=node)
                        if modbus_response.isError():
                            raise Exception(str(modbus_response))

                        logging.debug("[ModbusConnection] Node " + str(node) + ": Data: " + str(modbus_response.registers))
                        for i in range(len(modbus_response.registers)):
                            registers[startAddress + i] = modbus_response.registers[i]

                        return registers

                    except Exception as e:
                        logging.debug("[ModbusConnection] Modbus read error at node " + str(node) + ": " + str(e))
                        self.__increaseModbusErrorCounter__(node)
                        time.sleep(BUSRECOVERYTIME)
                else:
                    logging.debug("[ModbusConnection] Cannot read from node " + str(node) + ". Modbus-Socket not connected.")
            return None

    def readinputregisters(self, node, startAddress = 1000, registersToRead = 1):
        return self.__readregisters__(node, startAddress, registersToRead, "input")


# Entry Point     
if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    unitToTest = 1

    # trying to use modbus module
    socket = ModbusConnection.instance().__connectSocket__()
    if(socket == True):
        print(color('SUCCESS: Using modbus module.', fore='green', style='bright'))
    else:
        print(color('ERROR: Using modbus module.', fore='red', style='bright'))
        input("PRESS ENTER TO CONTINUE TESTING")

    # trying to read temperature from modbus module internal sensor
    internalTempRegisterNumber = 1021
    register = ModbusConnection.instance().readregisters(unitToTest, internalTempRegisterNumber, 1)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register != None and register != {} and errors == 0 and errorrate == 0):
        print(color('SUCCESS: Valid register read of interface temperature.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid register read of interface temperature failed.', fore='red', style='bright'))

    try:
        if register == None:
            raise(Exception("Empty Register."))
        if(register[internalTempRegisterNumber] < 999 and register[internalTempRegisterNumber] > 0):
            print(color('SUCCESS: Read temperature value in valid range. Temperature: ' + str(register[internalTempRegisterNumber]/10), fore='green', style='bright'))
        else:
            print(color('ERROR: Read temperature value in valid range. OUT OF RANGE: ' + str(register[internalTempRegisterNumber]/10), fore='red', style='bright'))
    except Exception as e:
            print(color('ERROR: Read temperature value in valid range. No data found. ' + str(e), fore='red', style='bright'))

    # reading multiple registers
    ModbusConnection.instance().resetCounters(unitToTest)
    register = ModbusConnection.instance().readregisters(unitToTest, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register != None and register != {} and errors == 0 and errorrate == 0):
        print(color('SUCCESS: Valid multiple register read.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid multiple register read.', fore='red', style='bright'))

    # reading multiple registers again
    ModbusConnection.instance().resetCounters(unitToTest)
    register = ModbusConnection.instance().readregisters(unitToTest, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register != None and register != {} and errors == 0 and errorrate == 0):
        print(color('SUCCESS: Valid multiple register read twice.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid multiple register read twice.', fore='red', style='bright'))

    # reading an invalid node id
    register = ModbusConnection.instance().readregisters(99, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(99)
    if(register == None and errors == 1):
        print(color('SUCCESS: Invalid node read.', fore='green', style='bright'))
    else:
        print(color('ERROR: Invalid node read.', fore='red', style='bright'))

    # reading from broadcast address
    register = ModbusConnection.instance().readregisters(0, 1000, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(0)
    if(register == None and errors == 1):
        print(color('ERROR: Node 0 (Broadcast) read.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: Node 0 (Broadcast) read.', fore='green', style='bright'))

    # reading of multiple invalid registers
    ModbusConnection.instance().resetCounters(unitToTest)
    register = ModbusConnection.instance().readregisters(unitToTest, 4130, 24)
    errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
    errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
    if(register == None and errors == 1 and errorrate == 1):
        print(color('SUCCESS: Multiple invalid register read.', fore='green', style='bright'))
    else:
        print(color('ERROR: Multiple invalid register read.', fore='red', style='bright'))

    # reading multiple registers multiple times
    ModbusConnection.instance().resetCounters(unitToTest)
    temp = 0
    for i in range(0, 50):
        register = ModbusConnection.instance().readregisters(unitToTest, 1000, 24)
        errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
        errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
        temp = ModbusConnection.instance().__connectionCounter__[unitToTest]
        time.sleep(0.3)
    if(register != None and register != {} and errors == 0 and errorrate == 0 and temp == 50):
        print(color('SUCCESS: Valid multiple register read multiple times.', fore='green', style='bright'))
    else:
        print(color('ERROR: Valid multiple register read multiple times.', fore='red', style='bright'))

    # writing to vaild node
    ModbusConnection.instance().resetCounters(unitToTest)
    register = 1023
    value = 1514
    try:
        result = ModbusConnection.instance().writeregister(unitToTest, register, value)
        errors = ModbusConnection.instance().getModbusErrorCounter(unitToTest)
        errorrate =  ModbusConnection.instance().getModbusErrorRate(unitToTest)
        if(result != None and result.value == value and errors == 0 and errorrate == 0):
            print(color('SUCCESS: write register to vaild node.', fore='green', style='bright'))
        else:
            print(color('ERROR: write register to vaild node. Invalid value', fore='red', style='bright'))
    except Exception as e:
        print(color('ERROR: write register to vaild node. ' + str(e), fore='red', style='bright'))

    # writing to invaild node
    node = 99
    register = 1023
    value = 1514
    ModbusConnection.instance().resetCounters(node)
    try:
        result = ModbusConnection.instance().writeregister(node, register, value)
        errors = ModbusConnection.instance().getModbusErrorCounter(node)
        errorrate =  ModbusConnection.instance().getModbusErrorRate(node)
        if(result == None and errors == 1 and errorrate == 1):
            print(color('SUCCESS: write register to invaild node.', fore='green', style='bright'))
        else:
            print(color('ERROR: write register to invaild node.', fore='red', style='bright'))
    except Exception as e:
        print(color('ERROR: write register to invaild node. ' + str(e), fore='red', style='bright'))