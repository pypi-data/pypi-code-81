from kafka import KafkaConsumer
import time

#消费者群组中有一个group_id参数，

consumer = KafkaConsumer(group_id="test1", bootstrap_servers=["172.16.16.4:9092"],
                          value_deserializer=lambda v: v.decode('utf-8') if v else None,
                         key_deserializer=lambda k:k.decode('utf-8') if k else None,
                          auto_offset_reset='latest')

consumer.subscribe(["test1","test*"])
for msg in consumer:
    key = msg
    value = msg
    print("%s-%d-%d key=%s value=%s" % (msg.topic, msg.partition, msg.offset, key, value))