# Simple, yet flexible ETL solution
Using Python and Kafka, with options to consume data from various sources (MQTT and REST included) and saving to multiple DBs (InfluxDB included, Mongo To be added).

## Directory structure

```
    SimpleETL
    /docker               - docker & docker-compose files necessary to run local simulation of ETL
    /docker/.env.mqtt     - docker-compose configuration file for mqtt variant of simulation
    /docker/.env.rest     - docker-compose configuration file for mqtt variant of simulation
    /etlapp               - main python module
    /etlapp/collector     - collector modules for collecting data from the sensors and 
                          redirecting to  the queue
    /etlapp/datagenerator - random data generators for the purpose of simulation
    /etlapp/datamapper    - data transformations (such as recalc from F to C)
    /etlapp/datawriter    - modules responsible for writing to the DB (influxDB, Mongo)
    /tests                - Unit and functional tests
```

## PreRequsites

Docker & docekr-compose is required

Python requirements are in requiremets.txt (except Flask as it breaks docker build and is unnecessary) using venv is highly recommended - in the future will have two deparate requirement.txt for dev and build (likely tox)

Python 3.7.9 used during development

## Usage

inside ```./docker``` folder perform following:
```
    docker-compose --env-file .env.rest build
    docker-compose --env-file .env.rest up -d
```

This will start a demo environment simulating traffic from sensor to the DB as well as it will bootstrap the dashboards preconfigured for influxDB

For MQTT version use:

```
    docker-compose --env-file .env.mqtt build
    docker-compose --env-file .env.mqtt up -d 
```

**NOTE** - you need to perform build when switching between mqtt and rest as they use the same docker-compose container names and this might lead to unexpected errors

Once containers are running you should see something like this when you run:

```
$ docker-compose --env-file .env.mqtt ps
         Name                       Command               State                         Ports
--------------------------------------------------------------------------------------------------------------------
docker_chronograf_1      /entrypoint.sh chronograf        Up      127.0.0.1:8888->8888/tcp
docker_collector_1       python -m etlapp.collector ...   Up
docker_datagenerator_1   python -m etlapp.datagenerator   Up
docker_datamapper_1      python -m etlapp.datamapper      Up
docker_datawriter_1      python -m etlapp.datawriter      Up
docker_grafana_1         /run.sh                          Up      0.0.0.0:3000->3000/tcp
docker_influxdb_1        /entrypoint.sh influxd           Up      0.0.0.0:8086->8086/tcp
docker_kafka-1_1         start-kafka.sh                   Up      0.0.0.0:9094->9094/tcp
docker_kafka-2_1         start-kafka.sh                   Up      0.0.0.0:9095->9095/tcp
docker_kafka-3_1         start-kafka.sh                   Up      0.0.0.0:9096->9096/tcp
docker_zookeeper_1       /bin/sh -c /usr/sbin/sshd  ...   Up      0.0.0.0:2181->2181/tcp, 22/tcp, 2888/tcp, 3888/tcp
mosquitto                /docker-entrypoint.sh /usr ...   Up      0.0.0.0:1883->1883/tcp, 0.0.0.0:9001->9001/tcp
```

At this point you can access web UI using Chronograph or Grafana on urls and create dashboards and queries:
```
http://127.0.0.1:8888/  -> to access chronograph
http://127.0.0.1:3000/  -> to access grafana
```

## Scaling

You can scale your environment horizontally by adding additional hosts using:
```
docker-compose --env-file .env.rest scale datamapper=3
```
This will work for ```datamapper```, ```collector``` and ```datagenerator``` (*Note* that you can adjust the desired throughput of each generator/emitter by env setting EMITTER_REQUESTS_PER_SECOND, the defaul is quite 0.5 requests per second)

## Testing

```
python -m pytest --cov=etlapp --cov-report term-missing
```

## TODO

```
- [ ] implement tests for MQTT related code
- [ ] implement tests for MongoDB related code
- [ ] Add docker-compose configuration for MongoDB runs
- [ ] consider capturing metrics
- [ ] add some out of the box dashboards
- [ ] consider batching of data during processing
- [ ] cleanup requirements.txt
- [ ] create separate requrements for dev/deploy (tox)
- [ ] ensure linting is clear
```

## Notes

```
Kafka Docker setup based on: https://github.com/wurstmeister/kafka-docker
Influx/Chronograph/Grafana setup from: https://github.com/jkehres/docker-compose-influxdb-grafana/blob/master/docker-compose.yml
```
