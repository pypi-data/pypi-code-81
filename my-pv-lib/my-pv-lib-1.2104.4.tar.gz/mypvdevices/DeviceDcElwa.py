#!/usr/bin/python

from colr import color
from datetime import datetime, timedelta
import logging
import time
import json
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusRtuDevice import ModbusRtuDevice
from mypvdevices.ModbusConnection import ModbusConnection

MODBUSWARNLEVEL = 0.5
REGISTERTIMEOUT = 30
BUILDNR = "4321"

class DeviceDcElwa(ModbusRtuDevice):
    __devicetype__ = "ELWA"
    __irerror__ = False
    __errorcode__ = 0

    def __init__(self, serial, nodeid):
        ModbusRtuDevice.__init__(self, serial, nodeid)
        self.__startRegister__ = 1000
        self.__registersToRead__ = 24

    def __createsetup__(self):
        return {
            "device": self.__devicetype__, \
            "fwversion": self.__firmwareversion__, \
            "serialno": self.__serial__, \
            "elno": self.__nodeId__, \
            "ww2target": None, \
            "ww2offset": 1514
            }

    def __getsettingsmap__(self):
        settings = {
            "ww2target": {
                "register": 1022,   #ELWA Modbus Interface boost temperature
                "forced": False
            },
            "ww2offset": {
                "register": 1023,   #Temp sensor offset calibration
                "forced": True
            }
        }
        return settings

    def getdata(self):

        acRelayState = self.getdataset("ac_relay_state")
        dcPower = self.getdataset("dc_power")
        operationMode = self.getdataset("operation_mode")

        if operationMode == 3 or operationMode == 5 or operationMode == 6 or operationMode == 7 or operationMode == 8 or operationMode == 9 or operationMode == 10 or operationMode == 11 or operationMode == 12 or operationMode == 13 or operationMode == 14 or operationMode == 15 or operationMode == 16 or operationMode == 20 or operationMode == 21 or operationMode == 135:
            acHeating = True
        else:
            acHeating = False

        if acRelayState != None:
            if acHeating == True and acRelayState == 1:
                boostpower = 750
            else:
                boostpower = 0
        else:
            boostpower = None

        if(boostpower != None):
            power = (int(dcPower) + int(boostpower))
            meter = -boostpower
        else:
            power = dcPower
            meter = None

        if self.__errorcode__ != 0:
            errorcode = self.__errorcode__
        else:
            errorcode = None

        errorrate = self.getcommunicationerrorsrate()

        data={
            "device": self.__devicetype__,
            "fwversion": self.__firmwareversion__,
            "loctime": time.strftime("%H:%M:%S"),
            "dev_id": self.__nodeId__,
            "day_counter" : self.getdataset("day_counter"),
            "op_mode": operationMode,
            "dc_breaker": self.getdataset("dc_breaker_state"),
            "dc_relay": self.getdataset("dc_relay_state"),
            "ac_relay": acRelayState,
            "temp1": self.getdataset("temp1"),
            "temp_day_min": self.getdataset("temp_day_min"),
            "temp_day_max": self.getdataset("temp_day_max"),
            "ww1target": self.getdataset("dc_temp_target"),
            "ac_temp_target": self.getdataset("ac_temp_target"),
            "tempchip": self.getdataset("tempchip"),
            "iso_voltage": self.getdataset("iso_voltage"),
            "dc_voltage": self.getdataset("dc_voltage"),
            "dc_current": self.getdataset("dc_current"),
            "power_elwa": power,
            "boostpower_elwa": boostpower,
            "dc_day_wh": self.getdataset("dc_day_wh"),
            "dc_total_kwh": self.getdataset("dc_total_kwh"),
            "ac_day_wh": self.getdataset("ac_day_wh"),
            "minutes_from_noon": self.getdataset("minutes_from_noon"),
            "minutes_since_dusk": self.getdataset("minutes_since_dusk"),
            "ac_boost_mode": self.getdataset("ac_boost_mode"),
            "m1sum": dcPower,
            "m0sum": meter,
            "temp2": self.getdataset("temp2"),
            "ww2target": self.getdataset("boost_temp_target"),
            "ww2offset": self.getdataset("ww2offset_calibration"),
            "modbuserrorrate":  errorrate,
            "errorcode": errorcode
        }       
        return data

    def getdataset(self, datasetname):
        if self.__irerror__ == False or datasetname in ("temp2"):
            return ModbusRtuDevice.getdataset(self, datasetname)
        else:
            return None

    def getlogdata(self, time = None):
        acRelayState = self.getlogvalue("ac_relay_state")
        if acRelayState != None:
            boostpower = int(round(acRelayState*750))
        else:
            boostpower = None
        
        dcPower = self.getintlogvalue("dc_power")
        if dcPower != None:
            if(boostpower != None):
                power = int(dcPower + boostpower)
            else:
                power = dcPower
        else:
            power = None
        if(boostpower != None):
            metercons = -boostpower
        else:
            metercons = None

        pvprod = dcPower

        sLog={
			"modbus_error_rate" : self.getcommunicationerrorsrate(),
			"day_counter" : self.getintlogvalue("day_counter"),
			"op_mode": self.getintlogvalue("operation_mode"),
			"dc_breaker": self.getintlogvalue("dc_breaker_state"),
			"dc_relay": self.getintlogvalue("dc_relay_state"),
			"ac_relay": self.getintlogvalue("ac_relay_state"),
			"temp": self.getintlogvalue("temp1"),
			"temp_day_min": self.getintlogvalue("temp_day_min"),
			"temp_day_max": self.getintlogvalue("temp_day_max"),
			"dc_temp_target": self.getintlogvalue("dc_temp_target"),
			"ac_temp_target": self.getintlogvalue("ac_temp_target"),
			"temp_internal": self.getintlogvalue("tempchip"),
			"iso_voltage": self.getintlogvalue("iso_voltage"),
			"dc_voltage": self.getintlogvalue("dc_voltage"),
			"dc_current": self.getintlogvalue("dc_current"),
			"dc_power": self.getintlogvalue("dc_power"),
			"dc_day_wh": self.getintlogvalue("dc_day_wh"),
			"dc_total_kwh": self.getintlogvalue("dc_total_kwh"),
			"ac_day_wh": self.getintlogvalue("ac_day_wh"),
			"minutes_from_noon": self.getintlogvalue("minutes_from_noon"),
			"minutes_since_dusk": self.getintlogvalue("minutes_since_dusk"),
			"ac_boost_mode": self.getintlogvalue("ac_boost_mode"),
			"temp2": self.getintlogvalue("temp2"),
			"ww2target": self.getintlogvalue("boost_temp_target"),
			"ww2offset": self.getintlogvalue("ww2offset_calibration"),
        }

        logData = {
            "time": time,
            "i_power": power,
            "i_boostpower": boostpower,
            "i_m1sum": pvprod,
            "i_metercons": metercons,
            "i_temp1": self.getintlogvalue("temp1"),
            "i_temp2": self.getintlogvalue("temp2"),
            "s_json" : json.dumps(sLog)
        }

        ModbusConnection.instance().resetCounters(self.__nodeId__)
        # self.__logdata__.clear()  #todo sicher?
        return logData

    def getintlogvalue(self, datasetname):
        if self.__irerror__ == False or datasetname in ("temp2"):
            return ModbusRtuDevice.getintlogvalue(self, datasetname)
        else:
            return None

    def getlogvalue(self, datasetname):
        if self.__irerror__ == False or datasetname in ("temp2"):
            return ModbusRtuDevice.getlogvalue(self, datasetname)
        else:
            return None

    def __checkRegiterTimeStamp__(self):
        if self.__registerLastSuccessfullReadTimeStamp__ != None and len(self.__registers__) > 0:
            difference = time.time() - self.__registerLastSuccessfullReadTimeStamp__
            if(difference > REGISTERTIMEOUT):
                return False    
        return True
    
    def __supervise__(self):

        ModbusRtuDevice.__supervise__(self)
        
        value = ModbusRtuDevice.getdataset(self,"temp1")
        if value != None and ( value > 1200 or value < 0 ):
            logging.warning("[DeviceDcElwa] " + self.getidentifier() + " - Temp1 sensor error: " + str(value))
            temp1error = True
        else:
            temp1error = False

        value = ModbusRtuDevice.getdataset(self,"temp2")
        if value != None and ( value > 1200 or value < 0 ):
            logging.warning("[DeviceDcElwa] " + self.getidentifier() + " - Temp2 sensor error: " + str(value))
            temp2error = True
        else:
            temp2error = False

        value = ModbusRtuDevice.getdataset(self,"operation_mode")
        if value != None and value > 100 :
            logging.warning("[DeviceDcElwa] " + self.getidentifier() + " - Operation Mode " + str(value) + " detected.")
            opmodeError = True
        else:
            opmodeError = False

        if ModbusConnection.instance().checkmodbusconnection():
            modbusError = False
        else:
            logging.debug("[DeviceDcElwa] " + self.getidentifier() + " - Modbus module not present.")
            ModbusConnection.instance().resetCounters(self.__nodeId__)
            modbusError = True

        modbusErrorRate = self.getcommunicationerrorsrate()
        
        if modbusError == False:
            if modbusErrorRate != None and modbusErrorRate >= 0.70:
                logging.warning("[DeviceDcElwa] " + self.getidentifier() + " - Modbus communication to device not working.")
                modbusError = True
            else:                    
                modbusError = False

        registerisvalid = self.__checkRegiterTimeStamp__()
        if registerisvalid != True and modbusError == False:
            logging.warning("[DeviceDcElwa] " + self.getidentifier() + " - Register values too old. Communication errors expected. Registers: " + str(self.__registers__) + " Timestamp: " + str(self.__registerLastSuccessfullReadTimeStamp__) + " Age: " + str(time.time() - self.__registerLastSuccessfullReadTimeStamp__))
            registerError = True
        else:
            registerError = False

        if registerError == False and modbusError == False and modbusErrorRate != None and modbusErrorRate > MODBUSWARNLEVEL and modbusErrorRate < 0.7:
            logging.warning("[DeviceDcElwa] " + self.getidentifier() + " - Modbus error rate to hight " + str(modbusErrorRate) + ".")
            modbusWarning = True
        else:
            modbusWarning = False

        value = ModbusRtuDevice.getdataset(self, "tempchip")
        if value == 0 and modbusError == False and registerError == False:
            logging.warning("[DeviceDcElwa] " + self.getidentifier() + " - No IR Connection to Device.")
            irError = True
            self.__irerror__ = True
        else:
            irError = False
            self.__irerror__ = False

        healthState = 0

        #healthState warnings
        if temp2error == True or irError == True or opmodeError == True or modbusWarning == True:
            healthState = 1

        #healthState errors
        if temp1error == True or modbusError == True or registerError == True:
            healthState = 2

        self.__seterrorcode__(irerror=irError, modbuserror=modbusError, registererror=registerError, temp1error=temp1error, temp2error=temp2error, opmodeerror=opmodeError, modbuswarning=modbusWarning)

        if modbusErrorRate != None or healthState == 2:
            self.__sethealthstate__(healthState)

    def __seterrorcode__(self, modbuserror=0, irerror=0, registererror=0, temp1error=0, temp2error=0, opmodeerror=0, modbuswarning=0):
        if modbuswarning: 
            self.__setBit__(0)
        else:
            self.__resetBit__(0)

        if modbuserror:
            self.__setBit__(1)
        else:
            self.__resetBit__(1)

        if irerror:
            self.__setBit__(2)
        else:
            self.__resetBit__(2)

        if registererror:
            self.__setBit__(3)
        else:
            self.__resetBit__(3)

        if temp1error:
            self.__setBit__(4)
        else:
            self.__resetBit__(4)

        if temp2error:
            self.__setBit__(5)
        else:
            self.__resetBit__(5)

        if opmodeerror:
            self.__setBit__(6)
        else:
            self.__resetBit__(6)

    def __setBit__(self, offset):
        mask = 1 << offset
        self.__errorcode__ = (self.__errorcode__ | mask)

    def __resetBit__(self, offset):
        mask = ~(1 << offset)
        self.__errorcode__ = (self.__errorcode__ & mask)

    def __getregistermapping__(self):
        datasets = {}
        datasets["day_counter"] = self.__createDataset__(1000, "avg")
        datasets["operation_mode"] = self.__createDataset__(1001, "avg")
        datasets["dc_breaker_state"] = self.__createDataset__(1002, "avg")
        datasets["dc_relay_state"] = self.__createDataset__(1003, "sum")
        datasets["ac_relay_state"] = self.__createDataset__(1004, "sum")
        datasets["temp1"] = self.__createDataset__(1005, "avg")
        datasets["temp_day_min"] = self.__createDataset__(1006, "avg")
        datasets["temp_day_max"] = self.__createDataset__(1007, "avg")
        datasets["dc_temp_target"] = self.__createDataset__(1008, "avg")
        datasets["ac_temp_target"] = self.__createDataset__(1009, "avg")
        datasets["tempchip"] = self.__createDataset__(1010, "avg")
        datasets["iso_voltage"] = self.__createDataset__(1011, "avg")
        datasets["dc_voltage"] = self.__createDataset__(1012, "avg")
        datasets["dc_current"] = self.__createDataset__(1013, "avg")
        datasets["dc_power"] = self.__createDataset__(1014, "sum")
        datasets["dc_day_wh"] = self.__createDataset__(1015, "avg")
        datasets["dc_total_kwh"] = self.__createDataset__(1016, "avg")
        datasets["ac_day_wh"] = self.__createDataset__(1017, "avg")
        datasets["minutes_from_noon"] = self.__createDataset__(1018, "avg")
        datasets["minutes_since_dusk"] = self.__createDataset__(1019, "avg")
        datasets["ac_boost_mode"] = self.__createDataset__(1020, "avg")
        datasets["temp2"] = self.__createDataset__(1021, "avg")
        datasets["boost_temp_target"] = self.__createDataset__(1022, "avg")
        datasets["ww2offset_calibration"] = self.__createDataset__(1023, "avg")
        return datasets

# Entry Point     
if __name__ == "__main__":

    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    serial = "120100200505tes1"
    cryptoKey = "41424142414241424142414241424142"
    serial2 = "120100200505tes2"
    cryptoKey2 = "41424142414241424142414241424142"
    serial3 = "120100200505tes3"
    cryptoKey3 = "41424142414241424142414241424142"
    server = "my-pv.live"

    # try to read from valid device
    device = DeviceDcElwa(serial, 1)
    try:
        device.__readallregisters__()
        if(len(device.__registers__) == 24):
            print(color('SUCCESS: reading registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid length")
    except Exception as e:
        print(color('ERROR: reading registers. ' + str(e), fore='red', style='bright'))

    try:
        if device.__syncsettings__():
            print(color('SUCCESS: syncing settings.', fore='green', style='bright'))
        else:
            raise Exception("settings sync failed")
    except Exception as e:
        print(color('ERROR: syncing settings. ' + str(e), fore='red', style='bright'))

    try:
        device.__processregisters__()
        value = device.getdataset("dc_power")
        if( value != None ):
            print(color('SUCCESS: processing registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: processing registers. ' + str(e), fore='red', style='bright'))

    try:
        value = device.getdataset("seppi")
        if( value == None ):
            print(color('SUCCESS: getting value of unkown registers.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: getting value of unkown registers. ' + str(e), fore='red', style='bright'))

    time.sleep(2)
    device.__processregisters__()
    time.sleep(2)

    device.__readallregisters__()
    try:
        device.__processregisters__()
        value = device.getlogvalue("dc_power")
        if( value != None ):
            print(color('SUCCESS: processing registers again.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: processing registers again. ' + str(e), fore='red', style='bright'))

    
    data = device.getdata()
    if(data != None and data != {}):
        print(color('SUCCESS: getting getdata.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting getdata.', fore='red', style='bright'))

    logData = device.getlogdata()
    if(logData != None and logData != {}):
        print(color('SUCCESS: getting getLogData.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting getLogData.', fore='red', style='bright'))

    key = "ww2target"
    targetValue = 534
    try:
        device.setsetupvalue(key, targetValue)
        print(color('SUCCESS: sending setup value to device.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: sending setup value to device.', fore='red', style='bright'))

    setup = device.getsetup()
    if(setup[key] == targetValue):
        print(color('SUCCESS: Setting setup value.', fore='green', style='bright'))
    else:
        print(color('ERROR: Setting setup value.', fore='red', style='bright'))

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
    try:
        device.__supervise__()
        print(color('SUCCESS: supervising.', fore='green', style='bright'))
    except Exception as e:
            print(color('ERROR: supervising. Error: ' + str(e), fore='red', style='bright'))

    input("Press ENTER to start running tests")
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceDcElwa(serial, 1)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addconnection(connection)
    device.start()

    try:
        while True:
            print(color('[DeviceDcElwa] test active. Press CTRL+C to stop', fore='blue', style='bright'))
            # device.showinfo()
            # device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DeviceDcElwa] Stopping Test...")
        device.stop()

    input("Press ENTER to start communication tests")

    #DCS communication tests
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceDcElwa(serial, 1)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addconnection(connection)
    # device.setLogDataSendInterval(5)

    device2 = DeviceDcElwa(serial2, 2)
    connection2 = DcsConnection(serial2, cryptoKey2, server, 50333)
    device2.addconnection(connection2)

    device3 = DeviceDcElwa(serial3, 7)
    connection3 = DcsConnection(serial3, cryptoKey3, server, 50333)
    device3.addconnection(connection3)

    device.start()
    device2.start()
    device3.start()
    try:
        while True:
            print(color('[DeviceDcElwa] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            # device.showInfo()
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            device2.showcommunicationerrors()
            device2.showcommunicationerrorsrate()
            device3.showcommunicationerrors()
            device3.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
        device2.stop()
        device3.stop()
    input("waiting...")
