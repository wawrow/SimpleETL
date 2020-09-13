from datetime import datetime
from random import uniform
from uuid import uuid4

from .. import config


def generate_reading():
    """Generates Mock reading with random values usind normal distribution and
       TEMPERATURE_F_MEAN  TEMPERATURE_F_SIGMA TEMPERATURE_F_DECIMALS settings
    Returns:
        dict: {id:'', type:'', content: {temperature_f: '', time_of_measurement: ''}}
    """
    return {
        'id': str(uuid4()),
        'type': 'Sensor',
        'content': {
            'temperature_f': round(uniform(
                config.RANDOM_GENERATOR_TEMPERATURE_F_MIN,
                config.RANDOM_GENERATOR_TEMPERATURE_F_MAX),
                config.GENERATOR_TEMPERATURE_F_DECIMALS),
            'time_of_measurement': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        }
    }
