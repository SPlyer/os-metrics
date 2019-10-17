import json
from unittest.mock import patch, MagicMock, Mock
from dataclasses import asdict

import settings
from collector import MetricsCollector, MetricsRecord


class TestMetricsCollector:

    @patch('collector.lm')
    @patch('time.time', MagicMock(return_value=12345))
    def test_get_metrics(self, lm_mock):
        lm_mock.cpu_stat.cpu_percents.return_value = {'idle': 90}
        lm_mock.cpu_stat.load_avg.return_value = (10, 1, 1)
        lm_mock.mem_stat.mem_stats.return_value = (100, 1211)
        lm_mock.disk_stat.disk_usage.return_value = (
            None, None, None, None, b'5%')

        c = MetricsCollector(Mock())

        assert c.get_metrics() == MetricsRecord(
            10, 10, 8.26, 5, settings.MACHINE_ID, 12345)


    def test_send_metrics(self):
        kafka_mock = Mock()

        metrics = MetricsRecord(10, 10, 10, 5, 'abcd', 12345)
        c = MetricsCollector(kafka_mock)
        c.get_metrics = Mock(return_value=metrics)
        c.send_metrics()

        metrics_bytes = json.dumps(asdict(metrics)).encode('utf8')

        kafka_mock.send.assert_called_with(
            settings.KAFKA_TOPIC_NAME, metrics_bytes)