from pprint import pprint

from . import main, ZabbixCTL
from ..utils import *


@main.group(help='hosts command')
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'key:pattern\n'
                    'ex1) name:^some -> This matches some, some-host, ...\n'
                    'ex2) hostid:41 -> This matches 4123232, 111141, ...'
                    'ex3) name:^$ -> This matches empty string')
              )
@click.option('-tm', '--time-match',
              callback=validate_time_match,
              help=('For search time pattern. Using unixtime\n'
                    'key:[from]-[to].\n'
                    'If you use --match at the same time, these mean and operator'
                    'From must be less than to.\n'
                    'ex1) errors_from:48120471-14834017 -> 48120471~14834017\n'
                    'ex2) errors_from:- -> 0~[now unixtime]\n'
                    'ex3) disable_until:-7184 -> 0~7184\n')
              )
@click.pass_obj
def hosts(obj: ZabbixCTL, match, time_match):
    """
    hostsコマンドのエントリーポイント
    """
    pprint(match)
    _hosts = get_hosts(obj.zapi, match=match, time_match=time_match)

    if len(_hosts) == 0:
        print('There is no host')
        exit(0)

    obj.hosts = _hosts


@hosts.command(name='list', help='list hosts')
@click.pass_obj
def _list(obj: ZabbixCTL):
    """
    hostsをリストする
    """
    click.echo(obj.hosts)


@hosts.command(help='delete hosts')
@click.pass_obj
@check_dry_run
def delete(obj: ZabbixCTL):
    """
    hostを削除する
    """
    if obj.dry_run:
        click.echo(f'{obj}')
        exit(0)

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
def disable(obj: ZabbixCTL):
    """
    hostを無効にする
    """
    if obj.dry_run:
        click.echo(f'{obj}')
        exit(0)

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
def update(obj: ZabbixCTL, data):
    """
    dataを渡してそれを使って更新する
    """
    if obj.dry_run:
        click.echo(f'{obj}')
        exit(0)

    # TODO: 作成
    click.echo(data)
