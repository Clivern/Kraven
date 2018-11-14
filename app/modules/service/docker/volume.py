"""
Volume Module
"""

# local Django
from .auth import Auth


class Volume(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)

    def list(self):
        result = []
        volumes_list = self._client.volumes.list()
        for volume in volumes_list:
            result.append({
                "long_id": volume.id,
                "short_id": volume.short_id,
                "name": volume.name,
                "created": volume.attrs["CreatedAt"],
                "driver": volume.attrs["Driver"],
                "scope": volume.attrs["Scope"],
                "attrs": volume.attrs
            })
        return result

    def get(self, volume_id):
        volume = self._client.volumes.get(volume_id)

        return {
            "id": volume.id,
            "short_id": volume.short_id,
            "name": volume.name,
            "created": volume.attrs["CreatedAt"],
            "driver": volume.attrs["Driver"],
            "scope": volume.attrs["Scope"],
            "attrs": volume.attrs
        }

    def remove(self, volume_id, force=False):
        return self._client.volumes.get(volume_id).remove(force)

    def prune(self, filters=None):
        return self._client.volumes.prune(filters)

    def create(self, name, driver, driver_opts={}, labels={}):
        return self._client.volumes.create(
            name=name,
            driver=driver,
            driver_opts=driver_opts,
            labels=labels
        )
