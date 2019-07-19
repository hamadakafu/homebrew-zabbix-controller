from unittest import mock
import time

from zabbix_controller.hosts import apis


class Data:
    def __init__(self, args, mock_returned, answer):
        self.args = args
        self.mock_returned = mock_returned
        self.answer = answer


def test_get_hosts():
    zapi = mock.Mock()
    table = [
        Data((zapi, [{'name': 'hhh'}]),
             [{'name': 'fff_hhh_fff', 'hostid': '194'}],
             [{'name': 'fff_hhh_fff', 'hostid': '194'}]),
        Data((zapi, [{'name': '^hhh'}]),
             [{'name': 'hhh1', 'hostid': '1414'},
              {'name': 'hhh2', 'hostid': '1415'},
              {'name': 'fff1', 'hostid': '1471048'}],
             [{'name': 'hhh1', 'hostid': '1414'},
              {'name': 'hhh2', 'hostid': '1415'}]),
        Data((zapi, [{'name': '^hhh'}], {'key': 'time', 'from': 0, 'to': int(time.time())}),
             [{'name': 'hhh_fff', 'time': '1'},
              {'name': 'fff_hhh', 'time': '1'},
              {'name': 'hhh_fff', 'time': str(int(time.time())+1)},
              {'name': 'fff_hhh', 'time': '-1'}],
             [{'name': 'hhh_fff', 'time': '1'}]),
        Data((zapi, [{'name': '^hhh'}, {'hostid': '^12345$'}], {'key': 'time', 'from': 0, 'to': int(time.time())}),
             [{'name': 'hhh_fff', 'hostid': '12345', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '12345', 'time': str(int(time.time())+1)},
              {'name': 'fff_hhh', 'hostid': '12346', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '12347', 'time': str(int(time.time())+1)},
              {'name': 'fff_hhh', 'hostid': '12348', 'time': '-1'}],
             [{'name': 'hhh_fff', 'hostid': '12345', 'time': '1'}]),
    ]
    for data in table:
        zapi.host.get.return_value = data.mock_returned
        hosts = apis.get_hosts(*data.args)
        assert hosts == data.answer, f'{data.args}'
