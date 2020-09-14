import json
import logging

import paho.mqtt.client as mqtt

from .. import config

log = logging.getLogger(__name__)
logging.basicConfig(level=config.LOG_LEVEL)


class Emitter:
    def __init__(self, endpoint_config):
        self.Host = endpoint_config.get(
            'MQTT_BROKER_HOST', config.MQTT_BROKER_HOST)
        self.Port = endpoint_config.get(
            'MQTT_BROKER_PORT', config.MQTT_BROKER_PORT)
        self.client = mqtt.Client()
        self.client.connect(self.Host, self.Port, 60)
        self.client.loop_start()

    def send_message(self, payload):
        log.info('Sending MQTT Message to %s:%s', self.Host, self.Port)
        self.client.publish(config.PIPELINE_NAME, payload=json.dumps(payload))
        log.debug('Message processed to the broker')


# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#     # client.subscribe("$SYS/#")
#     client.publish(config.PIPELINE_NAME, payload="test", qos=0, retain=False)

# The callback for when a PUBLISH message is received from the server.


# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
