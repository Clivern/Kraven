"""
Client Module
"""

# standard library
import json

# Third Party
from docker import APIClient

# local Django
from app.models import Host
from app.modules.util.crypto import Crypto


class Client():

    _client = None
    _host_id = None
    _host = None
    _retry = 3
    __crypto = Crypto()

    def __init__(self, host_id=None):
        self._host_id = host_id
        if host_id is not None:
            host = Host.objects.get(pk=host_id)
            if host.pk:
                host.server = self.__crypto.decrypt(host.server, host.token)
                host.auth_data = self.__crypto.decrypt(host.auth_data, host.token)
                self._host = host
            else:
                self._host = False

    def set_host(self, host_id):
        self._host_id = host_id
        host = Host.objects.get(pk=host_id)
        if host.pk:
            host.server = self.__crypto.decrypt(host.server, host.token)
            host.auth_data = self.__crypto.decrypt(host.auth_data, host.token)
            self._host = host
        else:
            self._host = False

        return self

    def check_health(self):
        for x in range(0, self._retry):
            if self._ping():
                return True
        return False

    def _ping(self):
        try:
            self._client = APIClient(base_url=self._host.server)
            return self._client.ping()
        except Exception as e:
            return False

    def _pretty_response(self, response):
        result = ""
        line = json.loads(response)

        if "id" in line:
            result += "%s: " % str(line["id"])

        if "status" in line:
            result += "%s" % str(line["status"])

        if "progress" in line:
            result += "%s%s" % (' '*20, str(line["progress"]))

        return result
