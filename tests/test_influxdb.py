import pytest
from unittest.mock import MagicMock

from etlapp.datawriter import influxdb_writer


def test_ensure_write_poits_is_called(mocker):
    consumermock = mocker.patch(
        'etlapp.datawriter.influxdb_writer.get_consumer')
    influxmock = mocker.patch(
        'etlapp.datawriter.influxdb_writer.InfluxDBClient')
    datapoint = MagicMock()
    consumermock.return_value.__iter__.return_value = [datapoint]
    influxdb_writer.main()
    influxmock.assert_called_once()
    influxmock.return_value.write_points.assert_called_once()


def test_ensure_write_poits_is_called_two_records(mocker):
    consumermock = mocker.patch(
        'etlapp.datawriter.influxdb_writer.get_consumer')
    influxmock = mocker.patch(
        'etlapp.datawriter.influxdb_writer.InfluxDBClient')
    consumermock.return_value.__iter__.return_value = [
        MagicMock(), MagicMock()]
    influxdb_writer.main()
    influxmock.assert_called_once()
    assert 2 == influxmock.return_value.write_points.call_count


def test_ensure_queue_read_is_committed(mocker):
    consumermock = mocker.patch(
        'etlapp.datawriter.influxdb_writer.get_consumer')
    influxmock = mocker.patch(
        'etlapp.datawriter.influxdb_writer.InfluxDBClient')
    consumermock.return_value.__iter__.return_value = [MagicMock()]
    influxdb_writer.main()
    consumermock.return_value.commit.assert_called_once()
