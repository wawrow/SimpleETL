from .. import config
from ..queuehelper import get_producer, get_consumer
import importlib
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)


def main():
    datamap = importlib.import_module(
        config.PIPELINE_DATA_TRANSFORMATION_MODULE)
    log.info("Starting Data mapper %s" %
             config.PIPELINE_DATA_TRANSFORMATION_MODULE)
    consumer = get_consumer(config.PIPELINE_COLLECTED_DATA_QUEUE_TOPIC)
    producer = get_producer()
    log.debug("Data mapper connected to the Queue")
    for message in consumer:
        message = datamap.map(message.value)
        log.debug('Message consumed: {}'.format(message,))
        producer.send(
            config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC, value=message)
        consumer.commit()


if __name__ == "__main__":
    main()
