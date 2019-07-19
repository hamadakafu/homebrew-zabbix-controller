from unittest import mock
import time

from zabbix_controller.utils import *


def test_validate_match():
    ctx = mock.Mock()
    param = mock.Mock()
    table = [
        ('{"name": "hoge"}', [{'name': 'hoge'}], True),
        ('{"state": 0}', [{'state': 0}], True),
        ('{"state": "0"}', [{'state': '0'}], True),
        (None, None, True),
    ]
    for data in table:
        values = validate_match(ctx, param, data[0])
        assert (values == data[1]) is data[2]


def test_validate_time_match():
    ctx = mock.Mock()
    param = mock.Mock()
    table = [
        ('errors_from:-', {'key': 'errors_from', 'from': 0, 'to': int(time.time())}, True),
        ('errors_from:2758325-178571414', {'key': 'errors_from', 'from': 2758325, 'to': 178571414}, True),
        ('errors_from:-178571414', {'key': 'errors_from', 'from': 0, 'to': 178571414}, True),
        ('errors_from:4710-', {'key': 'errors_from', 'from': 4710, 'to': int(time.time())}, True),
        (None, None),
    ]
    for data in table:
        values = validate_time_range(ctx, param, data[0])
        if values is None:
            assert data[0] == data[1]
            return

        assert (values['key'] == data[1]['key']) is data[2]
        assert (values['from'] == data[1]['from']) is data[2]
        assert (data[1]['to'] - 5 <= values['to'] <= data[1]['to']) is data[2]  # テストの実行による5秒の遅れを許す


def test_validate_json():
    ctx = mock.Mock()
    param = mock.Mock()
    table = [
        ('{"name": "hoge"}', {'name': 'hoge'}, True),
        ('{"state": 0}', {'state': 0}, True),
        ('{"state": "0"}', {'state': '0'}, True),
        (None, None, True),
    ]
    for data in table:
        values = validate_json(ctx, param, data[0])
        assert (values == data[1]) is data[2]
