# Configurations settings overridable by env variables
import logging
from os import environ

# Global Settings
LOG_LEVEL = environ.get('LOG_LEVEL', logging.WARNING)

# Connection Settins
KAFKA_BROKERS = environ.get('KAFKA_BROKERS', 'localhost:9094').split(';')

# Data Emitter settings
DATA_EMITTER = environ.get('DATA_EMITTER', 'etlapp.datagenerator.rest_emitter')
REST_EMITTER_URL = environ.get('REST_EMITTER_URL', 'http://localhost:5000')
DATA_GENERATOR = environ.get(
    'DATA_GENERATOR', 'etlapp.datagenerator.gaussian_generator')
EMITTER_REQUESTS_PER_SECOND = environ.get('EMITTER_REQUESTS_PER_SECOND', 0.5)
MQTT_BROKER_HOST = environ.get('MQTT_BROKER_HOST', '127.0.0.1')
MQTT_BROKER_PORT = int(environ.get('MQTT_BROKER_PORT', 1883))


# Data Generator settings
GENERATOR_TEMPERATURE_F_DECIMALS = environ.get(
    'GENERATOR_TEMPERATURE_F_DECIMALS', 2)
GENERATOR_TEMPERATURE_C_DECIMALS = environ.get(
    'GENERATOR_TEMPERATURE_C_DECIMALS', 2)

GAUSS_GENERATOR_TEMPERATURE_F_MEAN = environ.get(
    'GAUSS_GENERATOR_TEMPERATURE_F_MEAN', 78)
GAUSS_GENERATOR_TEMPERATURE_F_SIGMA = environ.get(
    'GAUSS_GENERATOR_TEMPERATURE_F_SIGMA', 17)

RANDOM_GENERATOR_TEMPERATURE_F_MIN = environ.get(
    'RANDOM_GENERATOR_TEMPERATURE_F_MIN', 32)
RANDOM_GENERATOR_TEMPERATURE_F_MAX = environ.get(
    'RANDOM_GENERATOR_TEMPERATURE_F_MAX', 212)

# Data Pipeline settings
PIPELINE_NAME = environ.get(
    'PIPELINE_NAME', 'temperatures')  # Used for DB Name
PIPELINE_COLLECTED_DATA_QUEUE_TOPIC = environ.get(
    'PIPELINE_COLLECTED_DATA_QUEUE_TOPIC', 'CollectedTemperatureData')
PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC = environ.get(
    'PIPELINE_TRANFORMED_DATA_QUEUE_TOPIC', 'TransformedTemperatureData')
PIPELINE_DATA_TRANSFORMATION_MODULE = environ.get(
    'PIPELINE_DATA_TRANSFORMATION_MODULE', 'etlapp.datamapper.%s_mapper' % PIPELINE_NAME)

# INFLUXDB SETTINGS
INFLUXDB_HOST = environ.get('INFLUXDB_HOST', 'localhost')
INFLUXDB_PORT = environ.get('INFLUXDB_PORT', 8086)
INFLUXDB_USERNAME = environ.get('INFLUXDB_USERNAME', 'admin')
INFLUXDB_PASSWORD = environ.get('INFLUXDB_PASSWORD', 'admin')

# Queue Settings
QUEUE_IMPLEMENTATION_MODULE = 'etlapp.queuehelper.kafka_queue'
