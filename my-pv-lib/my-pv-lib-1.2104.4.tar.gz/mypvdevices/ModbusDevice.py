#!/usr/bin/python

import logging
import threading
import time
from datetime import datetime
# import statistics
from colr import color
import sys
import os
import random

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.DcsConnection import DcsConnection

BUILDNR = "1.2104.4"

JOINTIMEOUT = 5
SERIALLEN = 16
DEVICESLEEPTIME = 10
DEFAULTMODBUSFREQUENCY = 15

class ModbusDevice:
    __firmwareversion__ = "2." + str(BUILDNR)
    __devicetype__ = "Dummy-Device"
    __lock__ = None
    __running__ = False
    __serial__ = None
    __monitorthread__ = None
    __modbusThread__ = None
    __datasets__ = None
    __data__ = None
    __logdata__ = None
    __logdataTimeStamp__ = None
    __logdataCounter__ = None
    __logdataLastValue__ = None
    __logdataSum__ = None
    __connections__ = None
    __setup__ = None
    __healthState__ = 0
    __registers__ = None
    __registerTimeStamp__ = None
    __settingsMap__ = None
    __startRegister__ = 1000
    __registersToRead__ = 24
    __lastlogdataSendTime__ = None
    __logdatasendinterval__ = 0
    __registerLastSuccessfullReadTimeStamp__ = None
    __modBusExecuted__ = None
    __modbusFrequency__ = DEFAULTMODBUSFREQUENCY

    def __init__(self, serial):
        if serial != None and len(serial) == SERIALLEN:
            self.__serial__ = serial
        else:
            errmsg = "Instance not created. Serial is invalid. Serial=" + str(serial)
            logging.error(errmsg)
            raise ValueError(errmsg)
            
        self.__lock__ = threading.Lock()
        self.__connections__ = list()
        self.__registers__ = dict()
        self.__data__ = dict()
        self.__logdata__ = dict()
        self.__logdataCounter__ = dict()
        self.__logdataLastValue__ = dict()
        self.__logdataSum__ = dict()
        self.__datasets__ = self.__getregistermapping__()
        self.__setup__ = self.__createsetup__()
        self.__settingsMap__ = self.__getsettingsmap__()
        logging.debug("new "+str(self.__devicetype__)+" created. Serial: " + str(self.__serial__))

    def addconnection(self, connection):
        # if connection != None and type(connection) is DcsConnection:
        if connection != None:
            if(connection.addDevice(self)):
                self.__connections__.append(connection)
                logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " Added connection to device")
            else:
                logging.error("[ModbusDevice] ID " + str(self.__serial__) + " Failed adding connection to device")
                raise Exception("cannot add connection")
        else:
            raise TypeError("invalid connection")

    def start(self):
        self.__running__ = True
        logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " starting...")
        self.__monitorthread__ = threading.Thread(target=self.__run__, name="Monitor " + str(self.__serial__))
        self.__monitorthread__.start()
        self.__modbusThread__ = threading.Thread(target=self.__runmodbus__, name="Modbus " + str(self.__serial__))
        self.__modbusThread__.start()
        time.sleep(0.1)
        for connection in self.__connections__:
            connection.connect()
        logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " started.")
    
    def stop(self):
        self.__running__ = False
        logging.info("[ModbusDevice] ID " + str(self.__serial__) + " stopping.")
        if(self.__modbusThread__ != None and self.__modbusThread__.is_alive()):
            self.__modbusThread__.join(3)     # todo: konstante verwenden
        for connection in self.__connections__:
            try:
                connection.loadlogdata()
                connection.sendlogdata()
                logging.info("[ModbusDevice] ID " + str(self.__serial__) + " logdata sent.")
            except:
                logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " cannot send logdata while stopping.")
            connection.disconnect()
    
    def getserial(self):
        return self.__serial__

    def getidentifier(self):
        return self.getserial()

    def getstate(self):
        return self.__running__
    
    def getdevicetype(self):
        return self.__devicetype__

    def getsetup(self): 
        return self.__setup__

    def setmodbusfrequency(self, frequency):
        if frequency != None and frequency >= 0 and frequency < 90000:
            self.__modbusFrequency__ = frequency
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " modbus frequency set to " + str(self.__modbusFrequency__))
            return True
        else:
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " set modbus frequency failed. Out of range: " + str(frequency))
            return False

    def setlogdatasendinterval(self, interval):
        if interval != None and interval >= 0 and interval < 90000:
            self.__logdatasendinterval__ = interval
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " logdata send interval set to " + str(self.__logdatasendinterval__))
            return True
        else:
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " set logdata send interval failed. Out of range: " + str(interval))
            return False

    def setstartregister(self, startRegister):
        if startRegister != None and startRegister >= 0 and startRegister < 10000:
            self.__startRegister__ = startRegister
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " start-register set to " + str(self.__startRegister__))
            return True
        else:
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " set start-register failed. Out of range: " + str(startRegister))
            return False

    def setregisterstoread(self, registersToRead):
        if registersToRead != None and registersToRead > 0 and registersToRead < 10000:
            self.__registersToRead__ = registersToRead
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " registersToRead set to " + str(self.__registersToRead__))
            return True
        else:
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " set registersToRead failed. Out of range: " + str(registersToRead))
            return False

    def __run__(self):
        while self.__running__:
            logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " monitor running...")
            for connection in self.__connections__:
                try:
                    connection.watchdog()
                except:
                    logging.error("[ModbusDevice] ID " + str(self.__serial__) + " watchdog failed.")

            if self.__logdatasendinterval__ > 0:
                if self.__lastlogdataSendTime__ == None:
                    self.__lastlogdataSendTime__ = datetime.now()
                else:
                    difference = datetime.now() - self.__lastlogdataSendTime__
                    if(difference.total_seconds() > self.__logdatasendinterval__):
                        for connection in self.__connections__:
                            try:
                                connection.loadlogdata()
                                connection.sendlogdata()
                                self.__lastlogdataSendTime__ = datetime.now()
                                logging.info("[ModbusDevice] ID " + str(self.__serial__) + " active sent logdata to server: " + str(connection.getServer()))
                            except Exception as e:
                                logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " active sending logdata to server " + str(connection.getServer()) + " failed. " + str(e))
            try:
                self.__supervise__()
            except Exception as e:
                logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " supervision failed. " + str(e))

            try:
                if self.__modBusExecuted__ != None:
                    difference = datetime.now() - self.__modBusExecuted__
                    if(difference.total_seconds() > self.__modbusFrequency__ * 3):
                        logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " modbus data too old: " + str(difference.total_seconds()))
                        if self.__datasets__ != None:
                            for dataset in self.__datasets__:
                                self.__data__[dataset] = None
            except Exception as e:
                logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " cleanup failed. " + str(e))

            time.sleep(DEVICESLEEPTIME)

    def setsetupvalue(self, key, value):
        logging.info("Setup Change: key="+str(key)+", value="+str(value))

        if key == None:
            msg="key required"
            raise TypeError(msg)

        if not isinstance(key, str):
            msg="key has to be a string"
            raise TypeError(msg)

        if value == None:
            msg="value required"
            raise TypeError(msg)

        if not isinstance(value, int):
            msg="value has to be a int"
            raise TypeError(msg)

        try:
            self.__setup__[key]
        except Exception as e:
            logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " Setup-Element does not exist: " + str(e))
            raise Exception("setup element does not exist.")
        try:
            self.__setup__[key] = value
            if key in self.__settingsMap__:
                register = self.__settingsMap__[key]["register"]
                self.writeregister(register, value)
                registervalue = self.readregister(register)
                if registervalue != value:
                    logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " Register verification failed. " + str(registervalue[register]))
                    raise Exception("register verification failed.")
            else:
                logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " no register mapping for key " + str(key))

        except Exception as e:
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " Setup change not successfull. " + str(e))
            raise e

    def __supervise__(self):
        errors = 0
        for connection in self.__connections__:
            try:
                if not connection.isconnected():
                    logging.info("[ModbusDevice] " + self.getidentifier() + " not connected to " + str(connection.getServer()))
                    errors += 1
            except Exception as e:
                logging.warning("[ModbusDevice] " + self.getidentifier() + " cannot check connection to " + str(connection.getServer()) + ". " + str(e))
        if errors == 0:
            logging.debug("[ModbusDevice] " + self.getidentifier() + ": DCS-Connections ok.")

    def __sethealthstate__(self, state):
        if state != None and state <= 3 and state >= 0:
            if self.__healthState__ != state:
                self.__healthState__ = state
                logging.info("[ModbusDevice] " + self.getidentifier() + ". HealthState set to " + str(state))
        else:
            logging.error("[ModbusDevice] " + self.getidentifier() + ". Cannot set healthState. Invalid state: " + str(state))
            raise Exception("invalid state " + str(state))

    def getHealthState(self):
        return self.__healthState__

    def __runmodbus__(self):
        while self.__running__:
            modbusstarttime = datetime.now()
            try:
                logging.debug("[ModbusDevice] " + self.getidentifier() + ". Running modbus...")
                self.__excecutemodbus__()
                self.__modBusExecuted__ = datetime.now()
            except Exception as e:
                logging.error("[ModbusDevice] " + self.getidentifier() + ". Modbus Thread Error: " + str(e))
            
            executiontime = datetime.now() - modbusstarttime
            logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " modbus execution time: " + str(executiontime.total_seconds()))
            if(executiontime.total_seconds() > DEFAULTMODBUSFREQUENCY):
                logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " modbus execution time too high: " + str(executiontime.total_seconds()))

            time.sleep(random.random())        
            time.sleep(self.__modbusFrequency__)

    def __excecutemodbus__(self):
        if self.__modbusFrequency__ > 0:
            logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " Modbus running...")
            try:
                self.__readallregisters__()
            except Exception as e:
                logging.error("[ModbusDevice] " + self.getidentifier() + ". Unknown modbus register read error: " + str(e))
                self.__registers__ = None
            if self.__registers__ != None:
                if len(self.__registers__) > 0:
                    try:
                        self.__syncsettings__()
                    except Exception as e:
                        logging.warning("[ModbusDevice] " + self.getidentifier() + ". Settingssync not successfull. " + str(e))
                else:
                    logging.debug("[ModbusDevice] " + self.getidentifier() + ". No bus communication to device.")
                
                try:
                    self.__processregisters__()
                except Exception as e:
                    logging.warning("[ModbusDevice] " + self.getidentifier() + ". processing registers not successfull. " + str(e))
            else:
                logging.debug("[ModbusDevice] " + self.getidentifier() + ". No registers to process.")

    def __syncsettings__(self):
        errors = 0
        if self.__settingsMap__ != None:
            for name in self.__settingsMap__:
                if self.__settingsMap__[name]["register"] in self.__registers__:
                    if name in self.__setup__:
                        if self.__registers__[self.__settingsMap__[name]["register"]] != self.__setup__[name]:
                            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " setting missmatch " + str(name) + " - Device: " + str(self.__registers__[self.__settingsMap__[name]["register"]]) + "; Setup: " + str(self.__setup__[name]) + ".")
                            if self.__settingsMap__[name]["forced"]:
                                try:
                                    self.writeregister(self.__settingsMap__[name]["register"], self.__setup__[name])
                                except Exception as e:
                                    logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " cannot write register while settings sync. Set " + str(name) + " to "+str(self.__setup__[name])+". " + str(e))
                                logging.info("[ModbusDevice] ID " + str(self.__serial__) + " forcing " + str(name) + " to "+str(self.__setup__[name])+".")
                            else:
                                self.__setup__[name] = self.__registers__[self.__settingsMap__[name]["register"]]
                                self.sendsetup()
                                logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " changed setup. " + str(name) + "=" + str(self.__setup__[name]) + ".")
                    else:
                        logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " setting element " + str(name) + " not found in setup.")
                        errors += 1
                else:
                    logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " register for setting " + str(name) + " not found.")
                    errors += 1
        if errors == 0:
            return True
        else:
            raise Exception("Errors with " + str(errors) + " elements")

    def sendsetup(self):
        success = True
        for connection in self.__connections__:
            if connection.isconnected():
                try:
                    connection.sendsetup()
                except Exception:
                    logging.error("[ModbusDevice] ID " + str(self.__serial__) + " cannot send setup change to server.")
                    success = False
        return success

    def readregister(self, registerId):
        register = self.__readregister__(registerId)
        return register

    def readregisters(self, startregisteraddress, registerstoread):
        return self.__readregisters__(startregisteraddress, registerstoread)

    def __readregister__(self, registerId):
        with self.__lock__:
            if registerId == 1234:
                self.__registers__[1234] = 432
            try:
                return self.__registers__[registerId]
            except Exception as e:
                raise Exception("Register " + str(e) + " cannot be read.")

    def __readallregisters__(self):
        if self.__startRegister__ != None and self.__registersToRead__ != None:
            logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " reading " + str(self.__registersToRead__) + " registers starting with " + str(self.__startRegister__))
            registers = self.__readregisters__(self.__startRegister__, self.__registersToRead__)
            if registers != None:
                self.__registers__ = registers
            else:
                self.__registers__.clear()
            self.__registerTimeStamp__ = time.time()
            if registers != None and len(registers) > 0:
                self.__registerLastSuccessfullReadTimeStamp__ = time.time()
        else:
            logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " no registers to read")

    def __readregisters__(self, startregisteraddress, registerstoread):
        with self.__lock__:
            registers = dict()
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " creating dummy data for " + str(self.__registersToRead__) + " registers")
            for i in range(registerstoread):
                registers[startregisteraddress + i] = i*1000
                if(i == 3):
                    registers[startregisteraddress + i] = None
                if(i == 5):
                    registers[startregisteraddress + i] = 65
                if(i == 13):
                    registers[startregisteraddress + i] = 1000
                if(i == 21):
                    registers[startregisteraddress + i] = datetime.now().minute
            return registers

    def writeregister(self, registerId, value):
        if registerId == None:
            msg="registerId required"
            raise TypeError(msg)

        if not isinstance(registerId, int):
            msg="registerId has to be a int"
            raise TypeError(msg)

        if value == None:
            msg="value required"
            raise TypeError(msg)

        if not isinstance(value, int):
            msg="value has to be a int"
            raise TypeError(msg)

        logging.debug(self.getidentifier() + ": writing register " + str(registerId) +" with value "+ str(value))
        self.__writeregister__(registerId, value)

    def __writeregister__(self, registerId, valueToWrite):
        with self.__lock__:
            logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " writing register " + str(registerId) + " value: " + str(valueToWrite))
            self.__registers__[registerId] = valueToWrite

    def getregistervalue(self, registerId):
        with self.__lock__:
            try:
                if(self.__registers__[registerId] != None):
                    value = {
                        "time": self.__registerTimeStamp__,
                        "value": self.__registers__[registerId]
                    }
                else:
                    value = None
            except Exception:
                logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " register not found. Register Id: " + str(registerId))
                value = None
        return value

    def __processregisters__(self):
        if self.__datasets__ != None:
            for dataset in self.__datasets__:
                registerid = self.__datasets__[dataset][0]
                register = self.getregistervalue(registerid)

                if register != None:
                    value = register["value"]
                    self.__data__[dataset] = value
                    self.__addtologdata__(dataset, register)
                    logging.debug("[ModbusDevice] ID " + str(self.__serial__) + ", dataset=" + str(dataset) + ", value=" + str(value) + " processed")
                else:
                    logging.debug("[ModbusDevice] ID " + str(self.__serial__) + " no value for dataset " + str(dataset))
                    self.__data__[dataset] = None
        else:
            logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " no datasets defined")
        self.__logdataTimeStamp__ = self.__registerTimeStamp__

    def __addtologdata__(self, datasetname, register):
        datasettype = self.__datasets__[datasetname][1]
        value = None
        if register["value"] != None:
            if(datasettype == "avg"):
                try:
                    self.__logdataCounter__[datasetname] = self.__logdataCounter__[datasetname] + 1
                except Exception:
                    self.__logdataCounter__[datasetname] = 1
                try:
                    self.__logdataSum__[datasetname] = self.__logdataSum__[datasetname] + register["value"]
                except Exception:
                    self.__logdataSum__[datasetname] = register["value"]
                value = self.__logdataSum__[datasetname] / self.__logdataCounter__[datasetname]
            if(datasettype == "sum"):
                try:
                    oldvalue = self.__logdata__[datasetname]
                except Exception:
                    oldvalue = 0
                try:
                    x0 = self.__logdataLastValue__[datasetname]
                except Exception:
                    x0 = 0
                if(x0 == None):
                    x0 = 0
                t0 = self.__logdataTimeStamp__
                if(t0 == None):
                    t0 = register["time"]
                x1 = register["value"]
                t1 = register["time"]
                dt = (t1 - t0)/3600
                newvalue = dt * ((x1 + x0)/2)
                value = oldvalue + newvalue
                self.__logdataLastValue__[datasetname] = x1
                # print(str(self.__serial__) + " Integrating " + str(datasetname) + ": dt="+str(round(dt, 4))+" x1="+str(round(x1, 4))+" x0="+str(round(x0, 4))+" oldvalue="+str(round(oldvalue, 4))+" newvalue="+str(round(newvalue, 4))+"  value="+str(round(value, 4)))
            self.__logdata__[datasetname] = value
    
    def getdataset(self, datasetname):
        if self.__data__ == None or len(self.__data__) == 0:
            return None

        try:
            return self.__data__[datasetname]
        except Exception:
            logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " dataset not found " + str(datasetname))
            return None 

    def getlogvalue(self, datasetname):
        if self.__logdata__ == None or len(self.__logdata__) == 0:
            return None

        try:
            return self.__logdata__[datasetname]
        except Exception:
            logging.warning("[ModbusDevice] ID " + str(self.__serial__) + " logvalue not found " + str(datasetname))
            return None

    def getintlogvalue(self, datasetname):
        logdata = self.getlogvalue(datasetname)
        if logdata != None:
            return int(logdata)
        else:
            return None
    
    def clearlog(self):
        self.__logdata__.clear()
        self.__logdataCounter__.clear()
        self.__logdataSum__.clear()
        self.__logdataTimeStamp__ = None

    def showinfo(self):
        if self.__datasets__ != None:
            for dataset in self.__datasets__:
                logging.info("[ModbusDevice] ID " + str(self.__serial__) + " " + dataset + ": Live: " + str(self.getdataset(dataset)) + ", Log: " + str(self.getlogvalue(dataset)) + ", HealthState: " + str(self.getHealthState()))
        else:
            print("[ModbusDevice] ID " + str(self.__serial__) + " no datasets defined")
            logging.info("[ModbusDevice] ID " + str(self.__serial__) + " no datasets defined")

    def getcommunicationerrorscounter(self):
        return 0

    def showcommunicationerrors(self):
        logging.info("[ModbusDevice] " + str(self.__serial__) + " - Communication Errors: " +  str(self.getcommunicationerrorscounter()))

    def getcommunicationerrorsrate(self):
        return 0

    def showcommunicationerrorsrate(self):
        rate = self.getcommunicationerrorsrate()
        if rate != None:
            rate = round(rate*100)
        logging.info("[ModbusDevice] " + str(self.getidentifier()) + " - Communication error-rate: " +  str(rate) + "%, Errors: " +  str(self.getcommunicationerrorscounter()))

    def __createDataset__(self, registerId, type):
        dataset = [registerId, type]
        return dataset

    #############

    def __createsetup__(self):
        return {
            "device": self.__devicetype__,
            "fwversion": self.__firmwareversion__,
            "serialno": self.__serial__,
            "ww2target": None,
            "ww2offset": 1514
            }

    def __getsettingsmap__(self):
        settings = {
            "ww2target": {
                "register": 1022,
                "forced": False
            },
            "ww2offset": {
                "register": 1023,
                "forced": True
            },
        }
        return settings
    
    def getdata(self):
        t = datetime.now()
        data = {
                "fwversion": self.__firmwareversion__,
				"power": t.second * 100,
                "temp1": t.minute,
                "check": 9544,
                "temp2": self.getdataset("temp2"),
				"loctime": time.strftime("%H:%M:%S")
                }            
        return data

    def getlogdata(self, time = None):
        logdata = {
            # "i_unknown": 123,
            "time": time,
            "i_power": self.getintlogvalue("power"),
            "i_boostpower": 750,
            "i_meterfeed": None,
            "i_metercons": 4,
            "i_temp1": self.getintlogvalue("temp1"),
            "i_m0l1": 6,
            "i_m0l2": 7,
            "i_m0l3": 8,
            "i_m1sum": 9,
            "i_m1l1": 10,
            "i_m1l2": 11,
            "i_m1l3": 12,
            "i_m2sum": 13,
            "i_m2l1": 14,
            "i_m2l2": 15,
            "i_m2l3": 16,
            "i_m2soc": 17,
            "i_m3sum": 18,
            "i_m3l1": 19,
            "i_m3l2": 20,
            "i_m3l3": 21,
            "i_m3soc": 22,
            "i_m4sum": 23,
            "i_m4l1": 24,
            "i_m4l2": 25,
            "i_m4l3": 26,
            "s_json" : "27",
            "i_temp2": self.getintlogvalue("temp2"),
            "i_power1": 29,
            "i_power2": 30,
            "i_power3": 31,
            "i_temp3": 32,
            "i_temp4": 33
            }
        return logdata

    def __getregistermapping__(self):
        datasets = {}
        datasets["power"] = self.__createDataset__(1013, "sum")
        datasets["test"] = self.__createDataset__(1014, "avg")
        datasets["inv"] = self.__createDataset__(1, "avg")
        datasets["temp1"] = self.__createDataset__(1005, "avg")
        return datasets

# Entry Point     
if __name__ == "__main__":

    # from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s [%(threadName)s]: %(message)s', level=logging.INFO)

    #device connection tests
    serial = "120100200505tes1"
    serial2 = "120100200505tes2"
    serial3 = "120100200505tes3"
    cryptoKey = "41424142414241424142414241424142"
    server = "my-pv.live"

    #AUTO-Tests
    #Constructor Tests
    try:
        device = ModbusDevice("123456789")
        print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))
        device = None

    try:
        device = ModbusDevice(None)
        print(color('ERROR: serial is None.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial is None.', fore='green', style='bright'))

    try:
        device = ModbusDevice(serial)
        print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
    except:
        print(color('ERROR: creating valid device.', fore='red', style='bright'))

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
        logdata = device.getlogdata()
        if(logdata == None):
            raise Exception("logdata is None")
        print(color('SUCCESS: getting device logdata.', fore='green', style='bright'))
    except:
        print(color('ERROR: getting device logdata.', fore='red', style='bright'))

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
        if(temp == "Dummy-Device"):
            print(color('SUCCESS: getting device type.', fore='green', style='bright'))
        else:
            raise Exception("device type does not match.")
    except:
        print(color('ERROR: getting device type.', fore='red', style='bright'))
  
    if(device != None and not device.setmodbusfrequency(None)):
        print(color('SUCCESS: setting modbus frequency (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (None).', fore='red', style='bright'))

    if(device != None and device.setmodbusfrequency(0)):
        print(color('SUCCESS: setting modbus frequency (0).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (0).', fore='red', style='bright'))
    
    if(device != None and device.setmodbusfrequency(10)):
        print(color('SUCCESS: setting modbus frequency (10).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (10).', fore='red', style='bright'))

    if(device != None and not device.setmodbusfrequency(90000)):
        print(color('SUCCESS: setting modbus frequency (90000).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus frequency (90000).', fore='red', style='bright'))

    if(device != None and not device.setstartregister(90000)):
        print(color('SUCCESS: setting modbus startRegister (90000).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (90000).', fore='red', style='bright'))

    if(device != None and device.setstartregister(1234)):
        print(color('SUCCESS: setting modbus startRegister (1234).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (1234).', fore='red', style='bright'))

    if(device != None and not device.setstartregister(None)):
        print(color('SUCCESS: setting modbus startRegister (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (None).', fore='red', style='bright'))

    if(device != None and device.setstartregister(0)):
        print(color('SUCCESS: setting modbus startRegister (0).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus startRegister (0).', fore='red', style='bright'))

    if(device != None and not device.setregisterstoread(90000)):
        print(color('SUCCESS: setting modbus registers to read (90000).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (90000).', fore='red', style='bright'))

    if(device != None and not device.setregisterstoread(None)):
        print(color('SUCCESS: setting modbus registers to read (None).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (None).', fore='red', style='bright'))

    if(device != None and not device.setregisterstoread(0)):
        print(color('SUCCESS: setting modbus registers to read (0).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (0).', fore='red', style='bright'))

    if(device != None and device.setregisterstoread(3)):
        print(color('SUCCESS: setting modbus registers to read (3).', fore='green', style='bright'))
    else:
        print(color('ERROR: setting modbus registers to read (3).', fore='red', style='bright'))

    if(device != None):
        try:
            register = device.readregister(1234)
            if register == 432:
                print(color('SUCCESS: reading register.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading register. Value missmatch: ' + str(register), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading register. Error: ' + str(e), fore='red', style='bright'))

    if(device != None):
        try:
            registers = device.readregisters(1000, 10)
            if registers[1000] == 0 and registers[1001] == 1000:
                print(color('SUCCESS: reading registers.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading registers. Value missmatch: ' + str(registers), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading registers. Error: ' + str(e), fore='red', style='bright'))

    if(device != None):
        try:
            device.writeregister(123,33)
            print(color('SUCCESS: writing Register.', fore='green', style='bright'))
        except Exception as e:
            print(color('ERROR: writing Register.', fore='red', style='bright'))

    key = "ww2target"
    targetValue = 30
    if device != None:
        try:
            device.setsetupvalue(key, targetValue)
            setup = device.getsetup()
            if setup[key] == targetValue:
                print(color('SUCCESS: Setting setup value with register key.', fore='green', style='bright'))
            else:
                raise Exception()
        except Exception as e:
            print(color('ERROR: Setting setup value with register key.', fore='red', style='bright'))

    key = "fwversion"
    targetValue = 40
    if device != None:
        try:
            device.setsetupvalue(key, targetValue)
            setup = device.getsetup()
            if setup[key] == targetValue:
                print(color('SUCCESS: Setting setup value without register key.', fore='green', style='bright'))
            else:
                raise Exception()
        except Exception as e:
            print(color('ERROR: Setting setup value without register key.', fore='red', style='bright'))

    key = "testkey"
    targetValue = 33
    if device != None:
        try:
            device.setsetupvalue(key, targetValue)
            print(color('ERROR: Setting invalid setting key.', fore='red', style='bright'))
        except Exception as e:
            print(color('SUCCESS: Setting invalid setting key.', fore='green', style='bright'))
            

    connection = DcsConnection(serial, cryptoKey, server, 50333)
    try:
        device.addconnection(connection)
        print(color('SUCCESS: adding connection to device.', fore='green', style='bright'))
    except Exception:
        print(color('ERROR: adding connection to device.', fore='red', style='bright'))

    try:
        device.start()
        print(color('SUCCESS: starting device.', fore='green', style='bright'))
    except Exception:
        print(color('ERROR: starting device.', fore='red', style='bright'))

    try:
        temp = device.getstate()
        if(temp == True):
            print(color('SUCCESS: getting device state (running).', fore='green', style='bright'))
        else:
            raise Exception("device state is not running.")
    except Exception:
        print(color('ERROR: getting device state (running).', fore='red', style='bright'))

    time.sleep(10)
 
    try:
        device.stop()
        print(color('SUCCESS: stopping device.', fore='green', style='bright'))
    except Exception:
        print(color('ERROR: stopping device.', fore='red', style='bright'))

    try:
        temp = device.getstate()
        if(temp == False):
            print(color('SUCCESS: getting device state (stopped).', fore='green', style='bright'))
        else:
            raise Exception("device state is not stopped.")
    except Exception:
        print(color('ERROR: getting device state (stopped).', fore='red', style='bright'))


    device = ModbusDevice(serial)
    connection = DcsConnection(serial, cryptoKey, server, 50333)
    device.addconnection(connection)
    device.start()

    if(device.setlogdatasendinterval(0)):
        print(color('SUCCESS: setting logdata send interval to 0.', fore='green', style='bright'))
    else:
        print(color('ERROR: setting logdata send interval to 0.', fore='red', style='bright'))

    if(device.setlogdatasendinterval(1111111)):
        print(color('ERROR: setting logdata send interval to 1111111.', fore='red', style='bright'))
    else:
        print(color('SUCCESS: setting logdata send interval to 1111111.', fore='green', style='bright'))

    if(device.setlogdatasendinterval(10)):
        print(color('SUCCESS: setting logdata send interval to 10.', fore='green', style='bright'))
    else:
        print(color('ERROR: setting logdata send interval to 10.', fore='red', style='bright'))
    
    time.sleep(20)
    device.stop()
 
    #Modbus tests
    device = ModbusDevice(serial)
    try:
        device.__readallregisters__()
        print(color('SUCCESS: reading registers.', fore='green', style='bright'))
    except:
        print(color('ERROR: reading registers.', fore='red', style='bright'))

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
    
    register = device.getregistervalue(1014)
    if(register != None and register["value"] == 14000):
        print(color('SUCCESS: reading valid register.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading valid register.', fore='red', style='bright'))

    register = device.getregistervalue(1003)
    if(register == None):
        print(color('SUCCESS: reading register that should be none.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading register that should be none.', fore='red', style='bright'))

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

    if(device.getdataset("power") == 1000 ):
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

    if( device.getlogvalue("test") == 14000 ):
        print(color('SUCCESS: getting logvalue (test).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test).', fore='red', style='bright'))

    time.sleep(1)
    device.__readallregisters__()
    device.__processregisters__()
    if( device.getlogvalue("power") > 0 ):
        print(color('SUCCESS: getting logvalue (power) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after wait.', fore='red', style='bright'))

    if( device.getlogvalue("test") == 14000 ):
        print(color('SUCCESS: getting logvalue (test) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after wait.', fore='red', style='bright'))

    if( device.getlogvalue("abc") == None ):
        print(color('SUCCESS: getting logvalue (abc) after wait.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (abc) after wait.', fore='red', style='bright'))

    device.stop()
    time.sleep(10)

    device = ModbusDevice(serial2)
    device.__running__ = True
    avgVal0 = device.getlogvalue("test")
    sumVal0 = device.getlogvalue("power")
    device.__excecutemodbus__()
    avgVal1 = device.getlogvalue("test")
    sumVal1 = device.getlogvalue("power")
    device.__excecutemodbus__()
    avgVal2 = device.getlogvalue("test")
    sumVal2 = device.getlogvalue("power")
    device.__excecutemodbus__()
    avgVal3 = device.getlogvalue("test")
    sumVal3 = device.getlogvalue("power")
    device.__excecutemodbus__()
    avgVal4 = device.getlogvalue("test")
    sumVal4 = device.getlogvalue("power")
    if( avgVal4 == avgVal1 and sumVal4 > sumVal2):
        print(color('SUCCESS: checking calculation.', fore='green', style='bright'))
    else:
        print(color('ERROR: checking calculation.', fore='red', style='bright'))

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

    device = ModbusDevice(serial)
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

    value = device.getlogvalue("power")
    if(value != None and value > 0 ):
        print(color('SUCCESS: getting logvalue (power) after starting device with frequency >0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power) after starting device with frequency >0.', fore='red', style='bright'))

    if( device.getlogvalue("test") == 14000 ):
        print(color('SUCCESS: getting logvalue (test) after starting device with frequency >0.', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (test) after starting device with frequency >0.', fore='red', style='bright'))

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

    time.sleep(5)
    #DCS communication tests
    device = ModbusDevice(serial3)
    connection = DcsConnection(serial3, cryptoKey, server, 50333)
    device.addconnection(connection)
    # device.setlogdatasendinterval(5)
    device.start()
    try:
        while True:
            print(color('[ModbusDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            device.showinfo()
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
    input("waiting...  PRESS ENTER")
