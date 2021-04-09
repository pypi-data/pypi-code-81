import serial
import serial.tools.list_ports
import struct
import time
import os
import platform
import logging
from typing import List, Tuple, Union, Dict, Any
from pathlib import Path

__all__ = [
    "ExceptionPSU",
    "ExceptionTimeout",
    "PsuEA",
]

# Telegram Header
SEND = 0xC0 + 0x20 + 0x10
RECEIVE = 0x40 + 0x20 + 0x10

STANDARD_HEADER = [SEND + 1, 0x0, 0x36]
#            Header  Output Obj  Mask   Command
REMOTE_MSG = STANDARD_HEADER + [0x10, 0x10]
OUTPUT_MSG = STANDARD_HEADER + [0x01, 0x01]

TRACKING_ON = STANDARD_HEADER + [0xF0, 0xF0]
TRACKING_OFF = STANDARD_HEADER + [0xF0, 0xE0]

ACKNOWLEDGE_ALARM = STANDARD_HEADER + [0x0A, 0x0A]

ERR_STRINGS = {
    0x0:  'NO ERROR',

    # Communication Error
    0x3:  'CHECKSUM WRONG',
    0x4:  'STARTDELIMITER WRONG',
    0x5:  'WRONG OUTPUT',
    0x7:  'OBJECT UNDEFINED',

    # User Error
    0x8:  'OBJECT LENGTH INCORRECT',
    0x9:  'NO RW ACCESS',
    0xf:  'DEVICE IN LOCK STATE',
    0x30: 'UPPER LIMIT OF OBJECT EXCEEDED',
    0x31: 'LOWER LIMIT OF OBJECT EXCEEDED'
}

OBJ_DEV_TYPE = 0x0
OBJ_SERIAL = 0x1
OBJ_NOM_U = 0x2
OBJ_NOM_I = 0x3
OBJ_NOM_P = 0x4
OBJ_DEV_CLASS = 0x13
OBJ_OVP_THRESHOLD = 0x26
OBJ_OCP_THRESHOLD = 0x27
OBJ_SET_U = 0x32
OBJ_SET_I = 0x33
OBJ_STATUS = 0x47


class ExceptionPSU(Exception):
    pass


class ExceptionTimeout(Exception):
    pass


class PsuEA:
    OUTPUT_1 = 0x0
    OUTPUT_2 = 0x1

    CV = 0x0
    CC = 0x2

    OUTPUT_OFF = 0b01
    REMOTE_OFF = 0b10

    PSU_DEVICE_LIST: Dict[str, Tuple[str]] = {
        "Linux":   (
            "ea-ps-2",
            "usb-EA_Elektro-Automatik",
        ),
        "Windows": (
            'PS 2000 B',
        ),
    }

    DEVICE_CLASS_SINGLE = 0x10
    DEVICE_CLASS_TRIPLE = 0x18

    PATH_DEV = '/dev'
    PATH_SERIAL = '/dev/serial/by-id'

    def __init__(self, comport: str = None, sn: str = None, desi: str = None, baudrate: int = 115200, log: bool = False, debug: bool = False):
        """
        :brief: Class to control PSUs from Elektro Automatik
                Tested with: EA PS 2042 - 06B,
                             EA PS 2342 - 10B
        :param comport: Linux: ttyUSBx or ttyACMx
                        Windows: COMx
        :type comport: str
        :param sn:  Serial number of PSU.
        :type sn: str
        :param desi: Designator of PSU.
        :type desi: str
        :param baudrate: Should stay to this value. Not changeable on PSU
        :type baudrate: int

        """

        ch_console = logging.StreamHandler()
        if debug:
            logger_level = logging.DEBUG
        else:
            logger_level = logging.INFO
        log_handler = [ch_console]
        logging.basicConfig(format='[%(levelname)s] %(asctime)s.%(msecs)03d - L%(lineno)d > %(message)s',
                            datefmt="%H:%M:%S", level=logger_level, handlers=log_handler)
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = log or debug
        self.logger.info("LOG MODE")
        self.logger.debug("DEBUG MODE")

        self._port = None
        self._baud = baudrate

        self.psu = None

        self.desc = {'name':                 '-',
                     'serial':               '-',
                     'controllable_outputs': 1
                     }

        _d_state = {'output':           self.OUTPUT_1,
                    'remote on':        False,
                    'output on':        False,
                    'controller state': 'CV',
                    'tracking active':  False,
                    'OVP active':       False,
                    'OCP active':       False,
                    'OPP active':       False,
                    'OTP active':       False,
                    'act voltage':      0.0,
                    'act current':      0.0
                    }

        self.__output_state: List[Dict] = [_d_state, _d_state.copy()]
        self.__output_state[self.OUTPUT_2]['output'] = self.OUTPUT_2

        self.__nom_voltage: float = 0.0
        self.__nom_current: float = 0.0
        self.__nom_power: float = 0.0
        self.__act_voltage: float = 0.0
        self.__max_current: float = 0.0

        self.__find_devices(comport, sn, desi)

        if self._port:
            self.get_status()

    def __del__(self):
        self.close()

    @staticmethod
    def __error_handling(res: int) -> Union[str, int]:
        """
        Error handling
        :param res: response number
        :type res: int
        :return: Error string
        :rtype: string or int
        """
        if ERR_STRINGS[res] != 'NO ERROR':
            return 'Error: ' + ERR_STRINGS[res]
        else:
            return res

    @staticmethod
    def __save_devices(dev_dict: dict, path: str, device_ids: Tuple[str]):
        """
        Save all found PSUs and group them by symlink target.
        Parameters
        ----------
        dev_dict : dict
            Device dictionary
        path : str
            Path to /dev or /dev/serial
        device_ids : tuple
            Device iDs by system (Linux, Windows)

        Returns
        -------

        """
        for dev in os.listdir(path):
            if not any(dev.startswith(id_) for id_ in device_ids):
                continue

            complete_path = os.path.join(path, dev)
            resovled_path = str(Path(complete_path).resolve())

            if not dev_dict.get(resovled_path):
                dev_dict[resovled_path] = [complete_path]
            else:
                dev_dict[resovled_path].append(complete_path)

    def __find_devices(self, comport: str, sn: str, desi: str):
        """
        Find device and connect to them or list a help string.
        :param comport: Comport
        :type comport: string
        :param sn: serial number of PSU
        :type sn: string
        :param desi: Designator of PSU
        :type desi: string
        """
        found = {}
        _dev = None
        system = platform.system()
        device_ids = self.PSU_DEVICE_LIST[system]
        devs = {}

        # Get Device list
        if system == 'Linux':
            self.__save_devices(devs, self.PATH_DEV, device_ids)
            if os.path.isdir(self.PATH_SERIAL):
                self.__save_devices(devs, self.PATH_SERIAL, device_ids)

        elif system == 'Windows':
            dev_list = serial.tools.list_ports.comports()
            devs.fromkeys(list(filter(lambda d: any(id_ in d for id_ in device_ids), dev_list)))
        else:
            raise ExceptionPSU("Not supported system architecture")

        # If comport is none, search all compatible PSUs.
        if comport is None:
            for dev in devs.keys():
                self.close()
                self.logger.debug("Found device at port {}".format(dev))
                self._port = dev
                desc = self.connect()
                desc['port'] = self._port

                # If list contains one device and no Sn or designator are specified, take this device
                if not sn and not desi and len(devs.keys()) == 1:
                    self.logger.debug("Take device {}".format(desc))
                    return

                # If SN or designator is specified and in the device list, take this device.
                if sn == desc['serial'] or desi == desc['name']:
                    self.logger.debug("Found corresponding device {}".format(desc))
                    return
                else:
                    # Collect found devices
                    if not desc["serial"] in found.keys():
                        found[desc["serial"]] = desc

            # Create help output
            if len(found) > 1:
                help_str = [' Found these PSUs:']
                for psu in found.values():
                    _outputs = psu['controllable_outputs']
                    _help = '{}) {} (SN: {}, Output{}: {}), Port: {}'.format(
                        len(help_str),
                        psu['name'],
                        psu['serial'],
                        "s" if _outputs > 1 else "",
                        _outputs,
                        [os.path.basename(p) for p in devs[psu['port']]]
                    )

                    help_str.append(_help)
                help_str = '\n'.join(help_str)
                self.close()

                if sn or desi:
                    raise ExceptionPSU('ERROR: No PSU with {} "{}" found.{}'.format('S/N' if sn else 'designator',
                                                                                    sn if sn else desi, help_str))
                raise ExceptionPSU('No PSU specified.{}'.format(help_str))
            elif len(found) == 1:
                return
            else:
                raise ExceptionPSU('ERROR: No PSU found')

        else:
            p = None
            if system == 'Linux':
                p_list = list(filter(lambda port: os.path.basename(comport) in [os.path.basename(p) for p in port], devs.values()))
                if p_list:
                    p = p_list[0]
            elif system == 'Windows':
                p = list(filter(lambda port: comport in port.description, devs.keys()))

            if not p:
                raise ExceptionPSU('ERROR: No PSU at port "{}" found.'.format(comport))

            self._port = p[0]
            self.connect()

    @staticmethod
    def __pack_list(_list: List[int]) -> bytes:
        """
        Pack list of bytes to bytestring
        :param _list: list of bytes
        :type _list: list
        :return: bytes
        :rtype: bytes
        """
        return struct.pack(f'{len(_list)}B', *_list)

    @staticmethod
    def __int_to_bytes(num: int, num_bytes: int) -> List[int]:
        """
        Convert int to bytes
        :param num: Value to convert
        :type num: int
        :param num_bytes: Amount of requested bytes
        :type num_bytes: int
        :return: list of bytes
        :rtype: list
        """
        _list = [8 * i for i in reversed(range(num_bytes))]
        return [(num >> i & 0xff) for i in _list]

    def __calc_checksum(self, cmd_list: List[int]) -> List[int]:
        """

        :param cmd_list:
        :type cmd_list:
        :return:
        :rtype:
        """
        checksum = 0
        for byte in cmd_list:
            checksum += byte
        return self.__int_to_bytes(checksum, 2)

    @staticmethod
    def __get_response(package: List[int]) -> List[int]:
        """
        Get response
        :param package: received message list
        :type package: list
        :return: sub list
        :rtype: list
        """
        return package[3:-2]

    def __tx_rx(self, cmd: List[int], expect_length: int) -> List[int]:
        """
        Send and receive message from device
        :param cmd: cmd list
        :type cmd: list
        :param expect_length:
        :type expect_length:
        :return: Response
        :rtype: bytes
        """
        if self.psu:
            checksum = self.__calc_checksum(cmd)
            output = self.__pack_list(cmd + checksum)
            self.psu.write(output)
            time.sleep(0.005)
            num = 0
            t0 = time.time()
            while num < (expect_length + 5):
                num = self.psu.inWaiting()
                if time.time() - t0 > 1:
                    raise ExceptionTimeout('Didn\'t receive %d bytes in time.' % (expect_length + 5))
            res = self.__get_response(self.psu.read(num))
            time.sleep(0.04)
            return res
        raise ExceptionPSU('No PSU connected')

    def _check_outputs(self, output_num: int):
        """
        Check, if requested output number is in range of actual available outputs.
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :raise ExceptionPSU, if device has only one output
        """
        existing_outputs = self.desc['controllable_outputs']
        if output_num > 0 and output_num >= existing_outputs:
            raise ExceptionPSU('Error: PSU has only {} output{}.'.format(existing_outputs,
                                                                         's' if existing_outputs > 1 else ''))
        elif self.__output_state[output_num]["tracking active"] and output_num > 0:
            raise ExceptionPSU('Error: Tracking is active. Second output is not controllable!')

    def __set_value(self, value: Union[int, float], max_value: Union[int, float], obj_num: int, output: int):
        """
        Set value on device
        :param value: voltage or current value
        :type value: int or float
        :param max_value: Max value (nominal value)
        :type max_value: int or float
        :param obj_num: object index
        :type obj_num: int
        :param output: Output number for multi output devices (e.g. PS 2342-10B)
        :type output: int
        """
        self._check_outputs(output)

        if not self.__output_state[output]['remote on']:
            self.remote_on(output)

        if max_value == 0.0:
            raise ExceptionPSU('Error: "Max Value" in "set_value()" is zero.')

        value_percent = int((value * 25600.0) / max_value)
        value_bytes = self.__int_to_bytes(value_percent, 2)
        packet = [SEND + len(value_bytes) - 1, output, obj_num] + value_bytes
        error = struct.unpack('B', self.__tx_rx(packet, 1))[0]
        if error != 0x0:
            raise ExceptionPSU(ERR_STRINGS[error])

    def __get_value(self, obj: int, exp_len: int, pattern: str, output: int) -> Union[List[int], Tuple[Any]]:
        """
        Get int value
        :param obj: object index
        :type obj: int
        :param exp_len: Expected message length in byte
        :type exp_len: int
        :param pattern: struct pattern string
        :type pattern: str
        :param output: Output number for multi output devices (e.g. PS 2342-10B)
        :type output: int
        :return: response list
        :rtype: Union[List[int], Tuple[Any]]
        """
        self._check_outputs(output)

        if not self.__output_state[output]['remote on']:
            self.remote_on(output)

        packet = [RECEIVE, output, obj]
        res = self.__tx_rx(packet, exp_len)

        if pattern == 's':
            return res
        return struct.unpack(pattern, res)

    def __get_float(self, obj: int, output: int) -> Tuple[Any]:
        """
        Get Float value from device
        :param obj: object index
        :type obj: int
        :param output: Output number for multi output devices (e.g. PS 2342-10B)
        :type output: int
        :return: values from device
        :rtype: Tuple[Any]
        """
        self._check_outputs(output)

        packet = [RECEIVE, output, obj]
        res = self.__tx_rx(packet, 4)
        return struct.unpack('>f', res)

    @staticmethod
    def _calculate_value(value: Union[int, float], nom_value: Union[int, float]) -> float:
        """
        Calculate the voltage or current coming from device.
        :param value: value from device
        :type value: int
        :param nom_value: nominal value
        :type nom_value: int or float
        :return: Actual voltage/current
        :rtype: float
        """
        return round((value * nom_value) / 25600.0, 3)

    def _init_device(self, output_num: int = 0):
        """
        Init device
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        """
        self.get_nominal_values(output_num, True)
        self.set_ovp(self.__nom_voltage, output_num)
        self.set_ocp(self.__nom_current, output_num)

    def connect(self, comport: str = None) -> Dict[str, Union[str, int]]:
        """
        :brief Connect with PSU
        :param comport: COM port name
        :type comport: str
        :return: Device Description
        :rtype: Dict[str, Union[str, int]]
        """
        port = ''
        if platform.system() == 'Windows':
            port = comport or self._port.device
        elif platform.system() == 'Linux':
            port = comport or self._port
        self.psu = serial.Serial(port, self._baud, timeout=5)
        return self.get_device_description(True)

    def close(self):
        """
        :brief Closes the serial connection.
        """
        if self.psu:
            for output in range(self.desc['controllable_outputs']):
                if output > self.OUTPUT_1 and self.__output_state[output]['tracking active']:
                    continue
                self.remote_off(output)

            self.psu.close()
        self.psu = None
        self._port = None

    def get_status(self, update: bool = True) -> List[Dict]:
        """
        :brief: Get status from device. See programming Guide for further information page 11
        :param update: If True, update state dictionary from device
        :param update: bool
        :return: Dictionary with current states.
        :rtype: dict
        """
        if update:
            outputs = self.desc['controllable_outputs']
            self.logger.debug("get_status(), Controllable outputs: {}".format(outputs))
            output_state = []
            status = list()
            for output_num in range(outputs):
                output_state.append({})
                # if tracking active and this is the second output, skip getting value and use status from first output.
                if output_num == self.OUTPUT_2 and output_state[0]['tracking active']:
                    self.logger.debug("Tracking is active")
                else:
                    status = self.__get_value(OBJ_STATUS, 6, '>BBHH', output_num)

                remote_on = status[0]
                status_byte = status[1]
                output_state[output_num]['remote on'] = remote_on == 1
                output_state[output_num]['output on'] = (status_byte & 0x1) == 1
                output_state[output_num]['controller state'] = 'CV' if (status_byte >> 1) & 0x3 == self.CV else 'CC'
                output_state[output_num]['tracking active'] = ((status_byte >> 3) & 0x1) == 1
                output_state[output_num]['OVP active'] = ((status_byte >> 4) & 0x1) == 1
                output_state[output_num]['OCP active'] = ((status_byte >> 5) & 0x1) == 1
                output_state[output_num]['OPP active'] = ((status_byte >> 6) & 0x1) == 1
                output_state[output_num]['OTP active'] = ((status_byte >> 7) & 0x1) == 1
                output_state[output_num]['act voltage'] = self._calculate_value(status[2], self.__nom_voltage)
                output_state[output_num]['act current'] = self._calculate_value(status[3], self.__nom_current)
            self.__output_state = output_state
        return self.__output_state

    def get_device_description(self, update: bool = False) -> Dict[str, Union[str, int]]:
        """
        :brief Get device name
        :return: Device name
        :rtype: Dict[str, Union[str, int]]
        """
        self.logger.debug("get_device_description()")
        if self.desc['name'] == '-' or update:
            self.logger.debug("get_device_description(): Update")
            self.desc['name'] = self.__get_value(OBJ_DEV_TYPE, 12, 's', 0)[:-1].decode('ascii')
            self.desc['serial'] = self.__get_value(OBJ_SERIAL, 11, 's', 0)[:-1].decode('ascii')
            self.desc['controllable_outputs'] = 1 if self.__get_value(OBJ_DEV_CLASS, 2, '>BB', 0)[1] == self.DEVICE_CLASS_SINGLE else 2
        return self.desc.copy()

    def __send_msg(self, msg: List[int], state_name: str = None):
        """
        Send message to PSU and throw error if a problem occurs.
        Parameters
        ----------
        msg : List[int]
            Telegram message for PSU
        state_name : str
            State name in dict to set the new value there.

        Raises
        ------
            ExceptionPSU: If error is not null
            ExceptionPSU: If sending message failed 5 times
        """
        counter = 5

        output_num = msg[1]
        value = msg[4]

        while True:
            res = self.__tx_rx(msg, 1)
            if len(res) == 1:
                error = struct.unpack('B', res)[0]
                if error != 0x0:
                    raise ExceptionPSU(ERR_STRINGS[error])
                else:
                    if state_name:
                        self.__output_state[output_num][state_name] = bool(value)
                    break

            if counter == 0:
                raise ExceptionPSU(f'ERROR: Did not received ACK for {state_name.upper()}: {value}')

            counter -= 1

    def _send_remote(self, value: int, output_num: int, init: bool):
        """
        Send remote message (on/off)
        :param value: 1 or 0 (on or off)
        :type value: int
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :param init: Init device first (only for remote_on())
        :type init: bool

        """
        self.logger.debug("send_remote({})".format(output_num))

        self._check_outputs(output_num)

        REMOTE_MSG[1] = output_num
        REMOTE_MSG[4] = value

        self.__send_msg(REMOTE_MSG, 'remote on')

        if init:
            self._init_device(output_num)

    def _send_output(self, value: int, output_num: int):
        """
        :brief Turn on or off power output on device
        :param value: 1 or 0 (On or Off)
        :type value: int
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: Device return message/ack
        :rtype: byte str
        """
        self._check_outputs(output_num)

        OUTPUT_MSG[1] = output_num
        OUTPUT_MSG[4] = value

        self.__send_msg(OUTPUT_MSG, 'output on')

    def remote_on(self, output_num: int = 0, init: bool = True):
        """
        :brief Activates remote mode on device
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :param init: if True, initialize the output.
        :type init: bool
        :return: Device return message/ack
        :rtype: byte str
        """
        self._send_remote(0x10, output_num, init)

    def remote_off(self, output_num: int = 0):
        """
        :brief Deactivates remote mode on device
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: Device return message/ack
        :rtype: byte str
        """
        if not self.__output_state[output_num]["remote on"]:
            self.logger.debug("Remote already off")
            return
        self._send_remote(0x00, output_num, False)

    def get_nominal_voltage(self, output_num: int = 0, update: bool = False) -> float:
        """
        Get nominal voltage from device.

        Parameters
        ----------
        output_num : int
            Output index
        update : bool
            Update nom. values. If true, get it from PSU. Otherwise use cached value.

        Returns
        -------
        float
            Nominal voltage
        """

        if not self.__nom_voltage or update:
            self.__nom_voltage = self.__get_float(OBJ_NOM_U, output_num)[0]
            self.logger.debug(f"Get from PSU nom voltage: {self.__nom_voltage}")
        return self.__nom_voltage

    def get_nominal_current(self, output_num: int = 0, update: bool = False) -> float:
        """
        Get nominal current from device.

        Parameters
        ----------
        output_num : int
            Output index
        update : bool
            Update nom. values. If true, get it from PSU. Otherwise use cached value.

        Returns
        -------
        float
            Nominal current
        """
        if not self.__nom_current or update:
            self.__nom_current = self.__get_float(OBJ_NOM_I, output_num)[0]
            self.logger.debug(f"Get from PSU nom current: {self.__nom_current}")
        return self.__nom_current

    def get_nominal_power(self, output_num: int = 0, update: bool = False) -> float:
        """
        Get nominal power from device.

        Parameters
        ----------
        output_num : int
            Output index
        update : bool
            Update nom. values. If true, get it from PSU. Otherwise use cached value.

        Returns
        -------
        float
            Nominal power
        """
        if not self.__nom_power or update:
            self.__nom_power = self.__get_float(OBJ_NOM_P, output_num)[0]
            self.logger.debug(f"Get from PSU nom power: {self.__nom_power}")
        return self.__nom_power

    def get_nominal_values(self, output_num: int = 0, update: bool = False) -> (float, float, float):
        """
        Get nominal voltage, current and power from device.

        Parameters
        ----------
        output_num : int
            Output index
        update : bool
            Update nom. values. If true, get it from PSU. Otherwise use cached value.

        Returns
        -------
        (float, float, float)
            Voltage, Current, Power
        """
        self.get_nominal_voltage(output_num, update)
        self.get_nominal_current(output_num, update)
        self.get_nominal_power(output_num, update)
        self.logger.debug(f"Nom Values: U: {self.__nom_voltage}, I: {self.__nom_current}, P: {self.__nom_power}")
        return self.__nom_voltage, self.__nom_current, self.__nom_power

    def set_voltage(self, voltage: Union[int, float], output_num: int = 0) -> float:
        """
        :brief: Set output voltage on device
        :param voltage: desired output voltage in V
        :type voltage: int/float
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: Device return message
        :rtype: byte str
        """
        # Calculate actual possible maximum current depending on maximum output power
        set_voltage = voltage
        if set_voltage > self.__nom_voltage:
            set_voltage = self.__nom_voltage
        try:
            if set_voltage > self.__nom_power / self.__max_current:
                set_voltage = self.__nom_power / self.__max_current
                self.logger.info('Set voltage to {:.2f} V due to maximum power of {:.2f} W'.format(set_voltage, self.__nom_power))
        except ZeroDivisionError:
            pass

        self.__act_voltage = float(set_voltage)
        self.__set_value(set_voltage, self.__nom_voltage, OBJ_SET_U, output_num)
        return self.__act_voltage

    def set_current(self, current: Union[int, float], output_num: int = 0) -> float:
        """
        :brief: Set maximum output current on device
        :param current: desired output current in A
        :type current: int/float
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: Device return message
        :rtype: byte str
        """
        # Calculate actual possible maximum current depending on maximum output power
        set_current = current
        if set_current > self.__nom_current:
            set_current = self.__nom_current
        try:
            if set_current > self.__nom_power / self.__act_voltage:
                set_current = self.__nom_power / self.__act_voltage
                self.logger.info(f'Set current to {set_current:.2f} A due to maximum power of {self.__nom_power:.2f} W and current voltage of {self.__act_voltage:.2f} V')
        except ZeroDivisionError:
            pass

        self.__max_current = float(set_current)
        self.__set_value(set_current, self.__nom_current, OBJ_SET_I, output_num)
        return self.__max_current

    def get_voltage(self, output_num: int = 0) -> float:
        """
        :brief: Get current output voltage from device
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: Voltage in V
        :rtype: float
        """
        self._check_outputs(output_num)

        if self.__nom_voltage <= 0.0:
            self.get_nominal_voltage(output_num)

        status = self.get_status()
        if status:
            return status[output_num]['act voltage']
        self.logger.debug("Warning: Status is empty")
        return 0.0

    def get_current(self, output_num: int = 0) -> float:
        """
        :brief: Get current of output_num
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: Current in A
        :rtype: float
        """
        self._check_outputs(output_num)

        if self.__nom_current <= 0.0:
            self.get_nominal_current(output_num)

        status = self.get_status()
        if status:
            return status[output_num]['act current']
        self.logger.debug("Warning: Status is empty")
        return 0.0

    def get_power(self, output_num: int = 0) -> float:
        """
        :brief: Get power of output_num
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: Power in W
        :rtype: float
        """
        self._check_outputs(output_num)

        status = self.get_status()
        return round(status[output_num]['act voltage'] * status[output_num]['act current'], 3)

    def output_on(self, output_num: int = 0):
        """
        :brief Turn on power output on device
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        """
        self._send_output(1, output_num)

    def output_off(self, output_num: int = 0):
        """
        :brief Turn off power output on device
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        """
        self._send_output(0, output_num)

    def set_ovp(self, voltage, output_num: int = 0):
        """
        :brief: Set Over Voltage Protection
        :param voltage: desired OVP voltage
        :type voltage: float/int
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        """
        self.__set_value(voltage, self.__nom_voltage, OBJ_OVP_THRESHOLD, output_num)

    def set_ocp(self, current, output_num: int = 0):
        """
        :brief: Set Over Current Protection
        :param current: desired OCP current
        :type current: float/int
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        """
        self.__set_value(current, self.__nom_current, OBJ_OCP_THRESHOLD, output_num)

    def get_ovp(self, output_num: int = 0) -> float:
        """
        :brief: Get Over Voltage Protection value
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: OVP value
        :rtype: float
        """
        val = self.__get_value(OBJ_OVP_THRESHOLD, 2, '>H', output_num)
        return self._calculate_value(val[0], self.__nom_voltage)

    def get_ocp(self, output_num: int = 0) -> float:
        """
        :brief: Get Over Current Protection value
        :param output_num: Output number for multi output devices (e.g. PS 2342-10B)
        :type output_num: int
        :return: OCP value
        :rtype: float
        """
        val = self.__get_value(OBJ_OCP_THRESHOLD, 2, '>H', output_num)
        return self._calculate_value(val[0], self.__nom_current)

    def reset_error(self, output_num: int = 0):
        """
        Reset error (OVP, OCP, OPP, OTP).
        Resetting error turns off all outputs.

        Parameters
        ----------
        output_num : int
            Output index
        """

        ACKNOWLEDGE_ALARM[1] = output_num
        self.__send_msg(ACKNOWLEDGE_ALARM)

    def tracking_on(self):
        """
        Turn tracking on. If tracking is on, output 2 control is disable and output 1 controls also output 2

        Raises
        ------
            ExceptionPSU: If user tries to turn on tracking on single output PSU.
        """
        if self.desc["controllable_outputs"] == 1:
            raise ExceptionPSU("Tracking is only available on Triple Output PSUs")

        self.__send_msg(TRACKING_ON)
        # Set status manual, because we have to do it for both outputs
        for o in range(self.desc["controllable_outputs"]):
            self.__output_state[o]["tracking active"] = True

    def tracking_off(self):
        """
        Turn tracking off.
        """
        self.__send_msg(TRACKING_OFF)
        # Set status manual, because we have to do it for both outputs
        for o in range(self.desc["controllable_outputs"]):
            self.__output_state[o]["tracking active"] = False
