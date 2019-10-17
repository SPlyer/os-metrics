# OS Metrics

The system includes two services:

* metrics_collector - collects OS metrics (CPU, memory, disk) and sends it to Kafka topic

* metrics_loader - consumes Kafka topic and saves to Postgres DB

## How to run

Several environment variables needs to be setup, mainly Postgres and Kafka configuration. Look at `settings.py` in `metrics_collector` and `metrics_loader` for more info. 

After updating `docker-compose.yml` with environment variables run:

    docker-compose up

It will start both collector and loader.

## Tests

To run tests for collector:

    docker-compose run metrics_collector bash
    pytest metrics_collector/tests.py


To run metrics loader tests:

    docker-compose run metrics_loader bash
    pytest metrics_loader/tests.py
