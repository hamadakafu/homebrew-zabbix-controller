from pprint import pprint

import click

from . import main, ZabbixCTL
from ..utils import validate_match, validate_time_range, validate_json, check_dry_run, ask_hosts
from .apis import get_hosts


@main.group(help='host command entry point')
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'key:pattern\n'
                    'ex1) name:^some -> This matches some, some-host, ...\n'
                    'ex2) hostid:41 -> This matches 4123232, 111141, ...'
                    'ex3) name:^$ -> This matches empty string')
              )
@click.option('-tr', '--time-range',
              callback=validate_time_range,
              help=('For search by time range. Using unixtime\n'
                    'key:[from]-[to].\n'
                    'If you use --match at the same time, these mean "and operator"'
                    '"from" must be less than "to".\n'
                    'ex1) errors_from:48120471-140834017 -> 48120471~140834017\n'
                    'ex2) errors_from:- -> 0~[now unixtime]\n'
                    'ex3) disable_until:-7184 -> 0~7184\n')
              )
@click.pass_obj
def hosts(obj, match, time_range):
    """
    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    match: dict
        Key is host property in zabbix api.
        Value is regular expresion used by re.
        Each items is chained && operator, not ||.
    time_range: dict
        Keys are 'key', 'from', 'to'.
        Values are str, int, int.
        'from' <= host['key'] <= 'to'

    """
    _hosts = get_hosts(obj.zapi, match=match, time_range=time_range)

    if len(_hosts) == 0:
        print('There is no host')
        exit(0)

    obj.hosts = _hosts


@hosts.command(name='list', help='list hosts')
@click.pass_obj
def _list(obj):
    """
    List hosts.

    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    """
    click.echo(obj.hosts)


@hosts.command(help='delete hosts')
@click.pass_obj
@check_dry_run
def delete(obj):
    """
    Delete hosts.

    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    """
    selected_hosts = ask_hosts(obj.hosts)
    if len(selected_hosts) == 0:
        print('No host is selected.')
        exit(0)
    obj.selected_hosts = selected_hosts
    if click.confirm(f'delete hosts: {[host["name"] for host in selected_hosts]}',
                     default=False,
                     abort=True,
                     show_default=True):
        obj.zapi.host.delete(*[host['hostid'] for host in selected_hosts])


@hosts.command(help='disable hosts')
@click.pass_obj
@check_dry_run
def disable(obj):
    """
    Disable hosts. It is deprecated.

    Parameters
    ----------
    obj: ZabbixCTL
    """
    selected_hosts = ask_hosts(obj.hosts)
    if len(selected_hosts) == 0:
        print('No host is selected.')
        exit(0)
    obj.selected_hosts = selected_hosts
    if click.confirm(f'disabled {[host["name"] for host in selected_hosts]}',
                     default=False,
                     abort=True,
                     show_default=True):
        for host in selected_hosts:
            result = obj.zapi.host.update(hostid=host['hostid'], status=1)
            pprint(result)


@hosts.command(help='update hosts')
@click.option('-d', '--data', callback=validate_json, help='data for update', required=True)
@click.pass_obj
@check_dry_run
def update(obj, data):
    """
    Update hosts.

    Parameters
    ----------
    obj: ZabbixCTL
        Including command state.
    data: dict
        New data
    """
    # TODO: 作成
    click.echo(data)
