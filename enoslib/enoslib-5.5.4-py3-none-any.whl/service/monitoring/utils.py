from contextlib import ContextDecorator
import logging
import queue
import socket
import threading
import time
from typing import Union

logger = logging.getLogger(__name__)


_emitter_lock = threading.Lock()
# Keep track of the api client
_emitter_instance = None


def get_emitter():
    with _emitter_lock:
        global _emitter_instance
        if not _emitter_instance:
            _emitter_instance = TelegrafEmitter()
            _emitter_instance.start()
        return _emitter_instance


class Measurement(object):
    def __init__(self, name: str):
        self.name = name
        self.tags = []
        self.fields = []
        self.timestamp = time.time_ns()

    def add_tags(self, **kwargs) -> "Measurement":
        for name, value in kwargs.items():
            self.tags.append((name, value))
        return self

    def add_fields(self, **kwargs) -> "Measurement":
        for name, value in kwargs.items():
            self.fields.append((name, value))
        return self

    def finalize(self):
        if not self.fields:
            raise ValueError("At least one field must be set")

    def __repr__(self):
        return f"<Measurement {str(self)}"

    def __str__(self):
        tags_str = ",".join([f"{name}={value}" for name, value in self.tags])
        field_str = ",".join([f"{name}={value}" for name, value in self.fields])
        return f"{self.name} {tags_str} {field_str} {self.timestamp}"


class timeit(ContextDecorator):
    def __init__(self, key: str, **kwargs):
        self.key = key
        self.tags = kwargs
        self.emitter = get_emitter()

    def __enter__(self):
        self.measurement = Measurement(self.key)
        self.measurement.add_tags(**self.tags)
        self.start = time.time()

    def __exit__(self, *exc):
        duration = time.time() - self.start
        self.measurement.add_fields(duration=duration)
        self.emitter.push(self.measurement)
        return duration


class TelegrafEmitter(threading.Thread):
    def __init__(self):
        logger.debug("reating a TelegrafEmitter instance")
        super().__init__(daemon=True)
        self.queue = queue.Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def push(self, value):
        self.queue.put(value)

    def run(self):
        while True:
            measurement = self.queue.get()
            try:
                logger.debug(f"Sending {measurement} over the socket")
                self.sock.sendto(str(measurement).encode(), ("localhost", 8125))
            except Exception as e:
                logger.error(e)
