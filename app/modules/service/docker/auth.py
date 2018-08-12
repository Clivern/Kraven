"""
Auth Module
"""

# Third Party
import docker

# local Django
from app.models import Host


class Auth():

    _client = None
    _host_id = None
    _host = None
    _retry = 3


    def __init__(self, host_id = None):
        self._host_id = host_id
        if host_id != None:
            host = Host.objects.get(pk=host_id)
            self._host = False if host.pk is None else host


    def set_host(self, host_id):
        self._host_id = host_id
        host = Host.objects.get(pk=host_id)
        self._host = False if host.pk is None else host

        return self


    def check_health(self):
        for x in range(0, self._retry):
            if self._ping():
                return True
        return False


    def _ping(self):
        try:
            self._client = docker.DockerClient(base_url=self._host.server)
            return self._client.ping()
        except Exception as e:
            return False