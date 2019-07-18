import re
import time
import json
from functools import wraps

from pyzabbix import ZabbixAPI
from bullet import Check
import click

from .zabbix_ctl import ZabbixCTL


def zabbix_auth(host, username, password, basicauth_username=None, basicauth_password=None):
    zapi = ZabbixAPI(host)
    if basicauth_username is not None and basicauth_password is not None:
        # Basic 認証
        zapi.session.auth = (basicauth_username, basicauth_password)
    # SLL/TLSの検証をするかどうかFalseの場合は警告メッセージが出力
    zapi.session.verify = False  # TODO: Trueにすべきかもしれない
    zapi.timeout = 5.1  # (秒)
    zapi.login(username, password)
    return zapi


def validate_match(ctx, param, values):
    if values is not None:
        if ':' not in values:  # --host-patternを指定するなら:区切りでしていする必要あるので
            raise click.BadParameter('Please include ":" in --host-pattern. Run --help')
        k, v = values.split(':', 1)  # 最初に現れた":"に対してのみsplitする
        values = {k: v}
    return values


def validate_time_range(ctx, param, values):
    """
    key:[unixtime]-[unixtime]をパースする
    errors_from:174134341-1841471834
    return {'key': 'errors_from', from: 174134341, to: 1841471834}
    errors_from:-
    return {'key': errors_from', from: 0, to: [今の時間]}
    """
    if values is not None:
        if ':' not in values:
            raise click.BadParameter('Please include ":" in --host-pattern. Run --help')
        k, v = values.split(':', 1)  # 最初に現れた":"に対してのみsplitする
        f, t = v.split('-')
        # -1047のとき 0-1047にする
        f = 0 if f == '' else int(f)
        # 71414-のとき 71414-[今の時間]にする
        t = int(time.time()) if t == '' else int(t)
        values = {'key': k, 'from': f, 'to': t}
    return values


def validate_json(ctx, param, values):
    """
    json形式のデータをdictに変換する
    """
    try:
        values = json.loads(values)
    except json.JSONDecodeError:
        raise click.BadParameter(f'You pass {values}. Please pass json format.')

    return values


def ask_hosts(hosts):
    """
    host を選択する
    return selected_hosts: [dict]
    """
    print('\n')  # ターミナルをリフレッシュ

    select_hostnames_cli = Check(
        prompt="Choose instance: input <space> to choose, then input <enter> to finish",
        choices=[host['name'] for host in hosts],
        align=4,
        margin=1,
    )
    hostnames = select_hostnames_cli.launch()
    selected_hosts = list(filter(lambda host: host['name'] in hostnames, hosts))

    return selected_hosts



def ask_graphs(hostname, graphs):
    """
    host: dict
    1つのホストに対して行う
    return graphs: [dicts]
    """
    print('\n')  # ターミナルをリフレッシュ
    choices = ['all']
    choices.extend([graph['name'] for graph in graphs])

    # 入力のバリデーションするのでwhile回す
    while True:
        select_graphnames_cli = Check(
            prompt=f"Choose graph in {hostname}: input <space> to choose, then input <enter> to finish",
            choices=choices,
            align=4,
            margin=1,
        )
        graphnames = select_graphnames_cli.launch()
        if 'all' in graphnames:
            if len(graphnames) != 1:  # all 選んだのに他の選ぶのはおかしい
                print('all選んで他の選ぶのは無効')
                continue
            else:
                selected_graphs = list(filter(lambda graph: graph['name'] in choices, graphs))
                return selected_graphs

        selected_graphs = list(filter(lambda graph: graph['name'] in graphnames, graphs))
        return selected_graphs


def check_dry_run(func):
    @wraps(func)
    def wrapped(obj: ZabbixCTL, *args, **kwargs):
        if obj.dry_run:
            click.echo(f'{obj}')
            # TODO: 関数のテストの仕方を考えている...zapiが呼ばれた回数をテストすれば良さそう
            exit(0)

        result = func(obj, *args, **kwargs)
        return result

    return wrapped
