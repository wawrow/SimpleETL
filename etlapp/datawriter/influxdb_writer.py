import logging

from influxdb import InfluxDBClient

from .. import config
from ..queuehelper import get_consumer

log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)


def temperature_to_influx(data):
    return {
        "measurement": "temperature_readings",
        "tags": {
            "type": data['type'],
            "region": "us-west"
        },
        "time": data['content']['time_of_measurement'],
        "fields": {
            "id": data['id'],
            "temperature_f": data['content']["temperature_f"],
            "temperature_c": data['content']["temperature_c"]
        }
    }


influx_record_conversion = {
    'temperatures': temperature_to_influx
}


def main():

    log.info('Starting InfluxDB writer for topic %s ',
             config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC)

    if config.PIPELINE_NAME not in influx_record_conversion:
        raise Exception(
            "Data to Influx DB data point conversion missing for data: %s" % config.PIPELINE_NAME)

    consumer = get_consumer(config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC)
    client = InfluxDBClient(config.INFLUXDB_HOST, config.INFLUXDB_PORT,
                            config.INFLUXDB_USERNAME, config.INFLUXDB_PASSWORD,
                            config.PIPELINE_NAME)

    log.debug("Connected to the topic.")

    # Note to self: This is potentially candidate for batch uploads, pending perforfmance testing
    for message in consumer:
        client.write_points(
            [influx_record_conversion[config.PIPELINE_NAME](message.value)])
        log.debug('Message consumed and written to the DB: %s', message)
        consumer.commit()

if __name__ == "__main__":
    main()