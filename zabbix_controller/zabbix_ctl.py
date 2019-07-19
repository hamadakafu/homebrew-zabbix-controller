import pprint


class ZabbixCTL(object):
    def __init__(self, zapi, hosts=None, graphs=None, **kwargs):
        self.zapi = zapi
        self.hosts = hosts
        self.graphs = graphs
        self.main_options = kwargs

    def __repr__(self):
        return 'zabbixctl-options: {!s}\nhosts: {!s}\ngraphs: {}'.format(
            pprint.pformat(self.main_options),
            pprint.pformat(self.hosts),
            pprint.pformat(self.graphs),
        )

