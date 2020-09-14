from etlapp.datamapper import temperatures_mapper
from datetime import datetime

data_fixture_32f = {
    'id': 'test',
    'type': 'Sensor',
    'content': {
            'temperature_f': 32.0,
            'time_of_measurement': datetime(2020, 1, 1, 12, 00)
    }
}

data_fixture_212f = data_fixture_32f.copy()
data_fixture_212f.update({'content': {'temperature_f': 212}})


def test_data_conversion_f_to_c_32f(mocker):
    result = temperatures_mapper.map(data_fixture_32f)
    assert 'temperature_c' in result['content']
    assert 0 == result['content']['temperature_c']


def test_data_conversion_f_to_c_212f(mocker):
    result = temperatures_mapper.map(data_fixture_212f)
    assert 'temperature_c' in result['content']
    assert 100 == result['content']['temperature_c']
