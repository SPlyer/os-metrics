import time
import json
import uuid
import logging
from dataclasses import dataclass, asdict

import linux_metrics as lm
from kafka import KafkaProducer

import settings

logger = logging.getLogger('mc.collector')


@dataclass
class MetricsRecord:
    load_avg: float
    cpu_util_pcts: float
    mem_used_pcts: float
    disk_usage_pcts: float
    machine_id: str
    timestamp: float
    metric_id: str


class MetricsCollector:

    def __init__(self, kafka_producer: KafkaProducer):
        self.kafka_producer = kafka_producer

    def get_metrics(self) -> MetricsRecord:

        cpu_pcts = lm.cpu_stat.cpu_percents(
            sample_duration=settings.COLLECTION_INTERVAL)

        load_avg_min, *_ = lm.cpu_stat.load_avg()

        mem_used, mem_total, *_ = lm.mem_stat.mem_stats()

        _, _, _, _, disk_usage_str, *_ = lm.disk_stat.disk_usage(
            settings.DISK_USAGE_PATH)

        disk_usage_pcts = int(disk_usage_str.decode('utf8').strip('%'))

        return MetricsRecord(
            cpu_util_pcts=round(100 - cpu_pcts['idle'], 2),
            mem_used_pcts=round(mem_used / mem_total * 100, 2),
            disk_usage_pcts=round(disk_usage_pcts, 2),
            load_avg=round(load_avg_min, 2),
            machine_id=settings.MACHINE_ID,
            timestamp=round(time.time(), 2),
            metric_id=str(uuid.uuid4()))

    def send_metrics(self) -> None:
            metrics = self.get_metrics()

            data = json.dumps(asdict(metrics)).encode('utf8')
            
            logger.debug(f'Sending metrics: {metrics}')

            self.kafka_producer.send(settings.KAFKA_TOPIC_NAME, data)

    def run(self) -> None:
        while True:
            self.send_metrics()