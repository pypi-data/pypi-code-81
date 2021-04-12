import sys
import json
import requests
from kafka import KafkaConsumer, TopicPartition
import multiprocessing as mp
from queue import Queue


def create_consumer(bootstrap_servers: str, topic: str, partition: int):
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
    consumer.assign([TopicPartition(topic, partition)])
    return consumer


def create_worker_queue(n_worker: int):
    worker_queue = Queue(n_worker)
    for i in range(n_worker):
        worker_queue.put(i)
    return worker_queue


def get_next_worker(worker_queue: Queue):
    next_worker = worker_queue.get()
    worker_queue.put(next_worker)
    return next_worker, worker_queue


def multiprocess_kafka_consumer(
    input_topic: str,
    partition: int,
    n_worker: int,
    bootstrap_servers: str,
    callable_function,
):
    consumer = utils.create_consumer(bootstrap_servers, input_topic, partition)
    message_queue = [mp.Manager().Queue() for i in range(n_worker)]
    worker_queue = utils.create_worker_queue(n_worker)

    for i in range(n_worker):
        worker = mp.Process(
            target=callable_function,
            args=(message_queue[i],),
        )
        worker.daemon = True
        worker.start()

    for message in consumer:
        next_worker, worker_queue = utils.get_next_worker(worker_queue)
        message_queue[next_worker].put(message)
