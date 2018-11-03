"""
Network Module
"""

# local Django
from .auth import Auth


class Network(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)

    def list(self):
        result = []
        networks_list = self._client.networks.list()
        for network in networks_list:
            result.append({
                "id": network.id,
                "short_id": network.short_id,
                "name": network.name,
                "created": network.attrs["Created"],
                "driver": network.attrs["Driver"],
                "scope": network.attrs["Scope"],
                "containers": network.containers,
                "attrs": network.attrs
            })
        return result

    def get(self, network_id):
        return self._client.networks.get(network_id)

    def remove(self, network_id):
        return self._client.networks.get(network_id).remove()

    def prune(self, filters=None):
        return self._client.networks.prune(filters)

    def disconnect(self, network_id, container, **configs):
        self._client.networks.get(network_id).disconnect(container, **configs)

    def connect(self, network_id, container, **configs):
        self._client.networks.get(network_id).connect(container, **configs)

    def create(self, name, **args):
        return self._client.networks.create(name=name, **args)
