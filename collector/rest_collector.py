from functools import partial
from json import dumps, loads

from flask import Flask, request
from kafka import KafkaProducer, errors

TOPIC = "testtopic123"
ENSURE_KAFKA_DELIVERY_TIMEOUT = 10

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers=['localhost:9094'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


def handle_kafka_error(data, ex):
    app.logger.error(
        'Kafka send faled (%s) record dropped: %s', ex, data)


@app.route('/', methods=['PUT'])
def receive_message():
    # TODO: Add data validation
    producer.send(TOPIC, request.json).add_errback(
        partial(handle_kafka_error, request.json))
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
