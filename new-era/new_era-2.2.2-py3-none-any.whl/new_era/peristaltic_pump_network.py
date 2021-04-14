import serial

from new_era.peristaltic_pump import PeristalticPump


class NetworkedPeristalticPump(PeristalticPump):
    def __init__(self,
                 pump_network,
                 address: int,
                 baudrate: int,
                 volume_unit: str = 'ml',
                 rate_unit: str = 'ml/min',
                 ):
        self.pump_network = pump_network
        self.ser = self.pump_network.ser
        self._port = self.pump_network.port
        self._baudrate = baudrate
        self._address = address

        # initialize rate and volume units on instantiation - these are the values in the RATE_UNIT and VOL_UNIT
        # dictionaries, as they are more readable
        self.rate_unit = rate_unit
        self.volume_unit = volume_unit
        # use the reversed versions or RATE and VOL_UNIT in order to get the command that the pump understands
        self.rate_unit_cmd = self.REV_RATE_UNIT[rate_unit]
        self.volume_unit_cmd = self.REV_VOL_UNIT[volume_unit]

        pump_firmware_version = self._xmit('VER')
        print(f'Connected to pump {pump_firmware_version}')


class PeristalticPumpNetwork:
    CONNECTION_SETTINGS = dict(
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )

    def __init__(self,
                 port: str,
                 baudrate: int = 9600,
                 ):
        self.ser = None
        self._port = port
        self._baudrate = baudrate
        self.connect()

    @property
    def port(self) -> str:
        return self._port

    @property
    def baudrate(self) -> int:
        return self._baudrate

    def connect(self):
        if self.ser is None:
            cn = serial.Serial(port=self.port, baudrate=self.baudrate, **self.CONNECTION_SETTINGS)
            self.ser = cn
        if not self.ser.isOpen():
            self.ser.open()

    def add_pump(self,
                 address: int,
                 baudrate: int = 9600,
                 volume_unit: str = 'ml',
                 rate_unit: str = 'ml/min',
                 ) -> NetworkedPeristalticPump:
        pump = NetworkedPeristalticPump(self, address, baudrate, volume_unit, rate_unit)
        return pump


