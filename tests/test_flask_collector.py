import pytest
from etlapp.collector import flask_collector
import json
from etlapp import config


@pytest.fixture
def client():
    # flask_collector.app.config['TESTING'] = True
    yield flask_collector.app.test_client()


sample_record = {'id': '1', 'type': 'Sensor', 'content': {
    'temperature_f': 123, 'time_of_measurement': '2012-01-01T12:00'}}


def test_successful_data(mocker, client):
    mocker.patch('etlapp.collector.flask_collector.queuehelper')
    result = client.put('/' + config.PIPELINE_NAME, content_type='application/json',
                        data=json.dumps(sample_record))
    assert 200 == result.status_code


def test_warning_and_processing_in_absence_of_schema(mocker, client):
    mocker.patch('etlapp.collector.flask_collector.queuehelper')
    schemasmock = mocker.patch('etlapp.collector.flask_collector.schemas')
    logmock = mocker.patch('etlapp.collector.flask_collector.log')
    schemasmock.data_schemas = {}
    result = client.put('/' + config.PIPELINE_NAME, content_type='application/json',
                        data=json.dumps(sample_record))
    assert 200 == result.status_code
    assert logmock.warning.called


def test_malformed_data(mocker, client):
    mocker.patch('etlapp.collector.flask_collector.queuehelper')
    logmock = mocker.patch('etlapp.collector.flask_collector.log')
    malfomed_data = sample_record.copy()
    malfomed_data.update({'id': 12.2863})
    result = client.put('/' + config.PIPELINE_NAME, content_type='application/json',
                        data=json.dumps(malfomed_data))
    assert 400 == result.status_code
    assert logmock.error.called

    # This assumes log.error is called with tuple, which is normal way to do so likely ok
    assert malfomed_data in logmock.error.call_args[0]


def test_queue_is_teareddown_flushes_and_closed(mocker, client):
    queuemock = mocker.patch('etlapp.collector.flask_collector.queuehelper')
    result = client.put('/' + config.PIPELINE_NAME, content_type='application/json',
                        data=json.dumps(sample_record))
    queuemock.get_producer.assert_called_once()
    queuemock.get_producer.return_value.flush.assert_called_once()
    queuemock.get_producer.return_value.close.assert_called_once()


def test_queue_instansiated_tearedown_once_for_multiple_requests(mocker, client):
    queuemock = mocker.patch('etlapp.collector.flask_collector.queuehelper')
    with flask_collector.app.app_context():
        result = client.put('/' + config.PIPELINE_NAME, content_type='application/json',
                            data=json.dumps(sample_record))
        result = client.put('/' + config.PIPELINE_NAME, content_type='application/json',
                            data=json.dumps(sample_record))
    queuemock.get_producer.assert_called_once()
    queuemock.get_producer.return_value.flush.assert_called_once()
    queuemock.get_producer.return_value.close.assert_called_once()
