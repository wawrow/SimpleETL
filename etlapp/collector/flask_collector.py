import logging
import sys
import time
from functools import partial, wraps
from json import dumps, load, loads

from flask import Flask, g, request
from flask.logging import create_logger
from jsonschema import ValidationError, validate

from .. import config, queuehelper
from . import schemas

ENSURE_KAFKA_DELIVERY_TIMEOUT = 10

app = Flask(__name__)
log = create_logger(app)
log.setLevel(config.LOG_LEVEL)
logging.basicConfig(level=config.LOG_LEVEL)


def get_producer():
    '''Singleton like access to producer coming from App Context
    Returns:
        KafkaProducer: 
    '''
    if 'producer' not in g:
        log.info("Connecting to the Queue")
        g.producer = queuehelper.get_producer()
    return g.producer


@app.teardown_appcontext
def teardown_producer(*args):
    producer = g.pop('producer', None)
    if producer is not None:
        log.info("Closing the Queue")
        producer.flush()
        producer.close()


def handle_kafka_error(data, ex):
    log.error(
        'Kafka send faled (%s) record dropped: %s', ex, data)


def validate_request_json_schema(schema_name):
    def decorator_wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if schema_name not in schemas.data_schemas:
                log.warning(
                    "Pipeline does not have a valid schema defined for validation purposes, " +
                    "will proceed without validation in good faith.")
            else:
                try:
                    validate(instance=request.json,
                             schema=schemas.data_schemas[schema_name])
                except ValidationError:
                    log.error("Invalid Request Payload Received: %s",
                              request.json)
                    # TODO: see if there is better code than 400
                    return 'Invalid Request Payload', 400
            return func(*args, **kwargs)
        return decorated_function
    return decorator_wrapper


@app.route('/' + config.PIPELINE_NAME, methods=['PUT'])
@validate_request_json_schema(config.PIPELINE_NAME)
def receive_message():

    get_producer().send(
        config.PIPELINE_COLLECTED_DATA_QUEUE_TOPIC, request.json) \
        .add_errback(partial(handle_kafka_error, request.json))

    # Alternative method to error handing to add_errback, would require try/except here - more LOC
    # result = future.get(timeout=3)

    log.info("Data sent to the queue %s", request.json)
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
