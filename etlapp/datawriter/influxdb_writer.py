
import logging
from json import dumps, loads

from influxdb import InfluxDBClient
from ..queuehelper import get_consumer

from .. import config

log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)
print('a')

log.info('Starting InfluxDB writer for topic %s ' %
         config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC)

consumer = get_consumer(config.PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC)
client = InfluxDBClient(config.INFLUXDB_HOST, config.INFLUXDB_PORT,
                        config.INFLUXDB_USERNAME, config.INFLUXDB_PASSWORD,
                        config.PIPELINE_NAME)

log.debug("Connected to the topic.")

for message in consumer:
    message = message.value
    client.write_points([
        {
            "measurement": "temperature_readings",
            "tags": {
                "type": message['type'],
                "region": "us-west"
            },
            "time": message['content']['time_of_measurement'],
            "fields": {
                "id": message['id'],
                "temperature_f": message['content']["temperature_f"],
                "temperature_c": message['content']["temperature_c"]
            }
        }
    ]
    )
    log.debug('Message consumed and written to the DB: {}'.format(message,))
    consumer.commit()
