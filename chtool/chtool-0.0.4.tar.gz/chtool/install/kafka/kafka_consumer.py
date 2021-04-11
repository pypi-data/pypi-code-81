
from kafka import KafkaConsumer

consumer = KafkaConsumer( bootstrap_servers=["172.16.16.4:9092"],
                          value_deserializer=lambda v: v.decode('utf-8') if v else None,
                         key_deserializer=lambda k:k.decode('utf-8') if k else None,
                          auto_offset_reset='earliest')
"""
auto_offset_reset    'smallest': 
                        'earliest',   #最开始
                        'largest':   
                        'latest'#当前最新

"""
consumer.subscribe(["test1","test_"])

for msg in consumer:
    key = msg
    value = msg
    print("%s-%d-%d key=%s value=%s" % (msg.topic, msg.partition, msg.offset, key, value))

#这是一个阻塞的过程，当生产者有消息传来的时候，就会读取消息，若是没有消息就会阻塞等待
#auto_offset_reset参数表示重置偏移量，有两个取值，latest表示读取消息队列中最新的消息，另一个取值earliest表示读取最早的消息。