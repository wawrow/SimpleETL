from json import dumps, loads

from kafka import KafkaConsumer, KafkaProducer

from temp_reading import map as datamap

TOPIC = "testtopic123"


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=['localhost:9094'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers=['localhost:9094'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


for message in consumer:
    message = datamap(message.value)
    print('Message consumed: {}'.format(message,))
    producer.send(TOPIC+'.transformed', value=message)
