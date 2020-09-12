import json
import logging

import requests

log = logging.getLogger(__name__)


class Emitter:
    def __init__(self, endpoint_config):
        assert 'Url' in endpoint_config
        self.Url = endpoint_config['Url']
        self.Method = 'PUT'

    def send_message(self, payload):
        headers = {'Content-Type': 'application/json'}
        log.info('Sending request Url %s', self.Url)
        log.debug('headers: %s, payload: %s', headers, payload)
        response = requests.put(
            self.Url, data=json.dumps(payload), headers=headers)
        log.debug('Response received: %s', response)
