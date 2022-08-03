from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
from logzero import setup_logger 
from logzero import logger
import json
import pytz
from datetime import datetime
import datetime as dt
from pathlib import Path
from kafka_class.validate_kafka_class import validate_kafka_class 
import sys

def main():
    try:
        consumer_class = validate_kafka_class()
        consumer_class.read_consumer_kafka(consumer_class.source_topic,consumer_class.group_id,consumer_class.process_flag )
    except Exception as e:
        logger = setup_logger('validate_kafka_class')
        logger.debug('failed to connect to Kafka , please check configration')
        sys.exit(1)




if __name__ == "__main__":
    logger.info('Starting to process Kafka messages for filtering out incorrect timestamps')
    main()