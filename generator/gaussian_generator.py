from uuid import uuid4
from random import gauss
from datetime import datetime

TEMPERATURE_F_MEAN = 78
TEMPERATURE_F_SIGMA = 17
TEMPERATURE_F_DECIMALS = 2


def generate_reading():
    return {
        'id': str(uuid4()),
        'type': 'Sensor',
        'content': {
            'temperature_f': round(gauss(
                TEMPERATURE_F_MEAN, TEMPERATURE_F_SIGMA), TEMPERATURE_F_DECIMALS),
            'time_of_measurement': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        }
    }
