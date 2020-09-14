from ..config import GENERATOR_TEMPERATURE_C_DECIMALS


def map(data):
    data['content'].update({
        'temperature_c': round((data['content']['temperature_f'] - 32) * 5.0/9.0, GENERATOR_TEMPERATURE_C_DECIMALS)
    })
    return data
