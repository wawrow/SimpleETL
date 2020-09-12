
from json import dumps, loads

from influxdb import InfluxDBClient
from kafka import KafkaConsumer

TOPIC = "testtopic123.transformed"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=['localhost:9094'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'temperatures')

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
    print('Message consumed: {}'.format(message,))
