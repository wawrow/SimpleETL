from uuid import uuid4
from random import uniform
from datetime import datetime

TEMPERATURE_F_MIN = 32
TEMPERATURE_F_MAX = 212
TEMPERATURE_F_DECIMALS = 2


def generate_reading():
    return {
        'id': str(uuid4()),
        'type': 'Sensor',
        'content': {
            'temperature_f': round(uniform(
                TEMPERATURE_F_MIN, TEMPERATURE_F_MAX), TEMPERATURE_F_DECIMALS),
            'time_of_measurement': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        }
    }
