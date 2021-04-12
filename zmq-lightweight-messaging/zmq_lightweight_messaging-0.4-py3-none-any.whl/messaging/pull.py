import sys
import time
import zmq
import json
from influx_client import InfluxClient

context = zmq.Context()
# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

# Setup influx
client = InfluxClient(db="backup_status")
client.init_db()

while True:
    json_body = receiver.recv()
    json_body = json_body.decode("utf-8")
    json_body = eval(json_body)
    print(json_body)
    client.insert(json_body)