#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import os
import enum
from pinecone.utils import get_container_memory_limit

RECV_TIMEOUT = 0.5
SEND_TIMEOUT = 0.5

MAX_CLIENTS = 100
MAX_RETRY_MSG = 100
DEFAULT_TIMEOUT = 2
GATEWAY_NAME = 'gatewayrouter'
AGGREGATOR_NAME = 'aggregator'
MAX_MSG_SIZE = 64 * 1024 * 1024
MAX_MSGS_PER_CONNECTION = 100
MAX_SOCKS_OPEN = 1000
DNS_TTL = 5

ZMQ_CONTROL_PORT = os.environ.get('ZMQ_CONTROL_PORT', 5559)
ZMQ_PORT_IN = os.environ.get('ZMQ_PORT_IN', 5557)
ZMQ_LOG_PORT = os.environ.get('ZMQ_LOG_PORT', 5558)
PC_CONTROLLER_PORT = os.environ.get('PC_CONTROLLER_PORT', 8083)
SERVICE_GATEWAY_PORT = os.environ.get('SERVICE_GATEWAY_PORT', 5007)
PERSISTENT_VOLUME_MOUNT = '/data'
ENV_VARS = [ZMQ_CONTROL_PORT, ZMQ_PORT_IN, ZMQ_LOG_PORT, PC_CONTROLLER_PORT]
ZMQ_SECONDARY_PORT = 5559
MAX_MSGS_PENDING = 1000

MAX_ID_LENGTH = int(os.environ.get("PINECONE_MAX_ID_LENGTH", default="64"))
MEMORY_UTILIZATION_LIMIT = float(os.environ.get("MEMORY_UTILIZATION_LIMIT", default="0.9"))
MEMORY_LIMIT_BYTES = MEMORY_UTILIZATION_LIMIT * get_container_memory_limit()


CPU_UNIT = 500
MEMORY_UNIT = 1875
DISK_UNIT = 5


class NodeType(str, enum.Enum):
    STANDARD = 'STANDARD'
    COMPUTE = 'COMPUTE'
    MEMORY = 'MEMORY'
    STANDARD2X = 'STANDARD2X'
    COMPUTE2X = 'COMPUTE2X'
    MEMORY2X = 'MEMORY2X'
    STANDARD4X = 'STANDARD4X'
    COMPUTE4X = 'COMPUTE4X'
    MEMORY4X = 'MEMORY4X'


NODE_TYPE_RESOURCES = {NodeType.STANDARD: {'memory': MEMORY_UNIT, 'cpu': CPU_UNIT, 'disk': DISK_UNIT},
                       NodeType.STANDARD2X: {'memory': 2 * MEMORY_UNIT, 'cpu': 2 * CPU_UNIT, 'disk': 2 * DISK_UNIT},
                       NodeType.STANDARD4X: {'memory': 4 * MEMORY_UNIT, 'cpu': 4 * CPU_UNIT, 'disk': 4 * DISK_UNIT},
                       NodeType.COMPUTE: {'memory': MEMORY_UNIT, 'cpu': 2 * CPU_UNIT, 'disk': DISK_UNIT},
                       NodeType.COMPUTE2X: {'memory': 2 * MEMORY_UNIT, 'cpu': 4 * CPU_UNIT, 'disk': DISK_UNIT * 2},
                       NodeType.COMPUTE4X: {'memory': 4 * MEMORY_UNIT, 'cpu': 8 * CPU_UNIT, 'disk': DISK_UNIT * 4},
                       NodeType.MEMORY: {'memory': 2 * MEMORY_UNIT, 'cpu': CPU_UNIT, 'disk': DISK_UNIT * 2},
                       NodeType.MEMORY2X: {'memory': 4 * MEMORY_UNIT, 'cpu': 2 * CPU_UNIT, 'disk': DISK_UNIT * 4},
                       NodeType.MEMORY4X: {'memory': 8 * MEMORY_UNIT, 'cpu': 4 * CPU_UNIT, 'disk': DISK_UNIT * 8}}

