from kafka import KafkaConsumer, KafkaProducer, TopicPartition
import json


def producerKaf(host, topic, value):
    def json_serialize(data):
        return json.dumps(data).encode("utf-8")

    kafka_ver = (0, 10)
    producer = KafkaProducer(bootstrap_servers=[host],
                             api_version=kafka_ver,
                             value_serializer=json_serialize)

    data = value
    msg = producer.send(topic, data)
    msg.get(timeout=30)
    producer.close(timeout=10)


def consumerKaf(host, topic):
    kafka_ver = (0, 10)
    consumer = KafkaConsumer(bootstrap_servers=[host],
                             auto_offset_reset='earliest',
                             api_version=kafka_ver)

    topic_partition = TopicPartition(topic, 0)
    assigned_topic = [topic_partition]
    consumer.assign(assigned_topic)
    consumer.poll()

    for msg in consumer:
        return msg.value
