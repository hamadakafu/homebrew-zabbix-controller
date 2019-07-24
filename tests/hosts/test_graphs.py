from unittest import mock

from zabbix_controller.hosts.graphs import get_graphs


class Data:
    def __init__(self, args, mock_returned, answer):
        self.args = args
        self.mock_returned = mock_returned
        self.answer = answer


def test_get_graphs():
    zapi = mock.Mock()
    table = [
        Data({'_filter': None, 'match': None},
             [{'graphid': '111', 'name': 'CPU usage'}],
             [{'graphid': '111', 'name': 'CPU usage'}]),
        Data({'_filter': {'host': 'hhh', 'hostid': 1111}, 'match': None},
             [{'graphid': '111', 'name': 'CPU usage'}],
             [{'graphid': '111', 'name': 'CPU usage', 'host': 'hhh'}]),
        Data({'_filter': None, 'match': [{'graphid': '^11'}]},
             [{'graphid': '1122', 'host': 'hhh-fff'},
              {'graphid': '2211', 'host': 'hhh-fff'}],
             [{'graphid': '1122', 'host': 'hhh-fff'}]),
        Data({'_filter': None, 'match': [{'graphid': '^11'}, {'host': 'fff$'}]},
             [{'graphid': '111', 'name': 'CPU usage', 'host': 'hhh-fff'},
              {'graphid': '222', 'name': 'CPU hoge', 'host': 'hhh-fff'},
              {'graphid': '333', 'name': 'CPU fuga', 'host': 'fff-hhh'},
              {'graphid': '444', 'name': 'CPU foo', 'host': 'fff-hhh'}],
             [{'graphid': '111', 'name': 'CPU usage', 'host': 'hhh-fff'},
              {'graphid': '222', 'name': 'CPU hoge', 'host': 'hhh-fff'}]),
        Data({'_filter': {'host': 'hhh-fff'},
              'match': [{'graphid': '^11', 'name': 'usage$'}]},
             [{'graphid': '111', 'name': 'CPU usage', 'host': 'hhh-fff'},
              {'graphid': '112', 'name': 'Memory usage', 'host': 'hhh-fff'},
              {'graphid': '222', 'name': 'CPU hoge', 'host': 'hhh-fff'},
              {'graphid': '333', 'name': 'CPU fuga', 'host': 'hhh-fff'},
              {'graphid': '444', 'name': 'CPU foo', 'host': 'hhh-fff'}],
             [{'graphid': '111', 'name': 'CPU usage', 'host': 'hhh-fff'},
              {'graphid': '112', 'name': 'Memory usage', 'host': 'hhh-fff'}]),
    ]
    for data in table:
        zapi.graph.get.return_value = data.mock_returned
        graphs = get_graphs(zapi, **data.args)

        for g in graphs:
            if data.args['_filter'] is not None:
                assert 'host' in g

        for graph in graphs:
            assert graph in data.answer

        for ans in data.answer:
            assert ans in graphs

        assert len(data.answer) == len(graphs)
