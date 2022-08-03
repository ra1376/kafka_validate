from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
from logzero import setup_logger 
from logzero import logger
import json
import pytz
from datetime import datetime
import datetime as dt
from pathlib import Path
import os

def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


def connect_kafka_producer(topic , producer_type):
    function_name = 'connect_kafka_producer'
    producer_conf = {'bootstrap.servers':'broker:29092', 
                    'acks':'all',
                    'batch.num.messages':1,
                    'queue.buffering.max.messages': 1
                    #'max.partition.fetch.bytes':
                    #'fetch.max.bytes':                        
            }
    try:
        logger.info(f'producer properties {producer_conf}')
        producer = Producer(producer_conf)
    except Exception as e:
        error_code=1
        logger.debug('Failed to connect to Producer')

    return producer

admin_client = AdminClient({'bootstrap.servers': 'broker:29092'})

# create topics
topics = ['input_topic', 'output_topic'] 
new_topics = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in topics]
#delete the already existing topics (input and target)
del_topics = admin_client.delete_topics(new_topics, operation_timeout=30)
for topic, f in del_topics.items():
    try:
        f.result()  # The result itself is None
        logger.info("Topic {} deleted".format(topic))
    except Exception as e:
        logger.info("Failed to delete topic {}: {}".format(topic, e))

fs = admin_client.create_topics(new_topics)

for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))


producer = connect_kafka_producer('input_topic','json')

home_dir = str(os.getcwd())
with open (home_dir+"/sample_data/sample_json.txt",'r') as r:
    for line in r:
        value  = str(line)
        json_val = json.loads(value)
        encoded_data = json.dumps(json_val).encode('utf-8')
        key = json_val['myKey']
        producer.produce(topic = "input_topic", key = str(key), value= encoded_data,callback=delivery_callback)
        producer.flush()


