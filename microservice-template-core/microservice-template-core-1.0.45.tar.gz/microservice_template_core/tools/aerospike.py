import aerospike
from microservice_template_core.tools.logger import get_logger
from microservice_template_core.settings import AerospikeConfig
from prometheus_client import Summary

logger = get_logger()


class AerospikeClient(object):
    # Prometheus Metrics
    AEROSPIKE_CONNECTIONS = Summary('aerospike_connections_latency_seconds', 'Time spent processing connect to aerospike')
    AEROSPIKE_READ = Summary('aerospike_read_latency_seconds', 'Time spent processing read from aerospike')
    AEROSPIKE_WRITE = Summary('aerospike_write_latency_seconds', 'Time spent processing write to aerospike')
    AEROSPIKE_SCAN = Summary('aerospike_scan_latency_seconds', 'Time spent processing scan in aerospike')

    def __init__(self):
        self.client = self.client_aerospike()

    @staticmethod
    @AEROSPIKE_CONNECTIONS.time()
    def client_aerospike():
        config = {
            'hosts': [(AerospikeConfig.AEROSPIKE_HOST, AerospikeConfig.AEROSPIKE_PORT)]
        }

        try:
            client = aerospike.client(config).connect()
            logger.info(msg=f"Connected to Aerospike - {config['hosts']}")
        except Exception as err:
            client = None
            logger.error(msg=f"failed to connect to the cluster with: {err} - {config['hosts']}")

        return client

    @AEROSPIKE_WRITE.time()
    def put_message(self, aerospike_set, aerospike_key, aerospike_message):
        key = (AerospikeConfig.AEROSPIKE_NAMESPACE, aerospike_set, aerospike_key)
        try:
            logger.info(msg=f"Add message to Aerospike: KEY - {key}")
            self.client.put(key, aerospike_message)
        except Exception as e:
            logger.error(msg=f"error: {e}")

    @AEROSPIKE_READ.time()
    def read_message(self, aerospike_set, aerospike_key):
        try:
            logger.info(msg=f'Read data from Aerospike. KEY - {aerospike_key}, SET - {aerospike_set}')
            key = (AerospikeConfig.AEROSPIKE_NAMESPACE, aerospike_set, aerospike_key)
            (key, metadata, record) = self.client.get(key)
        except Exception as err:
            logger.error(msg=f"Can`t read data from Aerospike. Return empty list of notifications for key - {aerospike_key}\nError: {err}")
            return []

        return record

    @AEROSPIKE_SCAN.time()
    def scan_keys(self, aerospike_set):
        s = self.client.scan(AerospikeConfig.AEROSPIKE_NAMESPACE, aerospike_set)
        records = []

        # callback to be called for each record read
        def callback(input_tuple):
            (_, _, record) = input_tuple
            records.append(record)
            return records

        # invoke the operations, and for each record invoke the callback
        s.foreach(callback)

        return records


# aerospike_client = AerospikeClient()
# aerospike_client.scan_keys('aggr_notifications')
# aerospike_client.put_message('aerospike_set', 'my_key', {'name': 'aer', 'test': 2, 'olol': 12})
# print(json.dumps(aerospike_client.read_message('aggr_notifications', '1000___voice___active___notifications')))

