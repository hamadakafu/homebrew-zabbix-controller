import re


def get_hosts(zapi, match=None, time_range=None):
    """
    return hosts: [dict]
    """

    # output=["name", "available"]等指定可能だが面倒なので全部持ってくる
    hosts = zapi.host.get()
    if match is not None:
        hosts = list(filter(
            lambda host: re.search(list(match.values())[0], host[list(match.keys())[0]]) is not None,
            hosts,
        ))

    if time_range is not None:
        hosts = list(filter(
            lambda host: time_range['from'] <= int(host[time_range['key']]) <= time_range['to'],
            hosts,
        ))
    return hosts


def update_hosts(zpai, host, data):
    """
    host をupdateする
    """
    # TODO: updateする


