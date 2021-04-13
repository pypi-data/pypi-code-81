#!/usr/bin/python

import logging
import time
from datetime import datetime
from colr import color
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusConnection import ModbusConnection
from mypvdevices.ModbusDevice import ModbusDevice

class ModbusRtuDevice(ModbusDevice):
    __devicetype__ = "ModbusRtuDevice"
    __nodeId__ = None

    def __init__(self, serial, nodeid):
        if nodeid != None and isinstance(nodeid, int):
            self.__nodeId__ = nodeid
        else:
            errmsg = "Instance not created. nodeid is invalid. nodeid=" + str(nodeid)
            logging.error(errmsg)
            raise TypeError(errmsg)

        ModbusDevice.__init__(self, serial)

    def getidentifier(self):
        return ModbusDevice.getidentifier(self) + ", Node: " + str(self.__nodeId__)
    
    def __readregister__(self, registerId):
        with self.__lock__:
            try:
                registers = ModbusConnection.instance().readregisters(self.__nodeId__, registerId, 1)
                if registers != None:
                    return registers[registerId]
                else:
                    raise Exception("Modbus communication failed.")
            except Exception as e:
                raise Exception("Register " + str(registerId) + " cannot be read. " + str(e))

    def __readregisters__(self, startregisteraddress, registerstoread):
        with self.__lock__:
            if self.__nodeId__ != None:
                return ModbusConnection.instance().readregisters(self.__nodeId__, startregisteraddress, registerstoread)

    def __writeregister__(self, registerId, valueToWrite):
        with self.__lock__:
            logging.debug("[ModbusRtuDevice] ID " + str(self.__serial__) + " writing register " + str(registerId) + " value: " + str(valueToWrite))
            if self.__nodeId__ != None:
                ModbusConnection.instance().writeregister(self.__nodeId__, registerId, valueToWrite)
            else:
                print("Register " + str(registerId) + " changed to " + str(valueToWrite))

    def getcommunicationerrorscounter(self):
        return ModbusConnection.instance().getModbusErrorCounter(self.__nodeId__)

    def getcommunicationerrorsrate(self):
        return ModbusConnection.instance().getModbusErrorRate(self.__nodeId__)

    def getdata(self):
        t = datetime.now()
        data = {
                "fwversion": self.__firmwareversion__,
				"power": t.second * 100,
                "temp1": t.minute,
                "check": 9811,
                "temp2": self.getdataset("temp2"),
				"loctime": time.strftime("%H:%M:%S")
                }            
        return data

# Entry Point     
if __name__ == "__main__":

    from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    #device connection tests
    serial = "120100200505tes1"
    cryptoKey = "41424142414241424142414241424142"
    server = "my-pv.live"

    #AUTO-Tests
    #Constructor Tests
    try:
        device = ModbusRtuDevice("123456789")
        print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))
        device = None

    try:
        device = ModbusRtuDevice(None)
        print(color('ERROR: serial is None.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial is None.', fore='green', style='bright'))

    try:
        device = ModbusRtuDevice(serial, 1)
        print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
    except:
        print(color('ERROR: creating valid device.', fore='red', style='bright'))

    identifier = device.getidentifier()
    if identifier == serial + ", Node: 1":
        print(color('SUCCESS: checking identifier.', fore='green', style='bright'))
    else:
        print(color('ERROR: checking identifier.', fore='red', style='bright'))

    try:
        setup = device.getsetup()
        if(setup == None):
            raise Exception("Setup is None")
        print(color('SUCCESS: getting device Setup.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: getting device Setup. Message: ' + str(e), fore='red', style='bright'))

    try:
        data = device.getdata()
        if(data == None):
            raise Exception("Data is None")
        print(color('SUCCESS: getting device data.', fore='green', style='bright'))
    except:
        print(color('ERROR: getting device data.', fore='red', style='bright'))

    try:
        logData = device.getlogdata()
        if(logData == None):
            raise Exception("logData is None")
        print(color('SUCCESS: getting device logData.', fore='green', style='bright'))
    except:
        print(color('ERROR: getting device logData.', fore='red', style='bright'))

    try:
        temp = device.getserial()
        if(temp == serial):
            print(color('SUCCESS: getting device Serial.', fore='green', style='bright'))
        else:
            raise Exception("Serial doesn't match serial used to create.")
    except:
        print(color('ERROR: getting device Serial.', fore='red', style='bright'))

    try:
        device.stop()
        print(color('SUCCESS: stopping device before start.', fore='green', style='bright'))
    except:
        print(color('ERROR: stopping device before start.', fore='red', style='bright'))

    try:
        temp = device.getstate()
        if(temp == False):
            print(color('SUCCESS: getting device state (before start).', fore='green', style='bright'))
        else:
            raise Exception("device state is not stopped.")
    except:
        print(color('ERROR: getting device state (before start).', fore='red', style='bright'))

    try:
        temp = device.getdevicetype()
        if(temp == "ModbusRtuDevice"):
            print(color('SUCCESS: getting device type.', fore='green', style='bright'))
        else:
            raise Exception("device type does not match.")
    except:
        print(color('ERROR: getting device type.', fore='red', style='bright'))
 
    #Modbus tests
    device = ModbusRtuDevice(serial, 1)
    try:
        device.__readallregisters__()
        print(color('SUCCESS: reading registers.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: reading registers. ' + str(e), fore='red', style='bright'))

    #register change 
    device.__registers__[1022] = 33
    device.__registers__[1023] = 1234
    try:
        device.__syncsettings__()
        if not device.__setup__["ww2target"] == 33:
            raise Exception("ww2target missmatch")
        if not device.__setup__["ww2offset"] == 1514:
            raise Exception("ww2offset missmatch")
        # if not device.__registers__[1023] == 1514:
        #     raise Exception("register 1023 missmatch")
        print(color('SUCCESS: syncing settings.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: syncing settings. ' + str(e), fore='red', style='bright'))
    
    device.__readallregisters__()

    if(device.getregistervalue(50) == None ):
        print(color('SUCCESS: reading unknown register.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading unknown register.', fore='red', style='bright'))
    
    register = device.getregistervalue(1021)
    if(register != None and register["value"] > 0 and register["value"] < 500):
        print(color('SUCCESS: reading valid register.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading valid register.', fore='red', style='bright'))

    if(device.getdataset("power") == None ):
        print(color('SUCCESS: getting dataset (power) before processing registers.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (power) before processing registers.', fore='red', style='bright'))

    if(device.getlogvalue("power") == None ):
        print(color('SUCCESS: getting logvalue (power) before processing registers.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) before processing registers.', fore='red', style='bright'))

    if(device.getlogvalue("test") == None ):
        print(color('SUCCESS: getting logvalue (test) before processing registers.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) before processing registers.', fore='red', style='bright'))

    device.__processregisters__()

    power = device.getdataset("power")
    if(power != None and power >= 0 ):
        print(color('SUCCESS: getting dataset (power).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (power).', fore='red', style='bright'))

    if(device.getdataset("abc") == None ):
        print(color('SUCCESS: getting dataset (abc).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (abc).', fore='red', style='bright'))

    if(device.getdataset(None) == None ):
        print(color('SUCCESS: getting dataset (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting dataset (None).', fore='red', style='bright'))

    if(device.getlogvalue(None) == None ):
        print(color('SUCCESS: getting logvalue (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (None).', fore='red', style='bright'))

    if(device.getlogvalue("abc") == None ):
        print(color('SUCCESS: getting logvalue (abc).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (abc).', fore='red', style='bright'))

    if( device.getlogvalue("power") == 0 ):
        print(color('SUCCESS: getting logvalue (power).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power).', fore='red', style='bright'))

    time.sleep(1)
    device.__readallregisters__()
    device.__registers__[1013] = 700
    device.__processregisters__()
    power = device.getlogvalue("power")
    if( power != None and power > 0 ):
        print(color('SUCCESS: getting logvalue (power) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after wait.', fore='red', style='bright'))

    if( device.getlogvalue("test") == 0 ):
        print(color('SUCCESS: getting logvalue (test) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after wait.', fore='red', style='bright'))

    if( device.getlogvalue("abc") == None ):
        print(color('SUCCESS: getting logvalue (abc) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (abc) after wait.', fore='red', style='bright'))

    device.clearlog()
    if( device.getlogvalue("abc") == None ):
        print(color('SUCCESS: getting logvalue (abc) after clear.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (abc) after clear.', fore='red', style='bright'))

    if( device.getlogvalue("test") == None ):
        print(color('SUCCESS: getting logvalue (test) after clear.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after clear.', fore='red', style='bright'))

    if( device.getlogvalue("power") == None ):
        print(color('SUCCESS: getting logvalue (power) after clear.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after clear.', fore='red', style='bright'))

    device = ModbusRtuDevice(serial, 1)
    device.setmodbusfrequency(0)
    device.start()
    time.sleep(5)

    if( device.getlogvalue("power") == None ):
        print(color('SUCCESS: getting logvalue (power) after starting device with frequency 0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after starting device with frequency 0.', fore='red', style='bright'))
    
    if( device.getlogvalue("test") == None ):
        print(color('SUCCESS: getting logvalue (test) after starting device with frequency = 0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after starting device with frequency = 0.', fore='red', style='bright'))

    device.setmodbusfrequency(1)
    time.sleep(3)
    device.stop()

    try:
        device.__sethealthstate__(0)
        print(color('SUCCESS: setting healthState to 0.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: setting healthState to 0.', fore='red', style='bright'))

    try:
        device.__sethealthstate__("seppi")
        print(color('ERROR: setting healthState to invalid.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: setting healthState to invalid.', fore='green', style='bright'))

    try:
        device.__sethealthstate__(None)
        print(color('ERROR: setting healthState to None.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: setting healthState to None.', fore='green', style='bright'))

    try:
        device.__sethealthstate__(3)
        print(color('SUCCESS: setting healthState to 3.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: setting healthState to 3.', fore='red', style='bright'))

    if(device != None):
        try:
            register = device.readregister(1021)
            if register > 0 and register < 900: 
                print(color('SUCCESS: reading register.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading register. Value missmatch: ' + str(register), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading register. Error: ' + str(e), fore='red', style='bright'))

    if(device != None):
        try:
            registers = device.readregisters(1000, 10)
            if registers[1000] !=  0 and registers[1001] != 0:
                print(color('SUCCESS: reading registers.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading registers. Value missmatch: ' + str(registers), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading registers. Error: ' + str(e), fore='red', style='bright'))

    # device = ModbusRtuDevice(serial, 1)
    # result = device.writeregister(123,22)    #Todo

    #DCS communication tests
    device = ModbusRtuDevice(serial, 1)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addconnection(connection)
    # device.setLogDataSendInterval(5)
    device.start()
    try:
        while True:
            print(color('[ModbusRtuDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            device.showinfo()
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
