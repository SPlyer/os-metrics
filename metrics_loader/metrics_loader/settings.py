import os

path = os.path.dirname(os.path.abspath(__file__))

KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_SSL_KEY_FILE = os.getenv('KAFKA_SSL_KEY_FILE',
                               f'{path}/secret/service.key')
KAFKA_SSL_CERT_FILE = os.getenv('KAFKA_SSL_CERT_FILE',
                                f'{path}/secret/service.cert')
KAFKA_SSL_CA_FILE = os.getenv('KAFKA_SSL_CA_FILE', f'{path}/secret/ca.pem')
KAFKA_TOPIC_NAME = os.getenv('KAFKA_TOPIC_NAME', 'metrics-dev')

POSTGRES_USER = os.getenv('POSTGRES_USER')

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

POSTGRES_HOST = os.getenv('POSTGRES_HOST')

POSTGRES_PORT = os.getenv('POSTGRES_PORT')

POSTGRES_DB = os.getenv('POSTGRES_DB')

DAEMON = os.getenv('DAEMON', 'false') == 'true' # run in daemon mode

DAEMON_PID_FILE = os.getenv('DAEMON_PID_FILE', '/var/run/metrics_loader.pid')

DAEMON_LOGS_FILE = os.getenv(
    'DAEMON_LOGS_FILE', '/var/log/metrics_loader.log')

MAX_RETRIES_ERRORS = int(os.getenv('MAX_RETRIES_ERRORS', '20')) # max reties before exit