import requests
import json
import logging

log = logging.getLogger(__name__)


class HttpEmitter:
    def __init__(self, endpoint_config):
        assert 'Url' in endpoint_config
        self.Url = endpoint_config['Url']
        self.Method = 'PUT'

    def send_message(self, payload):
        headers = {'Content-Type': 'application/json'}
        log.info(
            f'Sending request Url {self.Url}')
        log.debug(f'headers: {headers}, payload: {payload}')
        response = requests.put(
            self.Url, data=json.dumps(payload), headers=headers)
        log.debug(f'Response received: {response}')
