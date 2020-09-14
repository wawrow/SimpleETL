import logging
from functools import partial
from json import loads
from json.decoder import JSONDecodeError

import paho.mqtt.client as mqtt
from jsonschema import ValidationError, validate

from .. import config, queuehelper
from . import schemas

log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)


def on_connect(client, userdata, flags, rc):
    log.info("Connected to the mqtt broker result: %s ", rc)
    client.subscribe(config.PIPELINE_NAME)


def handle_kafka_error(data, ex):
    log.error(
        'Kafka send faled (%s) record dropped: %s', ex, data)


def on_message(producer, client, userdata, msg):
    log.info("MQTT message received on topic %s", msg.topic)
    try:
        data = loads(msg.payload)
        log.debug("Data parsed correctly from json %s", data)
        if config.PIPELINE_NAME in schemas.data_schemas:
            validate(instance=data,
                     schema=schemas.data_schemas[config.PIPELINE_NAME])
        else:
            log.warning(
                "Pipeline does not have a valid schema defined for validation purposes, " +
                "will proceed without validation in good faith.")
        log.debug("About to send message here: %s", producer)
        future = producer.send(config.PIPELINE_COLLECTED_DATA_QUEUE_TOPIC, data) \
            .add_errback(partial(handle_kafka_error, data))
        log.debug("Data sento onto the queue, result %s", future)
    except JSONDecodeError:
        log.error("Data received is not a valid JSON format (%s)",
                  msg.payload)
    except ValidationError:
        log.error("Invalid Request Payload Received: %s", msg.payload)
    except Exception as ex:  # pylint: disable=broad-except
        log.exception(ex)


if __name__ == "__main__":
    producer = queuehelper.get_producer()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = partial(on_message, producer)
    client.connect(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT, 60)
    client.loop_forever()
