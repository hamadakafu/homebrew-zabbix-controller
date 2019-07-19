from unittest import mock
import time

from zabbix_controller.hosts.graphs import get_graphs


class Data:
    def __init__(self, args, mock_returned, answer):
        self.args = args
        self.mock_returned = mock_returned
        self.answer = answer


def test_get_graphs():
    zapi = mock.Mock()
    table = [
        Data({'_filter': None, 'match': None}, [], []),
        Data({'_filter': {'host': 'hhh', 'hostid': 1111}, 'match': None},
             [{'graphid': '111', 'name': 'CPU usage'}],
             [{'graphid': '111', 'name': 'CPU usage', 'host': 'hhh'}]),
        Data({'_filter': None, 'match': [{'graphid': '^11'}]},
             [{'graphid': '11112222', 'host': 'hhh-fff'},
              {'graphid': '22221111', 'host': 'hhh-fff'}],
             [{'graphid': '11112222', 'host': 'hhh-fff'}]),
        Data({'_filter': None, 'match': [{'graphid': '^11'}, {'host': 'fff$'}]},
             [{'graphid': '11112222', 'host': 'hhh-fff'},
              {'graphid': '22221111', 'host': 'hhh-fff'},
              {'graphid': '22221111', 'host': 'fff-hhh'},
              {'graphid': '11112222', 'host': 'fff-hhh'}],
             [{'graphid': '11112222', 'host': 'hhh-fff'}]),
        Data({'_filter': {'host': 'hhh-fff'}, 'match': [{'graphid': '^11'}, {'name': 'usage$'}]},
             [{'graphid': '11112222', 'name': 'CPU usage', 'host': 'hhh-fff'},
              {'graphid': '22221111', 'name': 'CPU hoge', 'host': 'hhh-fff'},
              {'graphid': '22221111', 'name': 'CPU fuga', 'host': 'hhh-fff'},
              {'graphid': '11112222', 'name': 'CPU foo', 'host': 'hhh-fff'}],
             [{'graphid': '11112222', 'name': 'CPU usage', 'host': 'hhh-fff'}]),
    ]
    for data in table:
        zapi.graph.get.return_value = data.mock_returned
        graphs = get_graphs(zapi, **data.args)
        assert graphs == data.answer
        for g in graphs:
            assert 'host' in g
