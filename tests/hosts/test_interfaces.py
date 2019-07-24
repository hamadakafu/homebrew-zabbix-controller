from unittest import mock

from zabbix_controller.hosts.interfaces import get_interfaces


class Data:
    def __init__(self, args, mock_returned, answer):
        self.args = args
        self.mock_returned = mock_returned
        self.answer = answer


def test_get_interfaces():
    zapi = mock.Mock()
    table = [
        Data({'_filter': None, 'match': None}, [], []),
        Data({'_filter': {'host': 'hhh', 'hostid': 1111}, 'match': None},
             [
                 {'interfaceid': '111', 'name': 'CPU usage'},
             ],
             [
                 {'interfaceid': '111', 'name': 'CPU usage', 'host': 'hhh'},
             ]),
        Data({'_filter': None, 'match': [{'interfaceid': '^11'}]},
             [
                 {'interfaceid': '11112222', 'hostid': '111'},
                 {'interfaceid': '22221111', 'hostid': '111'},
                 {'interfaceid': '11112222', 'hostid': '222'},
             ],
             [
                 {'interfaceid': '11112222', 'hostid': '111'},
                 {'interfaceid': '11112222', 'hostid': '222'},
             ]),
        Data({'_filter': None, 'match': [{'interfaceid': '^11', 'hostid': '1122$'}]},
             [
                 {'interfaceid': '11112222', 'hostid': '1122'},
                 {'interfaceid': '22221111', 'hostid': '112'},
                 {'interfaceid': '22221111', 'hostid': '122'},
                 {'interfaceid': '11112222', 'hostid': '122'},
             ],
             [
                 {'interfaceid': '11112222', 'hostid': '1122'},
             ]),
        Data({'_filter': {'host': 'hhh-fff', 'hostid': '111'}, 'match': [{'interfaceid': '^11', 'useip': '^0$'}]},
             [
                 {'interfaceid': '11112222', 'useip': '0', 'host': 'hhh-fff'},
                 {'interfaceid': '22221111', 'useip': '1', 'host': 'hhh-fff'},
                 {'interfaceid': '22221111', 'useip': '0', 'host': 'hhh-fff'},
                 {'interfaceid': '11112222', 'useip': '1', 'host': 'hhh-fff'},
             ],
             [
                 {'interfaceid': '11112222', 'useip': '0', 'host': 'hhh-fff'},
             ]),
        # TODO: write test or pattern
    ]
    for data in table:
        zapi.hostinterface.get.return_value = data.mock_returned
        interfaces = get_interfaces(zapi, **data.args)
        assert interfaces == data.answer
