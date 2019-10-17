import logging
import signal

from daemon import Daemon
from kafka import KafkaConsumer
from pony.orm import Database


import settings
from models import define_entities
from loader import MetricsLoader

class LoaderDaemon(Daemon):

    _consumer = None
    _db = Database()

    def _handle_sigterm(self, signum, frame) -> None:
        try:
            if self._consumer:
                self._consumer.close()
        finally:
            self._db.disconnect()

    def _init_logging(self):
        logger = logging.getLogger('ml')
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(settings.DAEMON_LOGS_FILE)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    def _init_consumer(self):
        self._consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_NAME,
            auto_offset_reset="earliest",
            client_id="metrics-client-1",
            group_id="metrics-group",
            bootstrap_servers=settings.KAFKA_SERVER,
            security_protocol='SSL',
            ssl_cafile=settings.KAFKA_SSL_CA_FILE,
            ssl_certfile=settings.KAFKA_SSL_CERT_FILE,
            ssl_keyfile=settings.KAFKA_SSL_KEY_FILE)

    def _init_db(self):
        self._db.bind(
            provider='postgres', 
            user=settings.POSTGRES_USER, 
            password=settings.POSTGRES_PASSWORD, 
            host=settings.POSTGRES_HOST, 
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB)
        define_entities(self._db)
        self._db.generate_mapping(create_tables=True)

    def run(self):
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)

        self._init_logging()
        self._init_db()

        self._init_consumer()

        logger = logging.getLogger('ml.main')

        logger.info('Starting metrics loader service...')

        loader = MetricsLoader(self._db, self._consumer)
        loader.run()

def main():
    d = LoaderDaemon(settings.DAEMON_PID_FILE)
    d.run()


if __name__ == '__main__':
    main()

