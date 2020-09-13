import json
import logging

import requests
from .. import config

log = logging.getLogger(__name__)

# TODO: Should this be class?


class Emitter:
    def __init__(self, endpoint_config):
        self.Url = endpoint_config.get('Url', config.REST_EMITTER_URL)
        self.Method = 'PUT'

    def send_message(self, payload):
        headers = {'Content-Type': 'application/json'}
        log.info('Sending request Url %s', self.Url)
        log.debug('headers: %s, payload: %s', headers, payload)
        response = requests.put(
            self.Url, data=json.dumps(payload), headers=headers)
        log.debug('Response received: %s', response)
