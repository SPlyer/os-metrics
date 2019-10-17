import json
import time
import logging
from datetime import datetime
from pony.orm import db_session
from pony.orm.core import TransactionIntegrityError

import settings

logger = logging.getLogger('ml.loader')

class MetricsLoader:

    def __init__(self, db, kafka_consumer):
        self._kafka_consumer = kafka_consumer
        self._db = db

    def save_metric(self, metric) -> None:

        for name in ('load_avg', 'cpu_util_pcts', 
                     'mem_used_pcts', 'disk_usage_pcts'):

            self._db.Metric(
                id=f'{metric["metric_id"]}_{name}',
                timestamp=datetime.utcfromtimestamp(metric['timestamp']),
                metric_name=name,
                metric_value=metric[name],
                machine_id=metric['machine_id'])
    

    def process_messages(self, messages) -> None:
        for msg in messages:
            logger.debug(f'Got message from kafka: {msg.value}')
            metric = json.loads(msg.value.decode('utf8'))
            try:
                with db_session:
                    self.save_metric(metric)
            except TransactionIntegrityError as e:
                logger.info(f'Record already processed: {e}, {metric}')
            

    def run(self) -> None:
        while True:
            for _ in range(settings.MAX_RETRIES_ERRORS):
                try:
                    msg_pack = self._kafka_consumer.poll(timeout_ms=1000)
                    for _, messages in msg_pack.items():
                        self.process_messages(messages)
                    self._kafka_consumer.commit()
                except Exception as e:
                    logger.error(f'Failed to process messages: {e}', exc_info=True)
                    time.sleep(30)
                    continue
                else:
                    break
            else:
                logger.error('Too many errors, retried '
                            f'{settings.MAX_RETRIES_ERRORS} times, exiting...')
                break
