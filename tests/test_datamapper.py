import pytest
from etlapp import datamapper
from etlapp import config
from unittest import mock
import importlib
import pkgutil

# Adding round to magics, as by default it is not there
mock._magics.add('__round__')

mappers = [importlib.import_module('etlapp.datamapper.' + name)
           for _, name, _ in pkgutil.iter_modules(datamapper.__path__)
           if name.endswith('_mapper')]


@ pytest.mark.parametrize('tested_mapper', mappers)
def test_each_mapper_needs_map_method(tested_mapper):
    assert hasattr(tested_mapper, 'map')


@ pytest.mark.parametrize('tested_mapper', mappers)
def test_mapper_is_callable_and_returns_value(tested_mapper):
    data = mock.MagicMock()
    result = tested_mapper.map(data)
    assert result is not None


def test_ensure_correct_mapper_is_loaded_and_used(mocker):
    ilibmock = mocker.patch('etlapp.datamapper.importlib')
    consumermock = mocker.patch('etlapp.datamapper.get_consumer')
    producermock = mocker.patch('etlapp.datamapper.get_producer')
    datamapper.main()
    ilibmock.import_module.assert_called_with(
        config.PIPELINE_DATA_TRANSFORMATION_MODULE)


def test_ensure_data_is_read_and_written(mocker):
    ilibmock = mocker.patch('etlapp.datamapper.importlib')
    consumermock = mocker.patch('etlapp.datamapper.get_consumer')
    producermock = mocker.patch('etlapp.datamapper.get_producer')

    consumermock.return_value.__iter__.return_value = [mock.MagicMock()]
    datamapper.main()
    consumermock.return_value.__iter__.assert_called_once()
    producermock.return_value.send.assert_called_once()
