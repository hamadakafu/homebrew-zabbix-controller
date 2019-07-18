from .command import hosts
from ..utils import *
from . import ZabbixCTL


@hosts.group(help='host graph')
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'key:pattern\n'
                    'ex1) name:^some -> This matches some, some-graph, ...\n'
                    'ex2) graphid:41 -> This matches 4123232, 111141, ...'
                    'ex3) name:^$ -> This matches empty string')
              )
@click.pass_obj
def graphs(obj: ZabbixCTL, match):
    """
    graphsコマンドのエントリーポイント
    obj.graphsにホストとグラフのペアを入れる
    graphs = [{hostname: 'hgeo', graphs: [graph]}]
    """

    _graphs = []
    for host in obj.hosts:
        h_graphs = get_graphs(obj.zapi, host, match=match)
        if len(h_graphs) == 0:
            continue
        _graphs.append({'hostname': host['name'], 'graphs': h_graphs})
    if len(_graphs) == 0:
        print(f"There is no graph in {host['name']}")
        exit(0)

    obj.graphs = _graphs


@graphs.command(name='list', help='list graph')
@click.pass_obj
def _list(obj):
    click.echo(obj.graphs)


@graphs.command(help='delete graph')
@click.pass_obj
@check_dry_run
def delete(obj: ZabbixCTL):
    if obj.dry_run:
        click.echo(f'{obj}')
        exit(0)

    for graph in obj.graphs:
        selected_graphs = ask_graphs(graph['hostname'], graph['graphs'])
        if len(selected_graphs) == 0:
            print('No graph is selected.')
            continue
        if click.confirm(
                f'delete {graph["hostname"]}: {[graph["name"] for graph in selected_graphs]}',
                default=False,
                abort=True,
                show_default=True):
            obj.zapi.graph.delete(*[graph['graphid'] for graph in selected_graphs])
