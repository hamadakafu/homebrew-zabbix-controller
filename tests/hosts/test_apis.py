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
             [{'name': 'hhh_fff', 'hostid': '11111', 'time': '1'},
              {'name': 'fff_hhh', 'hostid': '22222', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '33333', 'time': str(int(time.time()) + 1)},
              {'name': 'fff_hhh', 'hostid': '44444', 'time': '-1'}],
             [{'name': 'hhh_fff', 'hostid': '11111', 'time': '1'}]),
        Data((zapi, [{'name': '^hhh'}, {'hostid': '111$'}],
              {'key': 'time', 'from': 0, 'to': int(time.time())}),
             [{'name': 'hhh_fff', 'hostid': '111', 'time': '1'},
              {'name': 'fff_hhh', 'hostid': '000111', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '222', 'time': '1'},
              {'name': 'fff_hhh', 'hostid': '333', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '444', 'time': str(int(time.time()) + 1)},
              {'name': 'fff_hhh', 'hostid': '555', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '666', 'time': str(int(time.time()) + 1)},
              {'name': 'fff_hhh', 'hostid': '777', 'time': '-1'}],
             [{'name': 'hhh_fff', 'hostid': '111', 'time': '1'},
              {'name': 'fff_hhh', 'hostid': '000111', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '222', 'time': '1'}]),
        Data((zapi, [{'name': '^hhh', 'hostid': '^12345$'}],
              {'key': 'time', 'from': 0, 'to': int(time.time())}),
             [{'name': 'hhh_fff', 'hostid': '12345', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '12346', 'time': str(int(time.time()) + 1)},
              {'name': 'fff_hhh', 'hostid': '12347', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '12348', 'time': str(int(time.time()) + 1)},
              {'name': 'fff_hhh', 'hostid': '12349', 'time': '-1'}],
             [{'name': 'hhh_fff', 'hostid': '12345', 'time': '1'}]),
        Data((zapi, [{'name': '^hhh', 'hostid': '^12345$'}, {'name': 'hhh$'}],
              {'key': 'time', 'from': 0, 'to': int(time.time())}),
             [{'name': 'hhh_fff', 'hostid': '12345', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '12346', 'time': str(int(time.time()) + 1)},
              {'name': 'fff_hhh', 'hostid': '12347', 'time': '1'},
              {'name': 'hhh_fff', 'hostid': '12348', 'time': str(int(time.time()) + 1)},
              {'name': 'fff_hhh', 'hostid': '12349', 'time': '-1'}],
             [{'name': 'hhh_fff', 'hostid': '12345', 'time': '1'},
              {'name': 'fff_hhh', 'hostid': '12347', 'time': '1'}]),
    ]
    for data in table:
        zapi.host.get.return_value = data.mock_returned
        hosts = apis.get_hosts(*data.args)

        for host in hosts:
            assert host in data.answer

        for ans in data.answer:
            assert ans in hosts

        assert len(data.answer) == len(hosts)
