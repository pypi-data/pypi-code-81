from kafka import KafkaProducer
import time

"""
##########################################################################################################

topic (str) ##指定向哪个主题发送消息。
value (optional)  ##value为要发送的消息值，必须为bytes类型，如果这个值为空，则必须有对应的key值，并且空值被标记为删除。可以通过配置value_serializer参数序列化为字节类型。
key (optional) ##key与value对应的键值，必须为bytes类型。kafka根据key值确定消息发往哪个分区（如果分区被指定则发往指定的分区），具有相同key的消息被发往同一个分区，如果key
               ##为NONE则随机选择分区，可以使用key_serializer参数序列化为字节类型。
               
headers (optional)  ##键值对的列表头部，列表项是str(key)和bytes(value)。
timestamp_ms (int, optional) – #时间戳

##########################################################################################################


"""


producer = KafkaProducer(bootstrap_servers=["172.16.16.4:9092"],
                         value_serializer=lambda v: v.encode('utf-8') if v else None,
                         key_serializer=lambda k:k.encode('utf-8') if k else None)

total = 20
for i in range(total):
    i += 1
    msg = "producer1+%d" % i
    print(msg)
    print(msg.encode('utf-8'))
    # future=producer.send('test1', key=bytes(str(i)), value=msg.encode('utf-8'))
    future=producer.send('test1', key="nihao", value="sss")
    time.sleep(1)
    future.get(timeout=60)

producer.close()