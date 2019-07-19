import re
from pyzabbix import ZabbixAPI


def get_hosts(zapi, match=None, time_range=None):
    """
    Get hosts matching 'match' and 'time_range'

    Parameters
    ----------
    zapi: ZabbixAPI
    match: [dict]
        [{'name': 'some_name'}]
    time_range: dict
        {'key': 'error_from', 'from': 0, 'to': int(time.time())}

    Returns
    -------
    hosts: [dict]
        list of host object.
    """

    hosts = zapi.host.get()
    if match is not None:
        for m in match:
            hosts = list(filter(
                lambda host: re.search(list(m.values())[0], host[list(m.keys())[0]]) is not None,
                hosts,
            ))

    if time_range is not None:
        hosts = list(filter(
            lambda host: time_range['from'] <= int(host[time_range['key']]) <= time_range['to'],
            hosts,
        ))

    return hosts


def update_hosts(zapi, hosts, data):
    """
    update host

    Parameters
    ----------
    zapi: ZabbixAPI
        ZabbixAPI object
    hosts: [dict]
        list of host object
    data: dict
        new data

    Returns
    -------
    results: list
    """
    results = []
    for host in hosts:
        result = zapi.host.update(hostid=host['hostid'], **data)
        results.append(result)

    return results
