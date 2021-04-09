"""
    Collection of useful functions and wrapper for the Labjacks T4 and T7
"""
import logging
import math
import os
import time
from typing import List, Tuple, Union, Dict

import numpy as np

__all__ = [
    "ExceptionDAQ",
    "ExceptionNoAcknowledgement",
    "DAQLabJack",
]

logger = logging.getLogger(__file__)

try:
    from labjack import ljm
except Exception as exc:
    logger.warning(str(exc))

LIB_PATH = '/usr/local/lib'


class ExceptionDAQ(Exception):
    def __init__(self, msg):
        logger.error(msg)


class ExceptionNoAcknowledgement(ExceptionDAQ):
    pass


class ExceptionUART(ExceptionDAQ):
    pass


# Need to be defined outside, because used as argument default values
_POSITIVE_EDGES: int = 3
_ONE_SHOT: int = 0


class DAQLabJack:
    TRIG_FALLING: int = 0
    TRIG_RISING: int = 1

    POSITIVE_EDGES: int = _POSITIVE_EDGES
    NEGATIVE_EDGES: int = 4

    ONE_SHOT: int = _ONE_SHOT
    CONTINUOUS: int = 1

    DIO_NAME_MAP: Dict[str, str] = {
        'FIO0':  'DIO0',
        'FIO1':  'DIO1',
        'FIO2':  'DIO2',
        'FIO3':  'DIO3',
        'FIO4':  'DIO4',
        'FIO5':  'DIO5',
        'FIO6':  'DIO6',
        'FIO7':  'DIO7',
        'EIO0':  'DIO8',
        'EIO1':  'DIO9',
        'EIO2':  'DIO10',
        'EIO3':  'DIO11',
        'EIO4':  'DIO12',
        'EIO5':  'DIO13',
        'EIO6':  'DIO14',
        'EIO7':  'DIO15',
        'CIO0':  'DIO16',
        'CIO1':  'DIO17',
        'CIO2':  'DIO18',
        'CIO3':  'DIO19',
        'MIO0':  'DIO20',
        'MIO1':  'DIO21',
        'MIO2':  'DIO22',
        "AIN0":  'AIN0',
        "AIN1":  'AIN1',
        "AIN2":  'AIN2',
        "AIN3":  'AIN3',
        "AIN4":  'AIN4',
        "AIN5":  'AIN5',
        "AIN6":  'AIN6',
        "AIN7":  'AIN7',
        "AIN8":  'AIN8',
        "AIN9":  'AIN9',
        "AIN10": 'AIN10',
        "AIN11": 'AIN11',
        "AIN12": 'AIN12',
        "AIN13": 'AIN13',
        "DAC0":  'DAC0',
        "DAC1":  'DAC1',
    }

    # Pins that can sample frequency
    PINS_FREQUENCY_IN: Dict[str, Tuple[str]] = {
        'T7': ('DIO0', 'DIO1'),
        'T4': ('DIO4', 'DIO5'),
    }
    PINS_PULSE_OUT: Dict[str, Tuple[str]] = {
        'T7': ('DIO0', 'DIO2', 'DIO3', 'DIO4', 'DIO5'),
        'T4': ('DIO6', 'DIO7'),
    }

    MAX_SCAN_RATE: Dict[str, int] = {
        'T4': 59880,
        'T7': 100000,
    }

    PRECISION: int = 6

    CORE_FREQ: int = 80e6

    list_types: Tuple[Union[list, tuple]] = (list, tuple)

    UART_INIT_REGISTER = (
        'ASYNCH_ENABLE',  # Deactivate Uart and configure it
        'ASYNCH_TX_DIONUM',
        'ASYNCH_RX_DIONUM',
        'ASYNCH_BAUD',
        'ASYNCH_RX_BUFFER_SIZE_BYTES',
        'ASYNCH_NUM_DATA_BITS',
        'ASYNCH_NUM_STOP_BITS',
        'ASYNCH_PARITY',
        'ASYNCH_ENABLE'
    )

    UART_INIT_VALUE = [0, 0, 1, 9600, 20, 8, 1, 0, 1]

    def __init__(self, device: str = 'ANY', connection_type: str = 'ANY', id: str = 'ANY', handle: int = None, log: bool = False, debug: bool = False):
        """
        Creates a DAQ object and connects to the corresponding labjack.

        Parameters
        ----------
        device : str
            Device Type. "T4", "T7" or "ANY"
        connection_type : str
            Can be: "ANY", "USB", "TCP", "ETHERNET", and "WIFI".
        id : str
            This can be a serial number, IP address, "ANY"
            or device name
        handle : int
            Device handle. If a handle is used, device, connection_type and id are not needed.
        log : bool
            Show logging output
        debug : bool
            Show also debug output.
        """
        if not any([file.startswith('libLabJackM') for file in os.listdir(LIB_PATH)]):
            logger.error("DAQLabJack: Labjack library 'libLabJackM' is not installed.")
            return

        # add DIO strings as attributes
        for key, name in self.DIO_NAME_MAP.items():
            setattr(self, key, name)

        if log or debug:
            logging.basicConfig(format='[%(levelname)s] (%(asctime)s.%(msecs)03d) {%(module)s:%(lineno)d}> %(message)s')
            logger.setLevel(logging.INFO)
            if debug:
                logger.setLevel(logging.DEBUG)

        self._id = id
        self._conn = connection_type
        self._device = device
        self._handle = None
        self._clock1_enabled = False
        self._clock2_enabled = False

        self.connect(device, connection_type, id, handle)

    def __str__(self) -> str:
        """
        String representation.

        Returns
        -------
        str
        """

        return f'LJ-{self._device}-{self._id}'

    def connect(self, device: str, connection_type: str, id: str, handle: int = None):
        """
        Connects to Labjack.

        Parameters
        ----------
        device : str
            Device Type. "T4", "T7" or "ANY"
        connection_type : str
            Can be: "ANY", "USB", "TCP", "ETHERNET", and "WIFI".
        id : str
            This can be a serial number, IP address, "ANY"
            or device name
        handle : int
            Device handle. If a handle is used, device, connection_type and id are not needed.
        """
        if handle is not None:
            self._handle = handle
        else:
            self._handle = ljm.openS(device, connection_type, id)

    def close(self):
        """
        Close Labjack connection.
        """
        if self._handle is not None:
            ljm.close(self._handle)

    def scan(self, connection_type: str = None) -> Tuple:
        """
        Scan for available Labjacks.
        Parameters
        ----------
        connection_type : str
            Can be: "ANY", "USB", "TCP", "ETHERNET", and "WIFI".

        Returns
        -------
        A tuple containing:
        (numFound, aDeviceTypes, aConnectionTypes, aSerialNumbers,
         aIPAddresses)

        numFound: Number of devices found.
        aDeviceTypes: List of device types for each of the numFound
            devices.
        aConnectionTypes: List of connection types for each of the
            numFound devices.
        aSerialNumbers: List of serial numbers for each of the numFound
            devices.
        aIPAddresses: List of IP addresses for each of the numFound
            devices, but only if the connection type is TCP-based. For
            each corresponding device for which aIPAddresses[i] is not
            TCP-based, aIPAddresses[i] will be
            labjack.ljm.constants.NO_IP_ADDRESS.
        """
        return ljm.listAllS(self._device, connection_type or self._conn)

    def write(self, ports: Union[List[str], Tuple[str], List[Tuple[str, int]], str],
              values: Union[List[Union[int, float]], Tuple[Union[int, float]], int, float] = None):
        """
        Write to one or multiple ports
        Parameters
        ----------
        ports : List, Tuple, str
            Port name(s). Can also be a list of tuples with port name and value. E.g: [("DIO1", 1),..]
            Argument values shall be None then.
        values : List, Tuple, int, float
            Values to write

        Raises
        ------
            ExceptionDAQ: If ports and values have not the same length

        """
        if isinstance(ports, self.list_types) and isinstance(ports[0], self.list_types):
            ljm.eWriteNames(self._handle, len(ports), [c[0] for c in ports], [c[1] for c in ports])

        elif isinstance(ports, self.list_types) and isinstance(values, self.list_types):
            if len(ports) != len(values):
                raise ExceptionDAQ('Amount of names and values are not the same')

            ljm.eWriteNames(self._handle, len(ports), ports, values)
        else:
            ljm.eWriteName(self._handle, ports, values)

    def read(self, ports: Union[str, List[str], Tuple[str]]) -> Union[List[Union[int, float]], int, float]:
        """
        Read one port or many.
        Parameters
        ----------
        ports : Union[str, List[str], Tuple[str]])

        Returns
        -------
        Union[List[Union[int,float]], int, float]
            Read values.

        """
        if isinstance(ports, self.list_types):
            return ljm.eReadNames(self._handle, len(ports), ports)
        else:
            return ljm.eReadName(self._handle, ports)

    def __calc_divisor_rollvalue(self, frequency: Union[float, int]) -> (int, int):
        """
        Calculate the frequency divisor and roll value.

        Parameters
        ----------
        frequency :  Union[float, int]
            Requested frequency

        Returns
        -------
        (int, int)
            Divisor and roll value
        """
        # divisor could only take the following values: 1,2,4,8,16,32,64,256
        divisor = 2 ** math.ceil(math.log(math.ceil(self.CORE_FREQ / (frequency * 65536)), 2))

        if divisor == 128:
            divisor = 256

        roll_value = int(self.CORE_FREQ / (frequency * divisor))

        return divisor, roll_value

    def _config_common_pwm(self, port: str, index: int, divisor: int, roll_value: int, clock_source: int, config_a: Union[int, float], config_b: Union[int, float] = None,
                           config_c: Union[int, float] = None, config_d: Union[int, float] = None):
        """
        Configure the PWM output.

        DutyCycle% = 100 * DIO#_EF_CONFIG_A / DIO_EF_CLOCK#_ROLL_VALUE
        Clock#Frequency = CoreFrequency / DIO_EF_CLOCK#_DIVISOR
        PWMFrequency = Clock#Frequency / DIO_EF_CLOCK#_ROLL_VALUE

        Parameters
        ----------
        port : str
            Port name
        index : int
            Select the extended feature. 0 = basic PWM, 1 = PWM with phases
        divisor : int
            Clock divisor.
        roll_value : int
            PWM frequency equals the roll value.
        clock_source : int
            Selects the clock source. Can be 0, 1, 2.
        config_a : Union[int, float]
            When the clock source's count matches this value the line will transition from high to low.
        config_b : Union[int, float]
            When the clock source's count matches this value the line will transition from low to high. Index need be 1.
        config_c : Union[int, float]
            Not used.
        config_d : Union[int, float]
            Not used.

        Raises
        ------
            ExceptionDAQ: If requested port is not supporting PWM.

        """

        if not self.DIO_NAME_MAP[port] in self.PINS_PULSE_OUT[self._device]:
            raise ExceptionDAQ(f'"{port}/{self.DIO_NAME_MAP[port]}" cannot generate "Pulse Out" on "{self._device}". Use "{self.PINS_PULSE_OUT[self._device]}" instead.')

        # Deactivate all clocks
        config = [
            ("DIO_EF_CLOCK0_ENABLE", 0),
            ("DIO_EF_CLOCK1_ENABLE", 0),
            ("DIO_EF_CLOCK2_ENABLE", 0)
        ]

        self.write(config)

        if clock_source == 0:
            self._clock1_enabled = False
            self._clock2_enabled = False
        if clock_source == 1:
            self._clock1_enabled = True
        if clock_source == 2:
            self._clock2_enabled = True

        # Turn the output port off
        self.write(self.DIO_NAME_MAP[port], 0)

        # Configure the signal to be generated
        _config_name_template = "{}_EF_CONFIG_{}"
        config_register = [(_config_name_template.format(self.DIO_NAME_MAP[port], 'A'), config_a)]

        for name, conf in zip(['B', 'C', 'D'], [config_b, config_c, config_d]):
            if conf is not None:
                config_register.append((_config_name_template.format(self.DIO_NAME_MAP[port], name), conf))

        config = [
            (f"{self.DIO_NAME_MAP[port]}_EF_ENABLE", 0),
            (f"DIO_EF_CLOCK{clock_source}_ENABLE", 0),
            (f"DIO_EF_CLOCK{clock_source}_DIVISOR", divisor),
            (f"DIO_EF_CLOCK{clock_source}_ROLL_VALUE", roll_value),
            *config_register,
            (f"{self.DIO_NAME_MAP[port]}_EF_INDEX", index),
            (f"{self.DIO_NAME_MAP[port]}_EF_OPTIONS", clock_source),
        ]

        self.write(config)

        self.write(self.DIO_NAME_MAP[port], 0)

        # Activate the clock and the signal
        config = []

        if self._clock1_enabled:
            config.append(("DIO_EF_CLOCK1_ENABLE", 1))

        if self._clock2_enabled:
            config.append(("DIO_EF_CLOCK2_ENABLE", 1))

        if not self._clock1_enabled and not self._clock2_enabled:
            config.append(("DIO_EF_CLOCK0_ENABLE", 1))

        config.append((f"{self.DIO_NAME_MAP[port]}_EF_ENABLE", 1))

        self.write(config)

    def _stream_port(self, port: str, num_scans: int = 20, scan_rate: int = 2000) -> np.ndarray:
        """

        Parameters
        ----------
        port :
        num_scans :
        scan_rate :

        Returns
        -------

        """
        """
        Acquire a number of samples from a port and average the return.
        :param port:
        :param num_scans: number of samples to acquire
        :type num_scans: int
        :param scan_rate: sampling frequency in Hz
        :type scan_rate: int
        :return:
        """

        port_address = ljm.nameToAddress(port)[0]  # returns (Address, DataType)
        # self.write("STREAM_RESOLUTION_INDEX", 2)

        # In order to acquire the correct value:
        #    1. shift multiplexer to desired port by reading from it, and ignore
        #    2. introduce delay: wait for input's dynamic response to equalize
        #    3. sample desired port again

        sampled_data_throwaway = self.read(port)
        time.sleep(0.01)  # delay in seconds

        # returns tuple (ScanRate, samples_acquired)
        sampled_data = ljm.streamBurst(self._handle, 1, [port_address], scan_rate, num_scans)[1]

        logger.debug(f"Sampled data: {sampled_data}")
        # Labjack very occasionally returns bogus value, such as -4496.733 or -506.242, etc.
        # their support does not know the reason, this is a workaround SW fix
        mean_value = np.mean(sampled_data)
        if abs(mean_value) > 100:
            sampled_data = ljm.streamBurst(self._handle, 1, [port_address], scan_rate, num_scans)[1]
            logger.debug(f"Sampled data (previous were bogus): {sampled_data}")
            mean_value = np.mean(sampled_data)

        return mean_value

    def read_average_voltage(self, ports: Union[str, List, Tuple], num_scans: int = 20, scan_rate: int = 2000) -> Union[np.ndarray, List[np.ndarray]]:
        """

        Parameters
        ----------
        ports :
        num_scans :
        scan_rate :

        Returns
        -------

        """
        """
        Acquire a number of samples from one or multiple ports and average the return.
        :param ports:
        :param num_scans: number of samples to acquire
        :type num_scans: int
        :param scan_rate: sampling frequency in Hz
        :type scan_rate: int
        :return:
        """
        if isinstance(ports, self.list_types):
            sampled_data_ave = []
            for port in ports:
                sampled_data_ave.append(self._stream_port(port, num_scans, scan_rate))
            return sampled_data_ave
        else:
            return self._stream_port(ports, num_scans, scan_rate)

    def get_frequency_max_min_voltage(self, port: str, voltage_range: float = 10.0, num_scans: int = 6000, scan_rate: int = 100e3) -> (float, float, float):
        """

        Parameters
        ----------
        port :
        voltage_range :
        num_scans :
        scan_rate :

        Returns
        -------

        """
        """
        Sample the analog signal and extract frequency, maximum voltage and minimum voltage.
        :param port: pin name
        :type port: str
        :param voltage_range: voltage range of the analog input (ex. 10 refers to +/-10V input).
                              Supported ranges: 10, 1, 0.1, 0.01
        :type voltage_range: int
        :param num_scans: number of samples to acquire
        :type num_scans: int
        :param scan_rate: sampling frequency in Hz
        :type scan_rate: int
        :return: list [frequency, average max, average min]
        """

        if scan_rate > self.MAX_SCAN_RATE[self._device]:
            scan_rate = self.MAX_SCAN_RATE[self._device]
            logger.warning(f'Scan rate too high. Set it to "{scan_rate}"')

        port_address = ljm.nameToAddress(port)[0]  # returns (Address, DataType)
        self.write('STREAM_BUFFER_SIZE_BYTES', 32768)  # maximum size, default is 4096
        self.write(f'{port}_RANGE', voltage_range)

        cnt = 5
        while True:
            try:
                # returns tuple (ScanRate, samples_acquired)
                sampled_data = ljm.streamBurst(self._handle, 1, [port_address], scan_rate, num_scans)[1]
                break
            except ljm.LJMError as e:
                cnt -= 1
                if cnt == 0:
                    logger.error(e)
                    raise ljm.LJMError('Not able to sample signal')

        # recovering the frequency of the sampled signal
        a = sampled_data
        a = a - np.mean(a)
        sampling_freq_of_dac = scan_rate  # maximum sampling freq=100kHz

        a_f = np.abs(np.real(np.fft.fft(a)))  # performing FFT on the data acquired, saving only real-absolute values
        a_f_trunk = a_f[1:int(len(a) / 2)]  # truncating the mirrored data from FFT

        threshold = np.max(a_f_trunk) - 5  # threshold of where to search for the frequency peaks

        freq_peak_index = np.where(a_f_trunk > threshold)[0]  # boolean comparison, finding indices
        freq_of_sig = round(freq_peak_index[0] / len(a) * sampling_freq_of_dac, self.PRECISION)

        sorted_samples = np.sort(sampled_data)

        range_percent = 5  # percent
        # to avoid bursts or outliers ignore to highest and lowest 1 or whatever percent
        range_ignore_percent = 0.5  # percent

        range_ignore_index = int(range_ignore_percent * len(sorted_samples) / 100)
        range_index = int(range_percent * len(sorted_samples) / 100)

        min_values = sorted_samples[range_ignore_index:range_index]
        max_values = sorted_samples[-range_index:-range_ignore_index]

        # round off the trailing numbers
        max_value = round(float(np.mean(max_values)), self.PRECISION)
        min_value = round(float(np.mean(min_values)), self.PRECISION)

        return freq_of_sig, max_value, min_value

    def get_average_max_min_voltage(self, port: str, num_scans: int = 6000, scan_rate: int = 100e3) -> List[float]:
        """

        Parameters
        ----------
        port :
        num_scans :
        scan_rate :

        Returns
        -------

        """
        """
        Get average, maximum and minimum voltage of an analog signal using build-in functions of Labjack.
        :param port: Analog port
        :type port: str
        :param num_scans: Number of scans
        :type num_scans: int
        :param scan_rate: Scan rate in Hertz
        :type scan_rate: int
        :return: Measured values, Tuple of (average, max, min) voltage
        :rtype: tuple
        """

        config = [
            (f'{port}_EF_INDEX', 3),
            (f'{port}_EF_CONFIG_A', num_scans),
            (f'{port}_EF_CONFIG_D', scan_rate),
        ]

        self.write(config)

        result = [
            f'{port}_EF_READ_A',
            f'{port}_EF_READ_B',
            f'{port}_EF_READ_C',
        ]

        return self.read(result)

    def config_read_frequency(self, port: str, clock_source: int = 0, edge: int = _POSITIVE_EDGES, config: int = _ONE_SHOT):
        """

        Parameters
        ----------
        port :
        clock_source :
        edge :
        config :

        Returns
        -------

        """
        """
        Configure Labjack to sample frequency
        :param port: pin name
        :type port: str
        :param clock_source: Clock source index, 0 (32bit), 1 (16bit), or 2 (16bit)
        :type clock_source: int
        :param edge: Sampling positive or negative edges
        :type edge: int
        :param config: Configure, if frequency is measured once (ONE_SHOT) or constantly (CONTINUOUS)
        :type config: int
        """
        if not self.DIO_NAME_MAP[port] in self.PINS_FREQUENCY_IN[self._device]:
            raise ExceptionDAQ(f'Error! "{port}/{self.DIO_NAME_MAP[port]}" cannot sample frequency. Use {self.PINS_FREQUENCY_IN[self._device]} instead.')

        if clock_source == 0:
            self._clock1_enabled = False
            self._clock2_enabled = False
        if clock_source == 1:
            self._clock1_enabled = True
        if clock_source == 2:
            self._clock2_enabled = True

        _config = [
            (f"{self.DIO_NAME_MAP[port]}_EF_ENABLE", 0),  # Deactivate
            (f"DIO_EF_CLOCK{clock_source}_ENABLE", 0),
            (f"DIO_EF_CLOCK{clock_source}_DIVISOR", 0),
            (f"DIO_EF_CLOCK{clock_source}_ROLL_VALUE", 0),
            (f"{self.DIO_NAME_MAP[port]}_EF_CONFIG_A", config),
            (f"{self.DIO_NAME_MAP[port]}_EF_INDEX", edge),  # 3 = positive edges, 4 = negative edges
        ]

        self.write(_config)

        _config = []

        if self._clock1_enabled:
            _config.append(("DIO_EF_CLOCK1_ENABLE", 1))

        if self._clock2_enabled:
            _config.append(("DIO_EF_CLOCK2_ENABLE", 1))

        if not self._clock1_enabled and not self._clock2_enabled:
            _config.append(("DIO_EF_CLOCK0_ENABLE", 1))

            _config.append((f"{self.DIO_NAME_MAP[port]}_EF_ENABLE", 1))

        self.write(_config)

    def read_frequency(self, port: str) -> float:
        """

        Parameters
        ----------
        port :

        Returns
        -------

        """
        """
        Sample frequency on digital input
        :param port: digital port name
        :type port: str
        :return: Frequency in Hertz
        :rtype: int
        """
        if not self.DIO_NAME_MAP[port] in self.PINS_FREQUENCY_IN[self._device]:
            raise ExceptionDAQ(f'"{port}/{self.DIO_NAME_MAP[port]}" cannot sample frequency. Use {self.PINS_FREQUENCY_IN[self._device]} instead.')

        # register = '%s_EF_READ_A_F_AND_RESET' % self.DIO_NAME_MAP[port]
        register = f'{self.DIO_NAME_MAP[port]}_EF_READ_A_F'

        cnt_try = 50

        while cnt_try > 0:
            res = self.read(register)
            if res != 0.0:
                return 1 / res
            cnt_try -= 1
        return 0.0

    def config_stream_trigger(self, port: str, enable: int = 1):
        """

        Parameters
        ----------
        port :
        enable :

        Returns
        -------

        """
        """
        stream_trigger = 0,  no trigger. Stream will start when Enabled
        stream_trigger = 2000,  DIO0_EF will start stream
        stream_trigger = 2001,  DIO1_EF will start stream
        stream_trigger = 2002,  DIO2_EF will start stream...to DIO7_EF

        keep in mind that scanRate of streamBurst has to be >= (numScans + 1) * 2 * frequency of triggering signal
        """
        stream_trigger = 2000 + int(self.DIO_NAME_MAP[port][3:])
        if enable == 0:
            stream_trigger = 0
        # Configure LJM for unpredictable stream timing
        ljm.writeLibraryConfigStringS("LJM_STREAM_SCANS_RETURN", "LJM_STREAM_SCANS_RETURN_ALL")
        ljm.writeLibraryConfigS("LJM_STREAM_RECEIVE_TIMEOUT_MS", 0)

        self.write(port, 0)

        # 2001 sets DIO1 / FIO1 as the stream trigger
        self.write("STREAM_TRIGGER_INDEX", stream_trigger)

        # DIO%s_EF_ENABLE: Clear any previous DIO0_EF settings [0]
        # DIO%s_EF_INDEX: 12 enables conditional reset used for triggered acquisition [12]
        # DIO%s_EF_CONFIG_A:
        #       Bit 0: Edge select; 0:falling, 1:rising.
        #       Bit 1: reserved
        #       Bit 2: 0=OneShot; 1 = only reset once. 0 = reset every n edges. [1 or 5]
        config = [
            (f"{self.DIO_NAME_MAP[port]}_EF_ENABLE", 0),
            (f"{self.DIO_NAME_MAP[port]}_EF_INDEX", 12),
            (f"{self.DIO_NAME_MAP[port]}_EF_CONFIG_A", 1),
            (f"{self.DIO_NAME_MAP[port]}_EF_ENABLE", 1)
        ]

        self.write(config)

    def read_average_voltage_triggered(self, port: Union[List[str], Tuple[str], str], num_scans: int = 20, scan_rate: int = 2000) -> List[np.ndarray]:
        """
        Sample analog port and return the average voltage.

        The maximum possible sample time is 180 ms.
        Sample time is the number of samples divided by the sample frequency. For example, the period is 16.7 ms when using a scan rate of 6000 Hz and 100 samples:

        100 samples / 6000 samples per second = 16.7 ms

        If the signal has a known periodic component, then setting the sample time to an even multiple of the period will generally improve results.

        Parameters
        ----------
        port : Union[List[str], Tuple[str], str]
            Port names
        num_scans : int
            Number of scans
        scan_rate : int
            Scan frequency in Hz

        Returns
        -------
        List[np.ndarray]

        """
        if not isinstance(port, self.list_types):
            port = [port]
        num_ports = len(port)
        port_addresses = ljm.namesToAddresses(num_ports, port)[0]  # returns (Address, DataType)
        # self.write('STREAM_SETTLING_US', 2000)  # stream settling time in microseconds, max = 4400
        sampled_data = ljm.streamBurst(self._handle, num_ports, port_addresses, float(scan_rate), num_scans)[1]  # returns tuple (ScanRate, samples_acquired)

        sampled_data_ave = []
        for i in range(1, num_ports + 1):
            sampled_data_per_channel = [i for i in sampled_data[i - 1::num_ports]]
            sampled_data_ave.append(np.mean(sampled_data_per_channel))

        return sampled_data_ave

    def set_voltage_range(self, port: str, voltage_range: int):
        """
        Applies the amplification on selected analog input. Default range is 10V, meaning analog input range is +/-10V.
        IMPORTANT: AIN are first mux'ed and then they are amplified. Therefore, when using MUX80, the same gain is applied to the set of mux'ed signals.

        Parameters
        ----------
        port : str
            Port name
        voltage_range : int
            Desired voltage range after amplification
            Supported ranges:
            10      : sets gain=x1, so that the analog input range is ±10 volts (default)
            1       : sets gain=x10, so that the analog input range is ±1 volts.
            0.1     : sets gain=x100, so that the analog input range is ±0.1 volts.
            0.01    : sets gain=x1000, so that the analog input range is ±0.01 volts
        Raises
        ------
            ExceptionDAQ: If device is not T7
        """
        if self._device != 'T7':
            raise ExceptionDAQ('Set voltage range only available on T7!')

        self.write(f'{port}_RANGE', voltage_range)

    def generate_pwm(self, port: str, frequency: int, clock_source: int = 0, duty_cycle: int = 0, phase_shift: int = None, num_pulses: int = None):
        """
        Generate PWM signal with controllable phase shift and controllable number of pulses.

        Parameters
        ----------
        port : str
            Port name
        frequency : int
            Desired PWM frequency in Hz
        clock_source : int
            Clock source. Possible values are 0, 1, 2. There is only one 32bit register. 0 uses all 32 bits, 1 and 2 use the upper and the lower 16 bits.
                             If you use clock 0, you cannot use 1 and 2 and vice versa.
        duty_cycle : int
            common duty cycle (of high pulses) in percentage
        phase_shift : int
            Phase shift in degrees
        num_pulses : int
            Number of pulses
        """

        divisor, roll_value = self.__calc_divisor_rollvalue(frequency)

        index = 0
        config_a = int(roll_value * duty_cycle / 100)
        config_b = 0
        config_c = 0

        if phase_shift is not None or num_pulses is not None:
            index = 1
            config_b = int((phase_shift or 0) * roll_value / 360)  # °
            count_duty_cycle = int(((duty_cycle * roll_value) / 100))  # %
            config_a = (config_b + count_duty_cycle) % roll_value

            if num_pulses is not None:
                index = 2
                config_c = num_pulses

        self._config_common_pwm(port, index, divisor, roll_value, clock_source=clock_source, config_a=config_a, config_b=config_b, config_c=config_c)

    def generate_pwm_halfbridge(self, port_pwm_high: str, port_pwm_low: str, frequency: int = 10e3, clock_source: int = 1, dead_time: float = 1e-6):
        """
        Generate PWM half bridge signal with controllable dead time.

        Parameters
        ----------
        port_pwm_high : str
            Pin name for high side signal (eg. FIO3)
        port_pwm_low : str
            Pin name for low side signal (eg. FIO4)
        frequency : int
            Frequency of the PWM in Hz
        clock_source : int
            Clock source. Possible values are 0, 1, 2. There is only one 32bit register. 0 uses all 32 bits, 1 and 2 use the upper and the lower 16 bits.
                             If you use clock 0, you cannot use 1 and 2 and vice versa.
        dead_time : float
            Dead time for two signals in seconds
        """

        index = 1
        divisor, roll_value = self.__calc_divisor_rollvalue(frequency)

        time_resolution = 1 / (frequency * roll_value)
        dead_time_counter = math.ceil(dead_time / time_resolution)
        config_a_low = (roll_value / 2) - 2 * dead_time_counter  # 50% duty cycle
        config_b_high = config_a_low + dead_time_counter
        config_a_high = config_b_high + roll_value / 2

        self._config_common_pwm(port_pwm_high, index, divisor, roll_value, clock_source, config_a=config_a_high, config_b=config_b_high)
        self._config_common_pwm(port_pwm_low, index, divisor, roll_value, clock_source, config_a=config_a_low)

    def disable_waveforms(self, *port: str):
        """
        Disable internal Labjack registers from any preconfigured states

        Parameters
        ----------
        port : str
            One or multiple port names. Is actually a tuple.

        Raises
        ------
            ExceptionDAQ: If port tuple is empty

        """
        if not port:
            raise ExceptionDAQ("Port names list is empty")

        for p in port:
            self.write(p, 0)
            self.write(f"{self.DIO_NAME_MAP[p]}_EF_ENABLE", 0)

    def read_differential(self, port: str, reference_port: str = None) -> np.ndarray:
        """
        Differential readings use a second AIN as a reference point (a.k.a. negative AIN channel).
        For AIN in extended range, positive channels can be in the following ranges:
                AIN16 to AIN23
                AIN32 to AIN39
                AIN48 to AIN55
                AIN64 to AIN71
                AIN80 to AIN87
                AIN96 to AIN103
                AIN112 to AIN119
                The negative channel is 8 higher than the positive channel. (ex. pos_ch: AIN48, neg_ch: AIN56).
        If reference_port is None, it takes the number of "port" (e.g AIN16 -> 16) and adds 8 to it (-> 24)

        Parameters
        ----------
        port : str
            Port name

        reference_port : str
            Negative channel to be used for selected positive channel.
                               199 = Default -> single ended

        Raises
        ------
            ExceptionDAQ: If device is not T7

        Returns
        -------
        np.ndarray
            Differential value read with reference to reference_port
        """
        if self._device != 'T7':
            raise ExceptionDAQ('Differential analog in only available on T7')

        single_ended = 199

        if isinstance(reference_port, str):
            reference_port = int(reference_port[3:])

        if reference_port is None:
            reference_port = int(port[3:]) + 8

        self.write(f'{port}_NEGATIVE_CH', reference_port)
        diff_value_read = self.read_average_voltage(port)
        # return to single_ended
        self.write(f'{port}_NEGATIVE_CH', single_ended)
        return diff_value_read

    def adc_config(self, clk_ch: str, cs_ch: str, mosi_ch: str, spi_mode: int = 0, clk_speed: int = 0, options: int = 0):
        """
        Configures the ADC on a Drive Module via SPI.

        Parameters
        ----------
        clk_ch : str
            DIO line for Clock (ex. CLK_ch = DIO3)
        cs_ch : str
            DIO line for ChipSelect (ex. CS_ch = DIO4)
        mosi_ch : str
            DIO line for MOSI (ex. MOSI_ch = DIO5)
        spi_mode :
        clk_speed : int
            SPI_SPEED_THROTTLE, clock frequency in kHz
                    0       = 780 (max speed)
                    65530	= 380
                    65500	= 100
                    65100	= 10
                    61100	= 1
                    21000	= 0.1
                    1       = 0.067
        options : int
            SPI_OPTIONS, Default = 0 => chip select active low
            bit 0:
            0 = Active low clock select enabled
            1 = Active low clock select disabled.
            bit 1:
            0 = set DIO directions before starting the SPI operations.
            1 = do not set DIO directions.
            bit 2:
            0 = transmit data MSB first
            1 = transmit data LSB first
            bit 3: Reserved
            bits 4-7: Number of bits in the last byte. 0 = 8.
            bits 8-15: Reserved
        """

        # defining the ADC channels
        config = [
            ("SPI_CLK_DIONUM", int(self.DIO_NAME_MAP[clk_ch][3:])),
            ("SPI_CS_DIONUM", int(self.DIO_NAME_MAP[cs_ch][3:])),
            ("SPI_MOSI_DIONUM", int(self.DIO_NAME_MAP[mosi_ch][3:])),
        ]

        self.write(config)

        # configuring the SPI communication
        config = [
            ("SPI_MODE", spi_mode),
            ("SPI_SPEED_THROTTLE", clk_speed),
            ("SPI_OPTIONS", options)
        ]

        self.write(config)

    def adc_get_bytes(self, channel_out: str, num_bytes: int) -> List[int]:
        """
        Get multiple bytes from ADC

        Parameters
        ----------
        channel_out : str
            MISO channel (DIO Port)
        num_bytes : int
            Amount of bytes

        Returns
        -------

        """
        config = [
            ("SPI_MISO_DIONUM", int(self.DIO_NAME_MAP[channel_out][3:])),
            ("SPI_NUM_BYTES", num_bytes)
        ]

        self.write(config)

        # performing the SPI communication
        # SPI is full duplex = number of bytes read from and written to the slave must be equal
        # * to read data from a slave without sending data to it, load dummy data into SPI_DATA_TX
        data_write = [0] * num_bytes
        ljm.eWriteNameByteArray(self._handle, 'SPI_DATA_TX', num_bytes, data_write)
        # execute SPI communication
        self.write("SPI_GO", 1)

        # read the bytes
        return ljm.eReadNameByteArray(self._handle, 'SPI_DATA_RX', num_bytes)

    def adc_get_value(self, channel_out: str) -> int:
        """
        Retrieve digital value from ADC

        Parameters
        ----------
        channel_out : str
            MISO channel

        Returns
        -------
        int
            ?-bit integer, number of bits depends on ADC
        """
        # numBytes = 2 => each D_OUT is 2 bytes long
        num_bytes = 2
        data_read = self.adc_get_bytes(channel_out, num_bytes)

        # extract the analog data.
        # this is specific to ADC used in Drive1000
        # ADC7265 sends 2 leading zeros, followed by 12 bits of data, followed by 2 trailing zeros
        data_out = [format(int(data_read[0]), '08b'), format(int(data_read[1]), '08b')]  # convert to binary numbers
        data_out = ''.join(data_out)[2:14]  # store as 12 bit number
        data_out = int(data_out, 2)  # convert to integer

        return data_out

    # to be verified how ADC is outputting data when a square wave is present
    # likely multiple SPI transactions needed
    def adc_get_stream(self, channel_out: str) -> List[int]:
        """
        Read 4 bytes from ADC and format the output data.

        Parameters
        ----------
        channel_out : str
            MISO channel

        Returns
        -------
        List[int]
            List with ADC values

        """
        # channel_out (MISO_ch) = adc_OUTA or adc_OUTB
        # numBytes = 2 => each D_OUT is 2 bytes long
        num_bytes = 4
        data_read = self.adc_get_bytes(channel_out, num_bytes)

        # extract the analog data
        # go through buffered bytes and extract every second 2-byte word
        # ADC7265 sends 2 leading zeros, followed by 12 bits of data, followed by 2 trailing zeros
        data = []
        data_out = []
        for i in range(0, len(data_read), 4):
            for m in range(i, i + 2):
                data.append(data_read[m])

        for n in range(0, len(data), 2):
            data_bin = [format(int(data[n]), '08b'), format(int(data_read[n + 1]), '08b')]  # convert to binary numbers
            data_bin = ''.join(data_bin)[2:14]  # store as 12 bit number
            data_out.append(int(data_bin, 2))  # convert to integer

        return data_out

    def i2c_config(self, sda_ch: str = 'EIO0', scl_ch: str = 'EIO1', clk_speed: int = 65516, options: int = 0):
        """
        Configure the I2C communication.
        Parameters
        ----------
        sda_ch : str
            Data line
            FIO0:7 = 0:7
            EIO0:7 = 8:15
            CIO0:7 = 16:23
        scl_ch : str
            Clock line
        clk_speed : int
            i2c speed. Default = 0, equivalent to 65536 = ~450 kHz
                1 = ~40 Hz,
                65516 = ~100 kHz.
        options : int
            controls details of the I2C protocol to improve device compatibility. Default = 0
                bit 0: 1 = Reset the I2C bus before attempting communication
                bit 1: 0 = Restarts will use a stop and a start
                       1 = Restarts will not use a stop
                bit 2: 1 = disable clock stretching
        """

        # defining the I2C channels
        ch_config = [
            ("I2C_SDA_DIONUM", int(self.DIO_NAME_MAP[sda_ch][3:])),
            ("I2C_SCL_DIONUM", int(self.DIO_NAME_MAP[scl_ch][3:]))
        ]

        self.write(ch_config)

        # configuring the I2C communication
        conf_names = [
            ("I2C_SPEED_THROTTLE", clk_speed),
            ("I2C_OPTIONS", options)
        ]

        self.write(conf_names)

    def i2c_set_slave_address(self, slave_address: int):
        """
        Set the I2C slave address

        Parameters
        ----------
        slave_address : int
            Slave address
        """
        # 7-bit address of the slave device, shifted left by FW to allow for I2C R/W bit
        self.write("I2C_SLAVE_ADDRESS", slave_address)

    def i2c_read(self, rx_register: int, rx_num_bytes: int) -> List[int]:
        """
        Reads n bytes from I2C slave.

        Parameters
        ----------
        rx_register : int
            Desired register address.
        rx_num_bytes : int
            Amount of bytes.

        Raises
        ------
           ExceptionNoAcknowledgement: if I2C Transaction was not successful

        Returns
        -------
        List[int]
            List of bytes.
        """
        config = [("I2C_NUM_BYTES_TX", 1),
                  ("I2C_NUM_BYTES_RX", rx_num_bytes)]

        self.write(config)

        # performing the I2C communication
        # data received from the slave is saved in the buffer on Labjack
        #    eWriteNameByteArray(handle, name, numBytes, Bytes)
        #    eReadNameByteArray(handle, name, numBytes)
        ljm.eWriteNameByteArray(self._handle, 'I2C_DATA_TX', 1, [rx_register])
        # executing I2C communication
        self.write("I2C_GO", 1)

        data_read = ljm.eReadNameByteArray(self._handle, 'I2C_DATA_RX', rx_num_bytes)

        # verify the transaction by reading the acknowledge bits
        # only bytes transmitted to the slave produce ACK bits
        # bit=1  transaction was successful
        # bit=0  transaction did not succeed
        # Wtf
        ack = int(self.read('I2C_ACKS'))
        if ack != (1 << ack.bit_length()) - 1 or ack == 0:
            raise ExceptionNoAcknowledgement("I2C Transaction was not successful")

        return data_read

    def i2c_write(self, tx_register: Union[List[int], Tuple[int], int], tx_data: Union[List[int], Tuple[int], int]):
        """
        Write data to I2C slave's register.
        Parameters
        ----------
        tx_register : Union[List[int], Tuple[int], int]
            One or more register address
        tx_data : Union[List[int], Tuple[int], int]
            One or more bytes to write

        Raises
        ------
           ExceptionNoAcknowledgement: if I2C Transaction was not successful
        """

        if not isinstance(tx_register, self.list_types):
            tx_register = [tx_register]

        if not isinstance(tx_data, self.list_types):
            tx_data = [tx_data]

        data_to_send = tx_register + tx_data

        config = [("I2C_NUM_BYTES_TX", len(data_to_send)),
                  ("I2C_NUM_BYTES_RX", 0)]

        self.write(config)

        # performing the I2C communication
        ljm.eWriteNameByteArray(self._handle, 'I2C_DATA_TX', len(data_to_send), data_to_send)
        # executing I2C communication
        self.write("I2C_GO", 1)

        # verify the transaction by reading the acknowledge bits
        # only bytes transmitted to the slave produce ACK bits
        # bit=1  transaction was successful
        # bit=0  transaction did not succeed
        ack = int(self.read('I2C_ACKS'))
        if ack != (1 << ack.bit_length()) - 1 or ack == 0:
            raise ExceptionNoAcknowledgement("I2C Transaction was not successful")

    def config_uart(self, port_tx: str, port_rx: str, baud_rate: int = 9600):
        """
        Init UART on Labjack.

        Parameters
        ----------
        baud_rate : int
            Baud rate of UART communication.
        port_tx : str
            Transceiver port name
        port_rx : str
            Receiver port name
        """

        self.UART_INIT_VALUE[1] = int(self.DIO_NAME_MAP[port_tx][3:])
        self.UART_INIT_VALUE[2] = int(self.DIO_NAME_MAP[port_rx][3:])
        self.UART_INIT_VALUE[3] = baud_rate

        self.write(self.UART_INIT_REGISTER, self.UART_INIT_VALUE)

    def transmit(self, data: Union[List, str]):
        """
        Send data to UART slave.

        Parameters
        ----------
        data : Union[List, str]
            Data to send.

        Raises
        ------
            ExceptionUART: If data is not a list or a string.

        """
        if not isinstance(data, (list, str)):
            raise ExceptionUART('Provided data is no list or string')

        if isinstance(data, str):
            data = [ord(c) for c in data]

        self.write('ASYNCH_NUM_BYTES_TX', len(data))

        for d in data:
            self.write('ASYNCH_DATA_TX', d)

        self.write('ASYNCH_TX_GO', 1)

    def receive(self, num_bytes: int = None) -> List[int]:
        """
        Receive data from slave.

        Parameters
        ----------
        num_bytes : int
            Expected amount of bytes.

        Returns
        -------
        List[int]
            Return values in a list.

        """
        bytes_in_buffer = self.in_waiting
        rx_buffer = []
        to_read = bytes_in_buffer

        if num_bytes and num_bytes <= bytes_in_buffer:
            to_read = num_bytes

        for c in range(to_read):
            rx_buffer.append(int(self.read('ASYNCH_DATA_RX')))

        return rx_buffer

    @property
    def in_waiting(self) -> int:
        """
        Current received amount of bytes in buffer.

        Returns
        -------
        int
            Amount of bytes.

        """
        return int(self.read('ASYNCH_NUM_BYTES_RX'))
