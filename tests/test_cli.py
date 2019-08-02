from unittest import mock
import json
from contextlib import ExitStack

from click import testing

import zabbix_controller


class Data(object):
    def __init__(self, args, mocked, stdout):
        self.args = args
        self.mocked = mocked
        self.stdout = stdout


def test_main():
    table = [
        Data(
            args=['--dry-run', 'hosts', 'list'],
            mocked=[
                ('zabbix_controller.hosts.command.get_hosts', []),
            ],
            stdout=f'{json.dumps({"message": "There is not host."})}\n'
        ),
        Data(
            args=['--dry-run', 'hosts', 'list'],
            mocked=[
                ('zabbix_controller.hosts.command.get_hosts', [{'name': 'hhh'}]),
            ],
            stdout=f'{json.dumps({"hosts": [{"name": "hhh"}]})}\n'
        ),
        Data(
            args=['--dry-run', 'hosts', 'graphs', 'list'],
            mocked=[
                ('zabbix_controller.hosts.command.get_hosts', [{'host': 'hhh'}]),
                ('zabbix_controller.hosts.graphs.get_graphs', [{'name': 'hhh_graph'}]),
            ],
            stdout=f'{json.dumps({"graphs": [{"name": "hhh_graph"}]})}\n'
        ),
        Data(
            args=['--version'],
            mocked=[],
            stdout=f'zabbixctl 0.1.17\n'
        ),
    ]

    for data in table:
        with ExitStack() as stack:
            ms = [stack.enter_context(mock.patch(d[0], return_value=d[1])) for d in data.mocked]
            with mock.patch('zabbix_controller.cli.zabbix_auth', return_value=object):
                runner = testing.CliRunner()
                result = runner.invoke(zabbix_controller.cli.main, data.args)

                assert result.exit_code == 0
                assert result.output == data.stdout
