import sys
from bleak import BleakScanner, BleakClient
import asyncio
from time import sleep
import threading, queue
import socket
from datetime import datetime
import json
from bffacilities.utils import createLogger
import logging
logger = createLogger("bt", level=logging.DEBUG,\
    savefile=False, stream=True, timeformat="%H:%M:%S" )

if sys.platform == "win32":
    from Windows.Devices.Bluetooth.Advertisement import BluetoothLEAdvertisementFilter, BluetoothLEAdvertisement 
else:
    raise ValueError("Unsupported")

class BluetoothWrapper(object):
    """封装蓝牙操作
    """
    IO_DATA_CHAR_UUID_W   = "0000ffe1-0000-1000-8000-00805f9b34fb"
    IO_DATA_CHAR_UUID_W2  = "0000ffe2-0000-1000-8000-00805f9b34fb"

    def __init__(self, **kwargs):
        self._btMsgProcessors = []
        processor = kwargs.get("btMsgProcessor")
        if processor is not None:
            self._btMsgProcessors.append(processor)
        self.loop = asyncio.get_event_loop()
        self._msgToBtQueue = queue.Queue()
        self._cmdQueue = queue.Queue()

        self._btClient = None
        self._btConnected = False
        self._devices = { } # key address
        self._lastAddress = None

    @property
    def is_connected(self):
        return self._btConnected
    @property
    def btMsgProcessor(self):
        return self._btMsgProcessors
    
    @btMsgProcessor.setter
    def btMsgProcessor(self, p):
        """
        Callback

            btMsgProcess(data: bytes)
        """
        self._btMsgProcessors.append(p)
    
    def export_deviceInfo(self):
        data = []
        for device in self._devices.values():
            name = device.name if hasattr(device, "name") else None
                
            data.append({
                "address": device.address,
                "name": name,
                "rssi": device.rssi
            })
        data = json.dumps(data)
        return data

    def syncDeviceToOther(self):
        """should be rewrite by subclass
        """
        pass

    def _onRecvBtMsg(self, sender: int, data: bytes):
        """
        Args
            data bytes
        """
        # logger.debug(f"Recv BT & Send: {len(data)}")
        for p in self._btMsgProcessors:
            p(data)

    def listDevice(self, timeout = 10):
        async def _list(timeout):
            devices = await BleakScanner.discover(timeout=timeout)
            for d in devices:
                if d.address not in self._devices:
                    self._devices[d.address] = d
            logger.info(f"{self._devices}")
            self.syncDeviceToOther()
        self.loop.run_until_complete(_list(timeout))
    
    def findDevice(self, name = None, seconds = 5.0):
        self.loop.run_until_complete(self.monitDevice(name, seconds))

    async def monitDevice(self, name, seconds=0):
        """
        Args:
            name  device name such as "BTDEVICE1"
        """
        bleFilter = BluetoothLEAdvertisementFilter()
        if name:
            ad = BluetoothLEAdvertisement()
            ad.put_LocalName(name)
            bleFilter.put_Advertisement(ad)

        scanner = BleakScanner(AdvertisementFilter=bleFilter)
        scanner.register_detection_callback(self._detection_callback)
        # await scanner.set_scanning_filter()
        await scanner.start()
        if seconds <= 5:
            while self._btConnected:
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(seconds)
        await scanner.stop()
        logger.info("[BT] Monit Device Done")

    def _detection_callback(self, device, advertisement_data):
        if len(advertisement_data.local_name) == 0:
            return
        if device.address not in self._devices:
            logger.info(f"First [{datetime.now()}] RSSI: {device.rssi}, {advertisement_data.local_name}, {device.address}")
        device.name = advertisement_data.local_name
        self._devices[device.address] = device
        self.syncDeviceToOther()

    async def _connect(self, address):
        """after function exits, bluetooth device will be disconnected
        """
        if self._btClient is not None:
            await self._btClient.disconnect()

        self._btClient = BleakClient(address)
        logger.info(f"[BT] Connecting Bluetooth: {address}")
        # service = await self._btClient.get_services()
        # model_number = await self._btClient.read_gatt_char(BluetoothWrapper.IO_DATA_CHAR_UUID_W )
        # print(f"Model Number {model_number}: {''.join(map(chr, model_number))}")
        try:
            self._btConnected = await self._btClient.connect()
            logger.info(f"[BT] Client {self._btClient} connected: {self._btConnected}")
            if self._btConnected:
                await self._btClient.start_notify(\
                    BluetoothWrapper.IO_DATA_CHAR_UUID_W, self._onRecvBtMsg)
        except Exception as e:
            self._btConnected = False
            logger.warning(f"[BT] Connect failed: {e}")
        # finally:
            # await self._btClient.disconnect()


    async def _sendMsgToBt(self):
        if not self._msgToBtQueue.empty():
            sData = self._msgToBtQueue.get()
            try:
                await self._btClient.write_gatt_char(BluetoothWrapper.IO_DATA_CHAR_UUID_W, sData)
            except : 
                pass
            logger.debug(f"SendData Bt {sData}")
        else:
            await asyncio.sleep(0)
    
    def sendMsgToBt(self):
        self.loop.run_until_complete(self._sendMsgToBt())

    async def _connectAndListen(self, address):
        await self._connect(address)
        try:
            while self._btConnected:
                await self._sendMsgToBt()
        except Exception as e:
            self._btConnected = False
            logger.warning(f"[BT] Exception Listen: {e}")
        finally:
            await self._btClient.disconnect()
        logger.info("[BT] connect process done")

    def connectToBLE(self, address, listen=False):
        """
        Args: 
            address:  MAC address

            listen 
            if True, the event loop will run always and stop main thread

            if False, you have to call `sendMsgToBt` mannually if there is 
            pending msg needs to be sent to bluetooth

        Note:
            If a bluetooth is connected, it should be disconnect first
        """
        if self._btConnected:
            if address != self._lastAddress:
                self.disconnect()
            else:
                logger.warning("Bluetooth Device is already connected")
                return

        self._lastAddress = address
        if listen:
            self.loop.run_until_complete(self._connectAndListen(address))
        else:
            self.loop.run_until_complete(self._connect(address))

    def disconnect(self):
        if self._btConnected:
            logger.info("[BT] Stoping bluetooth, wait for a moment")
            async def _stop():
                await self._btClient.disconnect()
            self.loop.run_until_complete(_stop())
            logger.info("[BT] bluetooth stopped")
        else:
            logger.warning("[BT] Not Connected")


    def _processCmd(self, cmd):
        """
        {
            "action": "listDevice",
            "timeout": "60", // seconds
        }

        {
            "action": "findDevice",
            "name": "CMPS", // or no name for find all device
            "timeout": 30, // default 30
        }

        {
            "action": "disconnect" // disconnect if a device has connected
        }

        {
            "action": "quit" // quit program
        }
        """
        # logger.debug(f"Cmd { threading.get_ident()}")
        action = cmd["action"]
        if action == "connect":
            if "address" in cmd:
                self.connectToBLE(cmd["address"])
        elif action == "listDevice":
            self.listDevice(timeout= cmd.get("timeout", 10))
        elif action == "findDevice":
            self.findDevice(name=cmd.get("name"), seconds= cmd.get("timeout", 20))
        elif action == "disconnect":
            self.disconnect()
        elif action == "quit":
            self.disconnect()
            self._running = False
            logger.info("About to quit")
        else:
            logger.warning("Unsupported cmd", action)

    def processCmd(self):
        """注意，用于蓝牙接收和发送的操作，
        该方法应该在创建 BluetoothWrapper 的线程中调用
        """
        if not self._cmdQueue.empty():
            self._processCmd(self._cmdQueue.get()) 

from bffacilities.socketserver import UdpSocketServer

class BluetoothMgr(BluetoothWrapper) :
    """
    @See bffacilities.socketserver.UdpSocketServer

    默认绑定到 UDP 12001 地址上，用于接收其他模块的控制信息

    """

    def __init__(self, port = 12001, broadcast = True, **kwargs):
        super().__init__(**kwargs)
        self._bind = port
        self.sockServer = UdpSocketServer()
        self.sockServer.createListener(port = self._bind, ip="127.0.0.1")
        self.sockServer.addProcessor(self.recvCtlMsg)
        self._running = True
        if kwargs.get("btMsgProcessor") is None:
            self.btMsgProcessor = self.sockServer.send

    @property
    def is_running(self):
        return self._running

    def recvCtlMsg(self, msg: bytes, addr: tuple):
        # print(msg, addr)
        if msg.startswith(b"{"):
            try:
                cmd = json.loads(msg.decode())
                self._processCmd(cmd)
            except: pass
        else:
            self._msgToBtQueue.put(msg)

    def syncDeviceToOther(self):
        data = self.export_deviceInfo()
        self._sockSender.sendto(data.encode() + b"\n\n")

    def start(self):
        """start an loop in main thread 
        start another thread for udp server
        """
        try:
            while self._running:
                self.sendMsgToBt()
                self.sockServer.serve_once()
                sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()
    
    start_one = start
    
    def stop(self):
        self.disconnect()
        self._running = False
        logger.info("==========Bt Mgr Quit===========")


if __name__ == "__main__":
    btMgr = BluetoothMgr()
    btMgr.start()