import pytest
import kafka.errors
from etlapp import queuehelper


def test_get_producer_returns_value(mocker):
    mocker.patch('etlapp.queuehelper.KafkaProducer')
    result = queuehelper.get_producer()
    assert result is not None


def test_get_producer_retries_n_times_on_error(mocker):
    producer = mocker.patch('etlapp.queuehelper.KafkaProducer')
    producer.side_effect = kafka.errors.NoBrokersAvailable()
    with pytest.raises(kafka.errors.NoBrokersAvailable):
        result = queuehelper.get_producer(retries=3, retrydelay=0.1)
    assert producer.call_count == 3


def test_get_consumer_returns_value(mocker):
    mocker.patch('etlapp.queuehelper.KafkaConsumer')
    result = queuehelper.get_consumer("TestTopic")
    assert result is not None


def test_get_consumer_retries_n_times_on_error(mocker):
    consumer = mocker.patch('etlapp.queuehelper.KafkaConsumer')
    consumer.side_effect = kafka.errors.NoBrokersAvailable()
    with pytest.raises(kafka.errors.NoBrokersAvailable):
        result = queuehelper.get_consumer(
            "TestTopic", retries=3, retrydelay=0.1)
    assert consumer.call_count == 3
