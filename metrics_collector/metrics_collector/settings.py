import os

path = os.path.dirname(os.path.abspath(__file__))

KAFKA_SERVER = os.getenv('KAFKA_SERVER',
                         'kafka-34f388bd-splyer-2eca.aivencloud.com:25243')
KAFKA_SSL_KEY_FILE = os.getenv('KAFKA_SSL_KEY_FILE',
                               f'{path}/secret/service.key')
KAFKA_SSL_CERT_FILE = os.getenv('KAFKA_SSL_CERT_FILE',
                                f'{path}/secret/service.cert')
KAFKA_SSL_CA_FILE = os.getenv('KAFKA_SSL_CA_FILE', f'{path}/secret/ca.pem')
KAFKA_TOPIC_NAME = os.getenv('KAFKA_TOPIC_NAME', 'metrics-dev')

# metrics collection interval in seconds
COLLECTION_INTERVAL = int(os.getenv('COLLECTION_INTERVAL', '5'))

DISK_USAGE_PATH = os.getenv('DISK_USAGE_PATH', '/')

MACHINE_ID = os.getenv('MACHINE_ID', os.uname()[1])

DAEMON_PID_FILE = os.getenv('DAEMON_PID_FILE', '/var/run/metrics_collector.pid')

DAEMON_LOGS_FILE = os.getenv(
    'DAEMON_LOGS_FILE', '/var/log/metrics_collector.log')
