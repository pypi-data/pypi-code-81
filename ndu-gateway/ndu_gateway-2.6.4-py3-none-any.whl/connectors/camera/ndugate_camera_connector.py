"""
NDU-Gate

connector ayar dosyası : etc/ndu-gateway/config/camera.json
"""

import time
from threading import Thread
from random import choice
from string import ascii_lowercase
import json
import zmq

from ndu_gateway.connectors.connector import Connector, log

# TODO - use config
HOSTNAME = "127.0.0.1"
PORT = "60600"


def log_exception(e):
    if hasattr(e, 'message'):
        log.error(e.message)
    else:
        log.exception(e)


class NDUGateCameraConnector(Thread, Connector):
    def __init__(self, gateway, config, connector_type):
        super().__init__()
        self.statistics = {'MessagesReceived': 0, 'MessagesSent': 0}
        self.__config = config
        log.info("NDU - config %s", config)
        self.__gateway = gateway
        # get from the configuration or create name for logs.
        self.setName(self.__config.get("name", "Custom %s connector " % self.get_name() + ''.join(choice(ascii_lowercase) for _ in range(5))))
        log.info("Starting Custom %s connector", self.get_name())

        self.daemon = True  # Set self thread as daemon
        self.stopped = True  # Service variable for check state
        self.__connected = False  # Service variable for check connection to device

        self.lastConnectionCheck = 0
        self.__connect_to_devices()

        self.deviceLastAttributes = {}
        self.__setAttributeQuery = {}

        log.info('Custom connector %s initialization success.', self.get_name())

        self._host = config.get("host", HOSTNAME)
        self._port = config.get("port", PORT)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

    def __connect_to_devices(self):
        self.__connected = True
        self.lastConnectionCheck = time.time()

    def open(self):
        log.info('%s connecting %s:%s', self.get_name(), self._host, self._port)
        self.stopped = False
        self.socket.connect("tcp://{}:{}".format(self._host, self._port))
        topic = self.__config.get("topic", "ndugate")
        self.socket.subscribe(topic)
        self.start()

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.__connected

    def run(self):  # Main loop of thread
        log.info('%s started.', self.get_name())

        result_dict = {
            'deviceName': self.__gateway.name,
            'deviceType': "default",
            'attributes': [],
            'telemetry': [],
        }

        try:
            while True:
                try:
                    data_part = self.socket.recv_string()
                    if not data_part:
                        continue

                    json_string = data_part.split(' ', 1)[1]
                    if json_string is None or json_string is str(""):
                        continue

                    data = json.loads(json_string)

                    result_dict['telemetry'] = []
                    result_dict['attributes'] = []

                    if data is None:
                        continue

                    if data.get("telemetry") is not None:
                        telemetry_data = data.get("telemetry")
                        result_dict['telemetry'].append(telemetry_data)

                    if data.get("attribute") is not None:
                        attr_data = data.get("attribute")
                        for attr_key in attr_data:
                            result_dict['attributes'].append({attr_key: attr_data[attr_key]})

                    self.__gateway.send_to_storage(self.__gateway.name, result_dict)
                    time.sleep(0.1)
                except Exception as e:
                    log_exception(e)
                    time.sleep(5)
        except Exception as e:
            log_exception(e)

    def close(self):
        if self.context:
            self.context.destroy()
        self.stopped = True

    def on_attributes_update(self, content):
        device_name = content["device"]
        log.debug("NDU - on_attributes_update device : %s , content : %s", content, device_name)
        pass

    def server_side_rpc_handler(self, content):
        log.debug("NDU - server_side_rpc_handler content : %s", content)
        pass



