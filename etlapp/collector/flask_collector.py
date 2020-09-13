import logging
import signal
import sys
import time
from functools import partial
from json import dumps, load, loads

from flask import Flask, request
from flask.logging import create_logger
from jsonschema import ValidationError, validate
from . import schemas
from .. import config
from ..queuehelper import get_producer

ENSURE_KAFKA_DELIVERY_TIMEOUT = 10

app = Flask(__name__)
log = create_logger(app)
log.setLevel(config.LOG_LEVEL)
logging.basicConfig(level=config.LOG_LEVEL)

# Note to self: it is possible that in wsgi scenario it might be more
# efficient to move creation of KafkaProducer to actual route method
# to avoid unnecessary instansiations

producer = get_producer()


def signal_handler(sig, frame):
    log.info("Shutting down collector / Flushing the producer queue")
    producer.flush()
    sys.exit(0)


def handle_kafka_error(data, ex):
    log.error(
        'Kafka send faled (%s) record dropped: %s', ex, data)


@app.route('/' + config.PIPELINE_NAME, methods=['PUT'])
def receive_message():
    # TODO: Validation block could probably be done in attribute
    if config.PIPELINE_NAME not in schemas.data_schemas:
        log.warning(
            "Pipeline does not have a valid schema defined for validation purposes, " +
            "will proceed without validation")
    else:
        try:
            validate(instance=request.json,
                     schema=schemas.data_schemas[config.PIPELINE_NAME])
        except ValidationError:
            log.error("Invalid Request Payload Received: %s", request.json)
            return 'Invalid Request Payload', 400

    future = producer.send(
        config.PIPELINE_COLLECTED_DATA_QUEUE_TOPIC, request.json) \
        .add_errback(partial(handle_kafka_error, request.json))

    # Alternative method to error handing, requires try/except here
    # result = future.get(timeout=3)

    log.info("Data sent to kafka %s", request.json)
    return '', 200


@app.route('/hello', methods=['GET'])
def receive_hello():
    # TODO: Add data validation
    return 'rehlo', 200


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.run(debug=True)
