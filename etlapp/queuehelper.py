from kafka import KafkaConsumer, KafkaProducer, errors
import time
import logging
from . import config
from json import dumps, loads

log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)


def get_producer(retries=None, retrydelay=1):
    """Obtain producer for the queue, will retry until broker is accessible
    Warning: if retries are set to None this method will block the execution of the script.
    Args:
        retries ([type], optional): None for indifinete retries. Defaults to None.
        retrydelay (int, optional): Delay between retries. Defaults to 1.

    Raises:
        error: NoBrokersAvailable if unable to connect in desired retries

    Returns:
        KafkaProducer: 
    """
    i = 0
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=config.KAFKA_BROKERS,
                                     value_serializer=lambda x:
                                     dumps(x).encode('utf-8'))
            return producer
        except errors.NoBrokersAvailable as error:
            log.warning("NoBrokersAvailable: Retrying")
            time.sleep(retrydelay)
            if retries is None:
                continue
            i = i+1
            if i >= retries:
                raise error


def get_consumer(topic, retries=None, retrydelay=1):
    """Obtain consumer for the queue, will retry until broker is accessible
    Warning: if retries are set to None this method will block the execution of the script.

    Args:
        topic ([type]): [description]
        retries ([type], optional): [description]. Defaults to None.
        retrydelay (int, optional): [description]. Defaults to 1.

    Raises:
        error: NoBrokersAvailable if unable to connect in desired retries

    Returns:
        KafkaConsumer: 
    """
    i = 0
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=config.KAFKA_BROKERS,
                group_id=config.PIPELINE_NAME,
                enable_auto_commit=False,
                value_deserializer=lambda x: loads(x.decode('utf-8')))
            return consumer
        except errors.NoBrokersAvailable as error:
            log.warning("NoBrokersAvailable: Retrying")
            time.sleep(retrydelay)
            if retries is None:
                continue
            i = i+1
            if i >= retries:
                raise error
