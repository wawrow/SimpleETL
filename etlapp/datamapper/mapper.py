from .. import config
from ..queuehelper import get_producer, get_consumer
import importlib
import logging

log = logging.getLogger(__name__)
# logging.basicConfig(level=config.LOG_LEVEL)
logging.basicConfig(level=logging.ERROR)

log.info("Starting Data mapper %s" %
         config.PIPELINE_DATA_TRANSFORMATION_MODULE)

datamap = importlib.import_module(config.PIPELINE_DATA_TRANSFORMATION_MODULE)

consumer = get_consumer(config.PIPELINE_COLLECTED_DATA_QUEUE_TOPIC)
producer = get_producer()

log.debug("Data mapper connected to the Queue")

for message in consumer:
    message = datamap.map(message.value)
    log.debug('Message consumed: {}'.format(message,))
    producer.send(config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC, value=message)
    consumer.commit()

# ConsumerRecord(topic='CollectedTemperatureData', partition=0, offset=3601, timestamp=1600036121820,
# timestamp_type=0, key=None,
# value={'id': '9a975be9-643c-41b1-b729-e57bd8bc059d', 'type': 'Sensor', 'content': {'temperature_f': 66.81, 'time_of_measurement': '2020-09-13T22:28:41'}}, headers=[],
# checksum=None, serialized_key_size=-1, serialized_value_size=147, serialized_header_size=-1)
