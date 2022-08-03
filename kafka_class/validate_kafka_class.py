#from setup_logger as l
from dataclasses import dataclass
from distutils.log import error
from gc import callbacks
import os
from socket import timeout
import sys
import yaml
from logzero import setup_logger 
from logzero import logger
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import json
import time
from dateutil import parser
import pytz
from datetime import datetime
import datetime as dt

__version__="0.0.1"
class validate_kafka_class:

    def __init__(self):
        
        #application
        self.target_ts = None
        self.force = None
        
        #Kafka
        self.kafka_settings={}
        self.kafka_broker = None
        self.kafka_cons_settings={}
        self.auto_commit_set = False
        self.auto_offset_reset = 'earliest'
        self.kafka_producer_poll = 0.0009
        self.kafka_prod_ack_flag = 'Y'
        #Global variables
        self.source_topic = None
        self.target_topic = None
        self.group_id = None
        self.process_flag = 'Y'
        self.check_topic_exists = 'False'
        p_dir = str(os.getcwd())

        settings_file = p_dir + '/config/config.yml'
        if os.path.exists(settings_file) is False:
            logger.debug(f'file does not exist, please check.')
            sys.exit(1)
        else:
            config_dict = yaml.safe_load(open(settings_file))
            self.kafka_broker = config_dict['kafka_broker']
            self.target_tz = config_dict['target_tz']
            self.force = config_dict['force_process']
            self.auto_commit_set = config_dict['auto_commit_set']
            self.auto_offset_reset = config_dict['auto_offset_reset']
            self.source_topic = config_dict['source_topic']
            self.target_topic = config_dict['target_topic']
            self.group_id = config_dict['group_id']
            self.process_flag = config_dict['process_flag']
            self.batch_num_messages = config_dict['batch_num_messages']
            self.queue_buffering_max_messages = config_dict['queue_buffering_max_messages']


    def msg_delivery_report(self, err, msg):
        """_summary_
            function to return message delivery report to topic
        Args:
        err (_type_): Error return
        msg (_type_): message
        """    
        function_name = "msg_delivery_report"
        if err is not None:
            logger.debug(f'Message failed to deliver:{format(err)}')
            logger.debug(f'topic_name:{msg.topic()}')
            logger.debug(f'value: {format(msg.value())}')
        else:
            logger.info("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

    def check_topic_exists(self, topic):
        """_summary_
        Method is used to check topic availability
        Args:
            topic (_type_): _description_
        """
        pass
    
    def process_consumed_messages(self, message, topic_to_write, process):
        function_name = 'process_consumed_messages'
        target_tz = self.target_tz
        consumed_msg = str(message)
        get_values = json.loads(consumed_msg)
        msg_key = get_values['myKey']
        timestamp_value = get_values['myTimestamp']
        if timestamp_value is None or timestamp_value == '':
            logger.info(f'found key with empty timestamp values {msg_key}')
        else:
            date_parsed = parser.isoparse(timestamp_value)
            tz = pytz.timezone(target_tz)
            target_tz_ts = date_parsed.astimezone(tz)
            #converting to ISO 8601
            iso_time = target_tz_ts.isoformat()
            json_dict = {}
            json_dict['myKey'] = msg_key
            json_dict['myTimestamp'] = iso_time
            json_msg = json.dumps(json_dict)
            return json_msg
    
    def connect_kafka_producer(self, topic , producer_type):
        function_name = 'connect_kafka_producer'
        logger.info(f'connecting function {function_name}')
        producer_conf = {'bootstrap.servers':self.kafka_broker, 
                         'acks':'all',
                         'batch.num.messages':self.batch_num_messages,
                         'queue.buffering.max.messages':self.queue_buffering_max_messages
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

    def write_kafka_producer(self,topic,key,producer_type, str_json):
        function_name="write_kafka_producer"
        global total_rec
        start_time = time.time()
        kafka_producer_acknowledgement = self.kafka_prod_ack_flag
        local_start = time.perf_counter()
        prd = self.connect_kafka_producer(topic, producer_type)
        if producer_type == 'json':
            key_data= key
            val_json = json.loads(str(str_json))
            sr_data = val_json
        try:
            if kafka_producer_acknowledgement == 'Y':
                prd.produce(topic = topic, key = key_data, value=str(sr_data), callback=self.msg_delivery_report)
                prd.flush()
            else:
                prd.produce(topic = topic, key = key_data, value=sr_data)
                prd.flush()
        except BufferError as ke:
            logger.debug('Buffer error while sending log to Kafka')
            queue_flush=prd.flush()
            while queue_flush > 0:
                prd.flush()
        except Exception as e:
            logger.debug(f'Failed to produce messages. {e}')

        local_end = time.perf_counter
        #logger.info(f'start time of process = {round(local_start, 0)}')
        #logger.info(f'end time of process = {round(local_end, 0)}')

    def connect_consumer_kafka(self, topic, group_id):
        function_name = 'connect_consumer_kafka'
        logger.debug('connecting Kafka Consumer')
        error_code = 0
        consumer = 0
        #check_for_topic = self.check_topic_exists(topic)
        consumer_conf = {'bootstrap.servers':self.kafka_broker, 
                         'group.id':self.group_id,
                         'enable.auto.commit': self.auto_commit_set,
                         'auto.offset.reset': self.auto_offset_reset
                         #'max.partition.fetch.bytes':
                         #'fetch.max.bytes':                        
                    }
        try:
            consumer = Consumer(consumer_conf)
        except Exception as e:
            consumer  = 0
            logger.debug(f'Error in connecting Kafka Consumer{e}')
        return consumer
    
    
    def read_consumer_kafka(self, topic, group_id, process_flag):
        function_name = 'write_consumer_kafka'
        logger.debug('processing consumed messages')
        consumer = 0
        process = self.force
        consumer = self.connect_consumer_kafka(topic, group_id)
        continue_running = True
        msg_count = 0
        min_commit_count = 1000
        try:
            consumer.subscribe([topic])
            while continue_running:
                msg = consumer.poll(timeout=1.0)
                if msg is None: continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug(f'Reached end at offset {msg.topic()},{msg.partition()},{msg.offset()}')
            
                    elif msg.error():
                        logger.debubg(f'Kafka Execption ocurred {msg.error}')
                        raise KafkaException(msg.error())
                else:
                    value = self.process_consumed_messages(msg.value().decode('utf8').replace("'", '"'),msg.topic(), 'YES')
                    msg_count += 1
                    logger.info("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                    if msg_count % min_commit_count == 0:
                        consumer.commit(asynchronous=False)
                    
                    if self.process_flag == 'Y':
                        logger.info(f'processing processed messages to target_topic for incorrect timestamp values to topic : {self.target_topic}')
                        if value is None or value == '':
                            logger.info("empty value for myTimestamp, ignoring and not writing the key to target topic")
                        else:
                            processed_value = value
                            value_key = msg.key().decode('utf-8')
                            logger.info(processed_value)
                           #json_val = json.dumps(processed_value)
                           #print(json_val)
                            target_topic = self.target_topic
                            self.write_kafka_producer(target_topic,value_key,'json',processed_value)
                            logger.info('processed messages to Kafka target topic')
                        

        except Exception as ex:
            logger.debug(f'Error while trying to consume from kafka{ex}')

        finally:
            consumer.close()
            continue_running = False

