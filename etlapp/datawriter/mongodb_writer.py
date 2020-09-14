import logging
from json import dumps, loads

import pymongo

from .. import config
from ..queuehelper import get_consumer

log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)

def main():

    log.info('Starting InfluxDB writer for topic %s ',
             config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC)

    consumer = get_consumer(config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC)
    client = pymongo.MongoClient(config.MONGODB_URL)
    db = client[config.MONGODB_DB]
    collection = db[config.PIPELINE_NAME]
    log.info("Connected to MongoDB.")

    # Note to self: This is potentially candidate for batch uploads, pending perforfmance testing
    for message in consumer:
        log.info("Message from the queue received")
        collection.insert_one(message.value)
        log.debug('Message consumed and written to the DB: %s', message)
        consumer.commit()

if __name__ == "__main__":
    main()
