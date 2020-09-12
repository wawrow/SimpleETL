
import importlib
import pkgutil
from datetime import datetime

import pytest

import datagenerator

generators = [importlib.import_module('datagenerator.' + name) for _, name, _ in pkgutil.iter_modules(
    datagenerator.__path__) if name.endswith('_generator')]


@ pytest.mark.parametrize('tested_generator', generators)
class TestValidateGenerator:

    def test_generator_has_generate_reading(self, tested_generator):
        assert 'generate_reading' in dir(tested_generator)

    def test_generator_result_format(self, tested_generator):
        reading = tested_generator.generate_reading()
        assert 'id' in reading
        assert 'type' in reading
        assert 'content' in reading
        assert 'temperature_f' in reading['content']
        assert 'time_of_measurement' in reading['content']

    def test_generator_date_format(self, mocker, tested_generator):
        dtmock = mocker.patch(tested_generator.__name__ + '.datetime')
        dtmock.utcnow.return_value = datetime(
            2012, 1, 2, 1, 1, 1)
        reading = tested_generator.generate_reading()
        assert reading['content']['time_of_measurement'] == '2012-01-02T01:01:01'

    def test_generator_types(self, tested_generator):
        reading = tested_generator.generate_reading()
        assert isinstance(reading['id'], str)
        assert isinstance(reading['type'], str)
        assert isinstance(reading['content']['time_of_measurement'], str)
        assert isinstance(reading['content']['temperature_f'],  (int, float))
