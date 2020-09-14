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
