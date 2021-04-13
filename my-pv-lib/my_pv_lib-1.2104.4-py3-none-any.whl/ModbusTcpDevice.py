#!/usr/bin/python

import logging
from socket import gaierror
import threading
from pyModbusTCP.client import ModbusClient
import sys
import os
from colr import color
import time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusDevice import ModbusDevice
from mypvdevices.DeviceDiscoverer import DeviceDiscoverer

RESOLVEHOSTERROR = 99

class ModbusTcpException(Exception):
    def __init__(self, msg, code):

        if code == None:
            msg="errorcode required"
            raise TypeError(msg)

        self.code = code
        self.message = msg
    def __str__(self):
        return repr(str(self.message) + ". Error-Code: " + str(self.code))

class ModbusTcpDevice(ModbusDevice):
    __devicetype__ = "ModbusTcpDevice"
    __mutex__ = threading.Lock()
    __modbusClient__ = None
    __host__ = None
    __modbushosterror__ = False
    __modbusconnectionerrorcounter__ = 0
    __modbusconnectioncounter__ = 0

    def __init__(self, serial):
        ModbusDevice.__init__(self, serial)
        self.recoverhost()

    def getidentifier(self):
        return self.getserial() + ", Host: " + str(self.__host__)

    def sethost(self, hostname):
        logging.info(self.getidentifier() + " Setting host to " + str(hostname))

        if hostname == None:
            msg="hostname required"
            logging.debug(self.getidentifier() + ": " + str(msg))
            raise TypeError(msg)

        if not isinstance(hostname, str):
            msg="hostname hast to be a string"
            logging.debug(self.getidentifier() + ": " + str(msg))
            raise TypeError(msg)

        self.__host__ = hostname

        if self.__modbusClient__ == None:
            try:
                self.__modbusClient__ = ModbusClient(host=self.__host__, port=502, timeout=5, auto_open=True, auto_close=True)
            except ValueError:
                print("Error with host or port params")
        else:
            self.__modbusClient__.host(self.__host__)

    def __readregisters__(self, startregisteraddress, registerstoread):
        with self.__mutex__:
            time.sleep(0.5)
            if self.__modbusClient__ != None:
                logging.debug(self.getidentifier() + ": Reading " + str(registerstoread) +" registers starting with register "+ str(startregisteraddress))
                registers = dict()
                try:
                    self.__modbusconnectioncounter__ += 1
                    modbus_response = self.__modbusClient__.read_holding_registers(startregisteraddress, registerstoread)
                    self.__modbushosterror__ = False
                    if modbus_response == None:
                        errorcode = self.__modbusClient__.last_error()

                        if errorcode == 2:
                            raise ModbusTcpException("Host not reachable " + str(self.__modbusClient__.host()), errorcode)
                        elif errorcode == 4:
                            raise ModbusTcpException("Invalid Registers " + str(startregisteraddress) + " " + str(registerstoread), errorcode)
                        else:
                            raise ModbusTcpException("Unknown Error. Error Code " + str(errorcode), errorcode)

                    logging.debug(self.getidentifier() + ": Data: " + str(modbus_response))
                    for i in range(len(modbus_response)):
                        registers[startregisteraddress + i] = modbus_response[i]
                except gaierror as e:
                    logging.warning(self.getidentifier() + " Cannot resolve host: " + str(self.__modbusClient__.host()))
                    self.__modbushosterror__ = True
                    self.__increaseModbusErrorCounter__()
                    raise ModbusTcpException("Cannot resolve host. " + str(self.__modbusClient__.host()), RESOLVEHOSTERROR)
                
                except Exception as e:
                    logging.warning(self.getidentifier() + ": Host: " + str(self.__modbusClient__.host()) + " Modbus read error: " + str(e))
                    self.__increaseModbusErrorCounter__()
                    raise e

                return registers

            else:
                logging.error(self.getidentifier() + ": no Modbus-Client ")
                return None

    def __readregister__(self, registeraddress):
        with self.__mutex__:
            time.sleep(0.5)
            if self.__modbusClient__ != None:
                logging.debug(self.getidentifier() + ": Reading register " + str(registeraddress))
                try:
                    self.__modbusconnectioncounter__ += 1
                    modbus_response = self.__modbusClient__.read_holding_registers(registeraddress, 1)
                    self.__modbushosterror__ = False
                    if modbus_response == None:
                        errorcode = self.__modbusClient__.last_error()

                        if errorcode == 2:
                            raise ModbusTcpException("Host not reachable " + str(self.__modbusClient__.host()), errorcode)
                        elif errorcode == 4:
                            raise ModbusTcpException("Invalid Register " + str(registeraddress), errorcode)
                        else:
                            raise ModbusTcpException("Unknown Error. Error Code " + str(errorcode), errorcode)

                    logging.debug(self.getidentifier() + ": Data: " + str(modbus_response))
                    register = modbus_response[0]
                    return register

                except gaierror as e:
                    logging.warning(self.getidentifier() + " Cannot resolve host: " + str(self.__modbusClient__.host()))
                    self.__modbushosterror__ = True
                    self.__increaseModbusErrorCounter__()
                    raise ModbusTcpException("Cannot resolve host. " + str(self.__modbusClient__.host()), RESOLVEHOSTERROR)
                
                except Exception as e:
                    logging.warning(self.getidentifier() + ". Modbus error: " + str(e))
                    self.__increaseModbusErrorCounter__()
                    raise e
            else:
                logging.error(self.getidentifier() + ": no Modbus-Client ")
                raise Exception("Register " + str(registeraddress) + " cannot be read. No modbus-client.")

    def __writeregister__(self, registerId, value):
        with self.__mutex__:
            time.sleep(0.5)
            if self.__modbusClient__ != None:
                try:
                    self.__modbusconnectioncounter__ += 1
                    result = self.__modbusClient__.write_single_register(registerId, value)
                    self.__modbushosterror__ = False
                except gaierror as e:
                    logging.warning(self.getidentifier() + " Cannot resolve host: " + str(self.__modbusClient__.host()))
                    self.__modbushosterror__ = True
                    self.__increaseModbusErrorCounter__()
                    raise ModbusTcpException("Cannot resolve host. " + str(self.__modbusClient__.host()), RESOLVEHOSTERROR)
                except Exception as e:
                    logging.warning(self.getidentifier() + " Modbus Write Error: " + str(e))
                    self.__increaseModbusErrorCounter__()
                    raise e
                if result == None:
                    logging.warning(self.getidentifier() + " Cannot write register. Register " + str(registerId))
                    self.__increaseModbusErrorCounter__()
                    raise ModbusTcpException("Cannot write register " + str(registerId), 22)    #Todo errornr

    def __supervise__(self):
        ModbusDevice.__supervise__(self)
        if self.__modbushosterror__:
            if not self.recoverhost():
                logging.warning(self.getidentifier() + " Cannot rediscover host.")
                    
    def getcommunicationerrorscounter(self):
        return self.__modbusconnectionerrorcounter__

    def getcommunicationerrorsrate(self):
        with self.__mutex__:
            errorRate = None
            try:
                errorRate = round(self.__modbusconnectionerrorcounter__ / self.__modbusconnectioncounter__, 2)
            except:
                logging.debug(self.getidentifier() + " Cannot calculate modbus tcp error rate.")
            return errorRate

    def resetCounters(self, nodeId):
        with self.__mutex__:
            try:
                self.__modbusconnectionerrorcounter__ = 0
                self.__modbusconnectioncounter__ = 0
            except Exception as e:
                logging.error(self.getidentifier() + " Error resetting modbus tcp connection counters. " + str(e))

    def __increaseModbusErrorCounter__(self):
        self.__modbusconnectionerrorcounter__ += self.__modbusconnectionerrorcounter__
        logging.debug(self.getidentifier() + " Communication error. Total errors: " + str(self.__modbusconnectionerrorcounter__))
        return self.__modbusconnectionerrorcounter__

    def discoverDevice(self):
        try:
            return DeviceDiscoverer.instance().getipforserial(self.__serial__)
        except Exception as e:
            logging.warning(self.getidentifier() + " Cannot discover device " + str(self.__serial__) + ". Error: " + str(e))
            return None

    def recoverhost(self):
        host = self.discoverDevice()
        if host == None:
            logging.warning(self.getidentifier() + " Cannot recover host.")
            return False
        else:
            self.sethost(host)
            return True

    def __getregistermapping__(self):
        datasets = {}
        datasets["power"] = self.__createDataset__(1000, "sum")
        datasets["hour"] = self.__createDataset__(1009, "avg")
        datasets["temp1"] = self.__createDataset__(1001, "avg")
        return datasets

    def __createsetup__(self):
        return {
            "device": self.__devicetype__,
            "fwversion": self.__firmwareversion__,
            "serialno": self.__serial__,
            "boost_mode": 0,
            "test": 33
            }

    def __getsettingsmap__(self):
        settings = {
            "boost_mode": {
                "register": 1005,
                "forced": True
            },
            "test": {
                "register": 1018,
                "forced": True
            }
        }
        return settings

# Entry Point     
if __name__ == "__main__":

    from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.INFO)

    # serial = "1601242002040015"
    serial = "2001002006100016"
    serial_fake = "2001005006100000"
    correctip = "192.168.92.29"

    #device connection tests
    dcsserial = "120100200505tes1"
    cryptoKey = "41424142414241424142414241424142"
    server = "my-pv.live"


    # #Test
    # device = ModbusTcpDevice(serial)
    # register = device.readregister(1001)
    # # device.sethost("seppi")
    # device.sethost("192.168.92.254")
    # register = device.readregister(1001)

    # connection = DcsConnection(dcsserial, cryptoKey, server, 50333)
    # # device.addconnection(connection)
    # # device.setLogDataSendInterval(5)
    # device.start()
    # try:
    #     while True:
    #         print(color('[ModbusTcpDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
    #         device.showinfo()
    #         device.showcommunicationerrors()
    #         device.showcommunicationerrorsrate()
    #         time.sleep(10)
    # except KeyboardInterrupt as e:
    #     print("[DCS-Connection] Stopping Test...")
    #     device.stop()



    #Constructor Tests
    try:
        device = ModbusTcpDevice("123456789")
        print(color('ERROR: serial invalid lengh.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial invalid lengh.', fore='green', style='bright'))
        device = None

    try:
        device = ModbusTcpDevice(None)
        print(color('ERROR: serial is None.', fore='red', style='bright'))
    except:
        print(color('SUCCESS: serial is None.', fore='green', style='bright'))

    try:
        device = ModbusTcpDevice(serial)
        print(color('SUCCESS: creating valid device.', fore='green', style='bright'))
    except:
        print(color('ERROR: creating valid device.', fore='red', style='bright'))

    identifier = device.getidentifier()
    if identifier == serial:
        print(color('SUCCESS: checking identifier.', fore='green', style='bright'))
    else:
        print(color('ERROR: checking identifier.', fore='red', style='bright'))

    try:
        setup = device.getsetup()
        if setup == None:
            raise Exception("Setup is None")
        if setup["device"] == "ModbusTcpDevice":
            print(color('SUCCESS: getting device Setup.', fore='green', style='bright'))
        else:
            raise Exception("Setup not valid")
    except Exception as e:
        print(color('ERROR: getting device Setup. Message: ' + str(e), fore='red', style='bright'))

    try:
        data = device.getdata()
        if data == None:
            raise Exception("Data is None")
        if data["check"] == 9544:
            print(color('SUCCESS: getting device data.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
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
        if(temp == "ModbusTcpDevice"):
            print(color('SUCCESS: getting device type.', fore='green', style='bright'))
        else:
            raise Exception("device type does not match.")
    except:
        print(color('ERROR: getting device type.', fore='red', style='bright'))
 
    device = ModbusTcpDevice(serial_fake)

    try:
        register = device.readregister(1001)
        print(color('ERROR: reading register without modbus client.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: reading register without modbus client.', fore='green', style='bright'))

    try:
        registers = device.readregisters(1001,10)
        if registers == None:
            print(color('SUCCESS: reading registers without modbus client.', fore='green', style='bright'))
        else:
            print(color('ERROR: reading registers without modbus client.', fore='red', style='bright'))
    except Exception as e:
        print(color('ERROR: reading registers without modbus client. ' + str(e), fore='red', style='bright'))

    try:
        register = device.__readallregisters__()
        print(color('SUCCESS: reading all register without modbus client.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: reading all register without modbus client. ' + str(e), fore='red', style='bright'))

    try:
        device.writeregister(1000, 55)
        print(color('SUCCESS: writing register without modbus client.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: writing register without modbus client.', fore='red', style='bright'))

    try:
        device.sethost(None)
        print(color('ERROR: setting host to none host.', fore='red', style='bright'))        
    except Exception as e:
        print(color('SUCCESS: setting host to none host.', fore='green', style='bright'))

    try:
        device.sethost(123)
        print(color('ERROR: setting host to int host.', fore='red', style='bright'))        
    except Exception as e:
        print(color('SUCCESS: setting host to int host.', fore='green', style='bright'))

    try:
        device.sethost(correctip)
        print(color('SUCCESS: setting host to vaild host.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: setting host to vaild host.', fore='red', style='bright'))
    
    try:
        device.sethost("myhost")
        print(color('SUCCESS: setting host to unreachable host.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: setting host to unreachable host.', fore='red', style='bright'))
    
    try:
        register = device.readregister(1001)
        print(color('ERROR: reading register from unreachable host.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: reading register from unreachable host.', fore='green', style='bright'))

    try:
        registers = device.readregisters(1001,10)
        print(color('ERROR: reading registers from unreachable host.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: reading registers from unreachable host.', fore='green', style='bright'))

    try:
        register = device.__readallregisters__()
        print(color('ERROR: reading all register from unreachable host.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: reading all register from unreachable host.', fore='green', style='bright'))

    try:
        device.writeregister(1000, 55)
        print(color('ERROR: writing register to unreachable host.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: writing register to unreachable host.', fore='green', style='bright'))    

    # setting working host
    device = ModbusTcpDevice(serial)

    try:
        register = device.readregister(1001)
        if register >= 0 and register < 1000:
            print(color('SUCCESS: reading register from valid host.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: reading register from valid host. ' + str(e), fore='red', style='bright'))

    try:
        registers = device.readregisters(1000, 10)
        if registers[1001] >= 0 and registers[1001] < 1000:
            print(color('SUCCESS: reading registers from valid host.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: reading registers from valid host. ' + str(e), fore='red', style='bright'))

    try:
        register = device.__readallregisters__()
        print(color('SUCCESS: reading all register from valid host.', fore='green', style='bright'))        
    except Exception as e:
        print(color('ERROR: reading all register from vaild host. ' + str(e), fore='red', style='bright'))

    try:
        device.writeregister(1040, 55)
        print(color('SUCCESS: writing register to valid host.', fore='green', style='bright')) 
    except Exception as e:
        print(color('ERROR: writing register to valid host.', fore='red', style='bright'))

    try:
        device.writeregister(1001, 55)
        print(color('ERROR: writing not writeable register to valid host.', fore='red', style='bright')) 
    except Exception as e:
        print(color('SUCCESS: writing not writeable register to valid host.', fore='green', style='bright')) 

    try:
        host = device.discoverDevice()
        print(color('SUCCESS: discovering device.', fore='green', style='bright')) 
    except Exception as e:
        host = None
        print(color('ERROR: discovering device.', fore='red', style='bright')) 

    if host == correctip:
        print(color('SUCCESS: device discover. ' + str(host), fore='green', style='bright'))
    else:
        print(color('ERROR: device discover. Device not found. Check if in same subnet! Host:' + str(host), fore='red', style='bright')) 

    if(device.getregistervalue(50) == None ):
        print(color('SUCCESS: reading unknown register.', fore='green', style='bright'))
    else:
        print(color('ERROR: reading unknown register.', fore='red', style='bright'))
    
    register = device.getregistervalue(1001)
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

    value = device.getdataset("power")
    if(value != None and value >= 0 ):
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

    value = device.getlogvalue("power")
    if(value != None and value == 0 ):
        print(color('SUCCESS: getting logvalue (power).', fore='green', style='bright'))
    else:
        print(color('ERROR: getting logvalue (power).', fore='red', style='bright'))

    device = ModbusTcpDevice(serial)
    device.sethost("dsfjsdljjl")

    try:
        register = device.readregister(1001)
        print(color('ERROR: reading register from invaild host.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: reading register from invaild host.', fore='green', style='bright'))

    try:
        register = device.readregisters(1001, 4)
        print(color('ERROR: reading register from invaild host.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: reading register from invaild host.', fore='green', style='bright'))

    try:
        device.writeregister(1040, 35)
        print(color('ERROR: reading register from invaild host.', fore='red', style='bright'))
    except Exception as e:
        print(color('SUCCESS: reading register from invaild host.', fore='green', style='bright'))

    device.__supervise__()

    try:
        register = device.readregister(1001)
        print(color('SUCCESS: reading register from valid host after supervice.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: reading register from valid host after supervice.', fore='red', style='bright'))

    try:
        register = device.readregisters(1001, 4)
        print(color('SUCCESS: reading registers from valid host after supervice.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: reading registers from valid host after supervice.', fore='red', style='bright'))

    try:
        device.writeregister(1040, 35)
        print(color('SUCCESS: writing register to valid host after supervice.', fore='green', style='bright'))
    except Exception as e:
        print(color('ERROR: writing register to valid host after supervice.', fore='red', style='bright'))

    device = ModbusTcpDevice(serial)
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

    device = ModbusTcpDevice(serial)
    device.start()
    time.sleep(5)
    device.sethost("invalidhost")
    time.sleep(10)

    try:
        register = device.readregister(1001)
        if register >= 0 and register < 1000:
            print(color('SUCCESS: reading register from valid host after discover.', fore='green', style='bright'))
        else:
            raise Exception("invalid value")
    except Exception as e:
        print(color('ERROR: reading register from valid host after discover. ' + str(e), fore='red', style='bright'))

    device.stop()
    time.sleep(1)

    #DCS communication tests
    device = ModbusTcpDevice(serial)
    connection = DcsConnection(dcsserial, cryptoKey, server, 50333)
    device.addconnection(connection)
    # device.setLogDataSendInterval(5)
    device.start()
    try:
        while True:
            print(color('[ModbusTcpDevice] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            device.showinfo()
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
