import logging
import signal

from daemon import Daemon
from kafka import KafkaProducer

import settings
from collector import MetricsCollector


class CollectorDaemon(Daemon):

    _producer = None

    def _handle_sigterm(self, signum, frame) -> None:
        if self._producer:
            self._producer.flush()
            self._producer.close()

    def _init_logging(self)-> None:
        logger = logging.getLogger('mc')
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(settings.DAEMON_LOGS_FILE)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    def _init_producer(self) -> None:
        self._producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_SERVER,
            security_protocol='SSL',
            api_version_auto_timeout_ms=5000,
            ssl_cafile=settings.KAFKA_SSL_CA_FILE,
            ssl_certfile=settings.KAFKA_SSL_CERT_FILE,
            ssl_keyfile=settings.KAFKA_SSL_KEY_FILE)

    def run(self) -> None:
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)

        self._init_logging()
        self._init_producer()

        logger = logging.getLogger('mc.main')

        logger.info('Starting metrics collector service...')

        collector = MetricsCollector(self._producer)
        collector.run()


def main() -> None:
    d = CollectorDaemon(settings.DAEMON_PID_FILE)
    d.run()


if __name__ == '__main__':
    main()
