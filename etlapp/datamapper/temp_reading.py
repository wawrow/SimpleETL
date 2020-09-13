DECIMALS = 2


def map(data):
    data['content'].update({
        'temperature_c': round((data['content']['temperature_f'] - 32) * 5.0/9.0, DECIMALS)
    })
    return data
