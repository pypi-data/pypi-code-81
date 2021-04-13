#!/usr/bin/python

from _pytest.compat import STRING_TYPES
from colr import color
from datetime import datetime, timedelta
import logging
import sys
import os
import time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mypvdevices.ModbusTcpDevice import ModbusTcpDevice

class DeviceAcThor(ModbusTcpDevice):
    __devicetype__ = "AC Thor"

    def __init__(self, serial):
        ModbusTcpDevice.__init__(self, serial)
        self.__startRegister__ = 1000
        self.__registersToRead__ = 81

    def __getregistermapping__(self):
        datasets = {}
        datasets["power"] = self.__createDataset__(1000, "sum")
        datasets["temp1"] = self.__createDataset__(1001, "avg")
        datasets["ww1_temp_max"] = self.__createDataset__(1002, "avg")
        datasets["status"] = self.__createDataset__(1003, "avg")
        datasets["power_timeout"] = self.__createDataset__(1004, "avg")
        datasets["boost_mode"] = self.__createDataset__(1005, "avg")
        datasets["ww1_temp_min"] = self.__createDataset__(1006, "avg")
        datasets["boost_time_1_start"] = self.__createDataset__(1007, "avg")
        datasets["boost_time_1_stop"] = self.__createDataset__(1008, "avg")
        datasets["hour"] = self.__createDataset__(1009, "avg")
        datasets["minute"] = self.__createDataset__(1010, "avg")
        datasets["second"] = self.__createDataset__(1011, "avg")
        datasets["boost_activate"] = self.__createDataset__(1012, "avg")
        datasets["acthor_nummber"] = self.__createDataset__(1013, "avg")
        datasets["power_max"] = self.__createDataset__(1014, "sum")
        datasets["temp_chip"] = self.__createDataset__(1015, "avg")
        datasets["control_fw_version"] = self.__createDataset__(1016, "avg")
        datasets["ps_fw_version"] = self.__createDataset__(1017, "avg")
        datasets["acthor_serial_p1"] = self.__createDataset__(1018, "avg")
        datasets["acthor_serial_p2"] = self.__createDataset__(1019, "avg")
        datasets["acthor_serial_p3"] = self.__createDataset__(1020, "avg")
        datasets["acthor_serial_p4"] = self.__createDataset__(1021, "avg")
        datasets["acthor_serial_p5"] = self.__createDataset__(1022, "avg")
        datasets["acthor_serial_p6"] = self.__createDataset__(1023, "avg")
        datasets["acthor_serial_p7"] = self.__createDataset__(1024, "avg")
        datasets["acthor_serial_p8"] = self.__createDataset__(1025, "avg")
        datasets["boost_time_2_start"] = self.__createDataset__(1026, "avg")
        datasets["boost_time_2_stop"] = self.__createDataset__(1027, "avg")
        datasets["control_fw_subversion"] = self.__createDataset__(1028, "avg")
        datasets["control_fw_update_available"] = self.__createDataset__(1029, "avg")
        datasets["temp2"] = self.__createDataset__(1030, "avg")
        datasets["temp3"] = self.__createDataset__(1031, "avg")
        datasets["temp4"] = self.__createDataset__(1032, "avg")
        datasets["temp5"] = self.__createDataset__(1033, "avg")
        datasets["temp6"] = self.__createDataset__(1034, "avg")
        datasets["temp7"] = self.__createDataset__(1035, "avg")
        datasets["temp8"] = self.__createDataset__(1036, "avg")
        datasets["ww2_max"] = self.__createDataset__(1037, "avg")
        datasets["ww3_max"] = self.__createDataset__(1038, "avg")
        datasets["ww2_min"] = self.__createDataset__(1039, "avg")
        datasets["ww3_min"] = self.__createDataset__(1040, "avg")
        datasets["rh1_max"] = self.__createDataset__(1041, "avg")
        datasets["rh2_max"] = self.__createDataset__(1042, "avg")
        datasets["rh3_max"] = self.__createDataset__(1043, "avg")
        datasets["rh1_day_min"] = self.__createDataset__(1044, "avg")
        datasets["rh2_day_min"] = self.__createDataset__(1045, "avg")
        datasets["rh3_day_min"] = self.__createDataset__(1046, "avg")
        datasets["rh1_night_min"] = self.__createDataset__(1047, "avg")
        datasets["rh2_night_min"] = self.__createDataset__(1048, "avg")
        datasets["rh3_night_min"] = self.__createDataset__(1049, "avg")
        datasets["night_flag"] = self.__createDataset__(1050, "avg")
        datasets["utc_correction"] = self.__createDataset__(1051, "avg")
        datasets["dst_correction"] = self.__createDataset__(1052, "avg")
        datasets["legionella_interval"] = self.__createDataset__(1053, "avg")
        datasets["legionella_start"] = self.__createDataset__(1054, "avg")
        datasets["legionella_temp"] = self.__createDataset__(1055, "avg")
        datasets["legionella _mode"] = self.__createDataset__(1056, "avg")
        datasets["stratification_flag"] = self.__createDataset__(1057, "avg")
        datasets["relay1_state"] = self.__createDataset__(1058, "avg")
        datasets["load_state"] = self.__createDataset__(1059, "avg")
        datasets["load_nominal_power"] = self.__createDataset__(1060, "avg")
        datasets["u_l1"] = self.__createDataset__(1061, "avg")
        datasets["i_li"] = self.__createDataset__(1062, "avg")
        datasets["u_out"] = self.__createDataset__(1063, "avg")
        datasets["frequ"] = self.__createDataset__(1064, "avg")
        datasets["operation_mode"] = self.__createDataset__(1065, "avg")
        datasets["access_level"] = self.__createDataset__(1066, "avg")
        datasets["u_l2"] = self.__createDataset__(1067, "avg")
        datasets["i_l2"] = self.__createDataset__(1068, "avg")
        datasets["meter_power"] = self.__createDataset__(1069, "avg")
        datasets["control_type"] = self.__createDataset__(1070, "avg")
        datasets["power_max_abs"] = self.__createDataset__(1071, "avg")
        datasets["u_l3"] = self.__createDataset__(1072, "avg")
        datasets["i_l3"] = self.__createDataset__(1073, "avg")
        datasets["power_out_1"] = self.__createDataset__(1074, "avg")
        datasets["power_out_2"] = self.__createDataset__(1075, "avg")
        datasets["power_out_3"] = self.__createDataset__(1076, "avg")
        datasets["operation_state"] = self.__createDataset__(1077, "avg")
        datasets["power_high_word"] = self.__createDataset__(1078, "avg")
        datasets["power_low_word"] = self.__createDataset__(1079, "avg")
        datasets["power_plus_relays"] = self.__createDataset__(1080, "avg")
        return datasets

    def __createsetup__(self):
        return {
            "device": self.__devicetype__, \
            "fwversion": self.__firmwareversion__, \
            "serialno": self.__serial__, \
            "ww1_max": None, \
            "ww1_min": 100
            }

    def __getsettingsmap__(self):
        settings = {
            "ww1_max": {
                "register": 1002,
                "forced": False
            },
        }
        return settings

    def getdata(self):

        data={
            "device": self.__devicetype__,
            "fwversion": self.__firmwareversion__,
            "loctime": time.strftime("%H:%M:%S")
        }       
        return data

    def getlogdata(self, time = None):

        logdata={
            "time": time,
            "device": self.__devicetype__,
            "fwversion": self.__firmwareversion__
        }       
        return logdata

    def __supervise__(self):
        logging.debug("Supervision running... (Needs to be implemented)")    
    

# Entry Point     
if __name__ == "__main__":

    from mypvdevices.DeviceAcThor import DeviceAcThor
    from DcsConnection import DcsConnection

    logging.basicConfig(format='%(asctime)s %(levelname)s[%(threadName)s:%(module)s|%(funcName)s]: %(message)s', level=logging.DEBUG)

    serial = "2001002006100016"
    serial_fake = "2001005006100000"
    correctip = "192.168.92.29"

    #device connection tests
    dcsserial = "120100200505tes1"
    cryptoKey = "41424142414241424142414241424142"
    server = "my-pv.live"

    # device.sethost(correctip)
    
    # try to read from valid device
    device = DeviceAcThor(serial)
    device.sethost(correctip)
    try:
        device.__readallregisters__()
        if(len(device.__registers__) == 81):
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
        value = device.getdataset("power")
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
        value = device.getlogvalue("power")
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

    key = "ww1_max"
    targetValue = 50
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
            register = device.readregister(1015)
            if register > 0 and register < 900: 
                print(color('SUCCESS: reading register.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading register. Value missmatch: ' + str(register), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading register. Error: ' + str(e), fore='red', style='bright'))

    if(device != None):
        try:
            registers = device.readregisters(1000, 10)
            if registers[1001] !=  0 and registers[1006] != 0:
                print(color('SUCCESS: reading registers.', fore='green', style='bright'))
            else:
                print(color('ERROR: reading registers. Value missmatch: ' + str(registers), fore='red', style='bright'))
        except Exception as e:
            print(color('ERROR: reading registers. Error: ' + str(e), fore='red', style='bright'))


    # input("Press ENTER to start running tests")
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceAcThor(serial)
    device.sethost(correctip)
    connection = DcsConnection(dcsserial, cryptoKey, server, 50333)
    device.addconnection(connection)
    device.start()

    try:
        while True:
            print(color('[DeviceAcThor] test active. Press CTRL+C to stop', fore='blue', style='bright'))
            device.showinfo()
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            device.__supervise__()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DeviceAcThor] Stopping Test...")
        device.stop()

    input("Press ENTER to start communication tests")

    #DCS communication tests
    logging.getLogger().setLevel(logging.INFO)
    device = DeviceAcThor(serial)
    device.sethost(correctip)
    connection = DcsConnection(dcsserial, cryptoKey, server, 50333)
    device.addconnection(connection)
    # device.setLogDataSendInterval(5)

    # device2 = DeviceAcThor(serial2, 2)
    # connection2 = DcsConnection(serial2, cryptoKey2, server, 50333)
    # device2.addconnection(connection2)

    # device3 = DeviceAcThor(serial3, 7)
    # connection3 = DcsConnection(serial3, cryptoKey3, server, 50333)
    # device3.addconnection(connection3)

    device.start()
    # device2.start()
    # device3.start()
    try:
        while True:
            print(color('[DeviceAcThor] DCS communication active. Press CTRL+C to stop', fore='blue', style='bright'))
            # device.showInfo()
            device.showcommunicationerrors()
            device.showcommunicationerrorsrate()
            # device2.showcommunicationerrors()
            # device2.showcommunicationerrorsrate()
            # device3.showcommunicationerrors()
            # device3.showcommunicationerrorsrate()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("[DCS-Connection] Stopping Test...")
        device.stop()
        # device2.stop()
        # device3.stop()
    input("waiting...")