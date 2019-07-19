import re
import pprint

import click
from pyzabbix import ZabbixAPI

from .command import hosts
from ..utils import validate_match, check_dry_run, ask_graphs
from . import ZabbixCTL


def get_graphs(zapi, _filter=None, match=None):
    """
    Get graphs.

    Add hostid, host property in graph dict.

    Parameters
    ----------
    zapi: ZabbixAPI
        ZabbixAPI object
    _filter: dict
        Must include host key that is hostname.
        {'name': 'some-name'}.
        Not regex. Used for API requests.
    match: [dict]
        Regex. Using re package. These conditions are chained by `and` operator.
        Not Used for API requests.
        Used after API requests.

    Returns
    -------
    _graphs: [dict]
        graph objects including host
    """
    if _filter is not None and 'host' not in _filter:
        raise ValueError('filter must include host key.')

    _graphs = zapi.graph.get(filter=_filter)
    if match is not None:
        for m in match:
            _graphs = list(
                filter(
                    lambda graph: re.search(list(m.values())[0], graph[list(m.keys())[0]]) is not None,
                    _graphs,
                )
            )

    if _filter is not None:
        for g in _graphs:
            g['host'] = _filter['host']

    return _graphs


@hosts.group(help='host graph')
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'You can use json.\n'
                    'ex1) \'{"name": "^some$"}\' -> This matches some, ...\n'
                    'ex2) \'{"graphid": 41}\' -> This matches 4123232, 111141, ...'
                    'ex3) \'{"name": "^$"}\' -> This matches empty string')
              )
@click.pass_obj
def graphs(obj: ZabbixCTL, match):
    """
    Entry point graphs command. Add graphs to ZabbixCTL.
    graphs = [{hostname: 'host_name', graphs: [graph]}]
    """

    _graphs = []
    for host in obj.hosts:
        h_graphs = get_graphs(obj.zapi, {'host': host['host']}, match=match)
        if len(h_graphs) == 0:
            continue

        _graphs.extend(h_graphs)

    obj.graphs = _graphs


@graphs.command(name='list', help='list graph')
@click.pass_obj
def _list(obj):
    click.echo(pprint.pformat(obj.graphs))


@graphs.command(help='delete graph')
@click.pass_obj
@check_dry_run
def delete(obj: ZabbixCTL):
    selected_graphs = ask_graphs(obj.graphs)
    if len(selected_graphs) == 0:
        click.echo('There is no graph.')
        exit(0)

    if click.confirm(
            f'delete:\n{pprint.pformat([(graph["host"], graph["name"]) for graph in selected_graphs])}',
            default=False,
            abort=True,
            show_default=True):
        obj.zapi.graph.delete(*[graph['graphid'] for graph in selected_graphs])
