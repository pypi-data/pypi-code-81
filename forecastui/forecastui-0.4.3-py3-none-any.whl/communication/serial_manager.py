from .serial_handler import SerialHandler
from ..callbacks import StatusCallback, CallbackManager, PresetCallback
from ..utility import Store

class SerialManager:

    def __init__(self):
        self.__is_connected = False
        self.__is_running = False

    def start(self, port, baudrate=921600):
        self.serial = SerialHandler(port=port, baudrate=baudrate)
        self.__callback_manager = CallbackManager(PresetCallback(Store.preset))
        self.serial.setDataReqCb(self.__callback_manager)
        self.is_connected = True

    def start_experiment(self, index):
        print("Starting experiment with value {}".format(index))
        self.serial.setStatusCb(StatusCallback())
        self.__callback_manager.current_index = index
        self.serial.start()
        self.is_running = True
        return self.is_running

    def stop_experiment(self):
        self.serial.stop()
        self.is_running = False
        return self.is_running

    def stop(self):
        if self.is_running:
            self.stop_experiment()
        self.is_connected = False
        return self.serial._dataReqCallback.getHistory()

    def input_value(self, value):
        if self.serial is not None:
            self.serial._dataReqCallback.unlock(value)

    def getLog(self):
        return self.serial.getLog()

    def getError(self):
        return self.serial.getErr()

    @property
    def is_running(self):
        return self.__is_running

    @is_running.setter
    def is_running(self, value):
        self.__is_running = bool(value)

    @property
    def is_connected(self):
        return self.__is_connected

    @is_connected.setter
    def is_connected(self, value):
        self.__is_connected = bool(value)