import datetime
from unittest.mock import Mock, call, patch

import settings
from loader import MetricsLoader


class TestMetricsLoader:

    def test_process_messages(self):
        messages = [Mock(value=
            b'{"load_avg": 0.01, "cpu_util_pcts": 0.3, "mem_used_pcts": '
            b'21.76, "disk_usage_pcts": 6, "machine_id": "4f477ed05590", '
            b'"timestamp": 1571317918.84, "metric_id": "'
            b'a333630a-328b-42c1-9279-bb8389085322"}')]

        db_mock = Mock()
        loader = MetricsLoader(db_mock, Mock())
        loader.process_messages(messages)
        ts = datetime.datetime(2019, 10, 17, 13, 11, 58, 840000)

        assert db_mock.Metric.call_count == 4

        db_mock.Metric.assert_has_calls([
            call(id='a333630a-328b-42c1-9279-bb8389085322_load_avg',
                 machine_id='4f477ed05590', metric_name='load_avg',
                 metric_value=0.01, timestamp=ts),
            call(id='a333630a-328b-42c1-9279-bb8389085322_cpu_util_pcts',
                 machine_id='4f477ed05590', metric_name='cpu_util_pcts',
                 metric_value=0.3, timestamp=ts),
            call(id='a333630a-328b-42c1-9279-bb8389085322_mem_used_pcts',
                 machine_id='4f477ed05590', metric_name='mem_used_pcts',
                 metric_value=21.76, timestamp=ts),
            call(id='a333630a-328b-42c1-9279-bb8389085322_disk_usage_pcts',
                 machine_id='4f477ed05590', metric_name='disk_usage_pcts',
                 metric_value=6, timestamp=ts)])

    @patch('time.sleep', Mock())
    def test_max_retries(self):
        kafka_mock = Mock()
        kafka_mock.poll.side_effect = Exception('some exception')
        loader = MetricsLoader(Mock(), kafka_mock)
        loader.run()
        assert kafka_mock.poll.call_count == settings.MAX_RETRIES_ERRORS