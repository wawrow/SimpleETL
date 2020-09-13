# This file contain schemas for validation of the incoming data, key corresponds to the pipeline name

data_schemas = {
    'temperatures': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string'
            },
            'type': {
                'type': 'string'
            },
            'content': {
                'type': 'object',
                'properties': {
                    'temperature_f': {
                        'type': 'number'
                    },
                    'time_of_measurement': {
                        'type': 'string'
                    }
                }
            }
        }
    }
}
