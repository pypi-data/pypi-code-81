import os
import pickle
import asyncio
import logging
# import traceback as tb

from bleak import BleakScanner, BleakClient

from .command import RabboniCmdHelper
from .constants import ACC_FSR_CHAR, GYRO_FSR_CHAR, DATA_RATE
from .errors import (
    DeviceNotFoundError,
    UnsupportedMacAddrError,
    UnsupportedModeError,
    DisconnectionException,
    ShutdownException
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
logger.addHandler(ch)
curdir_path = os.path.dirname(os.path.realpath(__file__))

NOTIFY_UUID = "00001601-0000-1000-8000-00805f9b34fb"
BATTERY_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
READ_CONFIG_UUID = "00001705-0000-1000-8000-00805f9b34fb"
SET_CONFIG_UUID = "0000fff6-0000-1000-8000-00805f9b34fb"
SET_CONFIG_RES_UUID = "00001705-0000-1000-8000-00805f9b34fb"


def search_rabboni(dev_list):
    result = None
    for ble_device in dev_list:
        if ble_device.name == 'RABBONI':
            result = ble_device
    return result


def convert_acc(acc, acc_scale, precision=3):
    x = int(acc, 16)
    x = twos_comp(x, 16)
    x = float(x)
    # print('convert_acc', acc, x, acc_scale, x*(acc_scale)/32768)
    return round(x*(acc_scale)/32768, precision)  # x*16/32768


def convert_gyr(gyr, gyr_scale, precision=3):
    x = int(gyr, 16)
    x = twos_comp(x, 16)
    x = float(x)
    # print('convert_gyr', x, gyr_scale)
    return round(x*gyr_scale/32768, precision)


def cal_trigger(acc_list):
    trigger_val = pow(acc_list[0], 2) + pow(acc_list[1], 2) + pow(acc_list[2], 2)
    # print(f'cal_trigger: {trigger_val}')
    return trigger_val > 2.5


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return float(val)


class Rabboni:
    """
    Rabboni 類別

    Args:
        mode (str): 連線模式
        name (str): 裝置名稱
    """

    def __init__(self, mode='BLE', name='Rabboni'):
        """The constructor"""
        self.mode = mode
        self.name = name
        self.dev = None
        self.ble_client = None
        self.count = 0
        self.exit_flag = False
        self.fetch_battery = False
        self.reading_config = False
        self.setting_config = False
        self.resetting_count = False
        self._cmd_helper = RabboniCmdHelper()
        muls_file = f'{curdir_path}/muls.pkl'
        with open(muls_file, 'rb') as f:
            self.muls = pickle.load(f)

    async def scan(self):
        """ 掃描周邊 BLE 裝置 """
        ble_devices = await BleakScanner.discover()
        logger.debug(f"Scan BLE Devices: {ble_devices}")
        return ble_devices

    async def connect(self, mac_address: str = None, callback=None):
        """ 建立 Rabboni 裝置連線 """
        if self.mode == 'USB':
            pass
        elif self.mode == 'BLE':
            ble_devices = await BleakScanner.discover()
            logger.debug(f"Discover BLE Devices: {ble_devices}")
            self.dev = search_rabboni(ble_devices)
            if self.dev is not None:
                if self.dev.address in self.muls:
                    self.ble_client = BleakClient(self.dev, timeout=5.0)
                    try:
                        logger.info(f"Connecting {self.ble_client}")
                        await self.ble_client.connect()
                        await self._notify_and_record(callback)
                    except DisconnectionException as e:
                        logger.warning(e)
                        self.exit_flag = True
                    except ShutdownException as e:
                        logger.warning(e)
                        self.exit_flag = True
                    except Exception as e:
                        logger.warning(e)
                        self.exit_flag = True
                        pass
                else:
                    raise UnsupportedMacAddrError(f'{mac_address} 為不支援的 MAC 地址')
            else:
                raise DeviceNotFoundError(f'找不到裝置 ({mac_address})，無法連線...')

            logger.debug(f"Shutting down {self.name} notification.")
            await self.ble_client.stop_notify(NOTIFY_UUID)
            logger.debug(f"Done shutting down {self.name} notification.")

            logger.debug(f"Disconnecting to device {self.name}.")
            await self.ble_client.disconnect()
            logger.debug(f"{self.name} End of Loop Iteration")
        else:
            raise UnsupportedModeError('連線模式僅支援 "USB" 或 "BLE"')

    async def _notify_and_record(self, callback=None):
        self.ble_client.set_disconnected_callback(self._disconnect_callback)
        logger.debug("Connected: {0}".format(await self.ble_client.is_connected()))
        logger.debug("Starting notification.")
        if callback is not None:
            await self.ble_client.start_notify(NOTIFY_UUID, callback, name=self.name)
        else:
            await self.ble_client.start_notify(NOTIFY_UUID, self._notify_callback)

        while not self.exit_flag:
            if self.fetch_battery:
                await self.get_battery_level()
            elif self.reading_config:
                await self.read_config()
            elif self.setting_config:
                await self.set_config()
            elif self.resetting_count:
                await self.reset_count()
            else:
                await asyncio.sleep(1)

        await self.disconnect()
        # logger.debug("Shutting Down.")
        # raise ShutdownException

    async def disconnect(self):
        """ Rabboni 裝置斷開連線 """
        self.exit_flag = True
        await self.ble_client.stop_notify(NOTIFY_UUID)
        logger.debug(f"Done shutting down {self.name} notification.")

        logger.debug(f"Disconnecting to device {self.name}.")
        await self.ble_client.disconnect()
        logger.debug(f"{self.name} End of Loop Iteration")

    async def get_battery_level(self):
        """ 獲取 Rabboni 裝置電池狀態 """
        self.fetch_battery = True
        data = await self.ble_client.read_gatt_char(BATTERY_UUID)
        battery_level = int(bytes(data).hex(), 16)
        logger.debug(f'battery_level: {battery_level}')
        self.fetch_battery = False
        return battery_level

    async def get_sensor_config(self):
        reading_cmd = bytearray([self._cmd_helper.read_config_cmd.command])
        logger.debug(f'reading_cmd: {reading_cmd}')

        self.reading_config = True
        await self.ble_client.write_gatt_char(SET_CONFIG_UUID, reading_cmd)
        config_value = await self.ble_client.read_gatt_char(READ_CONFIG_UUID)
        logger.debug(f'config_value: {config_value}')
        self.reading_config = False
        return config_value

    async def set_sensor_config(self, acc_scale=2, gyr_scale=250, rate=10, threshold=2000):
        config_data = [0x00 for i in range(14)]
        config_data[0:2] = [ACC_FSR_CHAR[acc_scale], GYRO_FSR_CHAR[gyr_scale]]
        config_data[3:5] = [1, 1]
        config_data[8] = DATA_RATE[rate]
        config_data[12:14] = [threshold // 256, threshold % 256]  # 2500 => [9, 196]
        self._cmd_helper.set_config_cmd = config_data
        setting_cmd = bytearray([self._cmd_helper.set_config_cmd.command]+self._cmd_helper.set_config_cmd.data)
        logger.debug(f'setting_cmd: {setting_cmd}')

        self.setting_config = True
        await self.ble_client.write_gatt_char(SET_CONFIG_UUID, setting_cmd)
        config_value = await self.ble_client.read_gatt_char(SET_CONFIG_RES_UUID)
        logger.debug(f'set_sensor_config config_value: {config_value}')
        self.setting_config = False
        return config_value

    async def reset_count(self):
        """ 重置 Rabboni 裝置紀錄數 """
        reset_current_cmd = bytearray([self._cmd_helper.reset_current_count_cmd.command])
        reset_stored_cmd = bytearray([self._cmd_helper.reset_stored_count_cmd.command])

        self.resetting_count = True
        await self.ble_client.write_gatt_char(SET_CONFIG_UUID, reset_current_cmd)
        await self.ble_client.write_gatt_char(SET_CONFIG_UUID, reset_stored_cmd)
        config_value = await self.ble_client.read_gatt_char(SET_CONFIG_RES_UUID)
        logger.debug(f'reset_count config_value: {config_value}')
        self.resetting_count = False
        return config_value

    def _notify_callback(self, sender, data):
        # logger.info(f"sender: {sender}, data: {data}")
        value_data = bytes(data).hex()
        # logger.info(f'rab_callback sender: {sender}, value_data: {value_data}')
        # logger.info(f'rab_callback kwargs: {kwargs}')
        acc_list = [convert_acc(value_data[:4], 2),  convert_acc(value_data[4:8], 2), convert_acc(value_data[8:12], 2)]
        gyr_list = [convert_gyr(value_data[12:16], 2),  convert_gyr(value_data[16:20], 2),
                    convert_gyr(value_data[20:24], 2)]
        cur_count = int(value_data[24:28], 16)
        stored_count = int(value_data[28:], 16)
        trigger = cal_trigger(acc_list)
        # logger.info(f'trigger: {trigger}')
        print({'name': self.name, 'acc': acc_list,
               'gyr': gyr_list, 'trigger': trigger,
               'count': [cur_count, stored_count]})

    def _disconnect_callback(self, client):
        logger.warning(f"Client {client} got disconnected!")
        self.exit_flag = True
        # raise DisconnectionException("Client with address {} got disconnected!".format(client.address))
