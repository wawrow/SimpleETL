
import pytest
from datetime import datetime
from generator import gaussian_generator
from generator import random_generator

generators = [gaussian_generator, random_generator]


@pytest.mark.parametrize('tested_generator', generators)
class TestValidateGenerator:

    def test_gaussian_generator_result_format(self, tested_generator):
        reading = tested_generator.generate_reading()
        assert 'id' in reading
        assert 'type' in reading
        assert 'content' in reading
        assert 'temperature_f' in reading['content']
        assert 'time_of_measurement' in reading['content']

    def test_gaussian_generator_date_format(self, mocker, tested_generator):
        dtmock = mocker.patch(tested_generator.__name__ + '.datetime')
        dtmock.utcnow.return_value = datetime(
            2012, 1, 2, 1, 1, 1)
        reading = tested_generator.generate_reading()
        assert reading['content']['time_of_measurement'] == '2012-01-02T01:01:01'

    def test_gaussian_generator_types(self, tested_generator):
        reading = gaussian_generator.generate_reading()
        assert isinstance(reading['id'], str)
        assert isinstance(reading['type'], str)
        assert isinstance(reading['content']['time_of_measurement'], str)
        assert isinstance(reading['content']['temperature_f'],  (int, float))
