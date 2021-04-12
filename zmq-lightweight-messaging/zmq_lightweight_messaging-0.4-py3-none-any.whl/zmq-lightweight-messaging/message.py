import datetime
import subprocess
import logging
import zmq
from uuid import uuid4
import json

class Message:
    def __init__(self, service):
        # logging configuration
        self.service = service
        self.logfile = "/home/siddharth/Documents/"+str(self.service)+".log"
        self.logging = logging
        self.logging.basicConfig(filename=self.logfile, level=logging.INFO, format="[%(asctime)s]-[%(levelname)s]-%(message)s", datefmt="%d-%b-%y %H:%M:%S")

        # 0MQ configuration
        self.context = zmq.Context()
        self.sink = self.context.socket(zmq.PUSH)
        self.sink.connect("tcp://localhost:5558")

        self.start_time = datetime.datetime.now()


    # function to format the output from subprocess pipe
    def format_out(self, std_out):
        std_out = std_out.decode("utf-8")
        std_out = std_out.split("\n")
        std_out = list(filter(None, std_out))

        return std_out

    
    def close(self, job_name, status, comment, last_successful):
        end_time = datetime.datetime.now()

        json_body = [{
            "measurement": self.service,
            "tags": {
                "backup": self.service
            },
            "time": str(datetime.datetime.now()),
            "fields": {
                "uuid": str(uuid4()),
                "jobName": job_name,
                "startTime": str(self.start_time),
                "endTime": str(end_time),
                "status": status,
                "comment": comment,
                "lastSuccessful": str(last_successful)
            }
        }]

        self.sink.send_json(json_body)
        self.sink.close()
        self.context.term()