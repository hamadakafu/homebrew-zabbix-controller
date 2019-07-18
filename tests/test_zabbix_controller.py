from unittest import mock
import time

from zabbix_controller.utils import *


def test_get_hosts():
    zapi = mock.Mock()
    table = [
        ([{'name': 'hogehoge', 'hostid': '194'}],
         {'name': 'hoge'},
         [{'name': 'hogehoge', 'hostid': '194'}]),
        ([{'name': 'hogeho1', 'hostid': '1414'},
          {'name': 'hogeho2', 'hostid': '1415'},
          {'name': 'foooooo1', 'hostid': '1471048'}],
         {'name': '^hogeho'},
         [{'name': 'hogeho1', 'hostid': '1414'}, {'name': 'hogeho2', 'hostid': '1415'}])
    ]
    for data in table:
        zapi.host.get.return_value = data[0]
        hosts = get_hosts(zapi, data[1])
        assert hosts == data[2], f'hosts must be {data[2]}'
