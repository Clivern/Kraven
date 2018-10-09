"""
Auth Module
"""

import json

# Third Party
import docker

# local Django
from app.models import Host
from app.modules.util.crypto import Crypto
from app.modules.util.io import Directory
from app.modules.util.io import File
from app.settings.info import APP_ROOT


class Auth():

    _client = None
    _host_id = None
    _host = None
    _retry = 3
    _timeout = 1
    __crypto = None
    __directory = None
    __file = None
    __host_auth_storage = "%s/storage/app/private/host/%d/auth_data"

    def __init__(self, host_id=None):
        self.__crypto = Crypto()
        self.__directory = Directory()
        self.__file = File()

        self._host_id = host_id
        if host_id is not None:
            host = Host.objects.get(pk=host_id)
            if host.pk:
                host.server = self.__crypto.decrypt(host.server, host.token)
                host.auth_data = self.__crypto.decrypt(host.auth_data, host.token)
                host.auth_data = json.loads(host.auth_data)
                self._host = host
                self.__cache_auth_data()
            else:
                self._host = False

    def set_host(self, host_id):
        self._host_id = host_id
        host = Host.objects.get(pk=host_id)
        if host.pk:
            host.server = self.__crypto.decrypt(host.server, host.token)
            host.auth_data = self.__crypto.decrypt(host.auth_data, host.token)
            host.auth_data = json.loads(host.auth_data)
            self._host = host
            self.__cache_auth_data()
        else:
            self._host = False

        return self

    def check_health(self, client_type="docker_client"):
        for x in range(0, self._retry):
            if self._ping(client_type):
                return True
        return False

    def _ping(self, client_type="docker_client"):
        try:
            if client_type == "docker_client":
                self._client = docker.DockerClient(base_url=self._host.server, tls=self.tls_config(), timeout=self._timeout)
            else:
                self._client = docker.APIClient(base_url=self._host.server, tls=self.tls_config(), timeout=self._timeout)

            return self._client.ping()
        except Exception as e:
            return False

    def tls_config(self):
        if self._host.auth_data["auth_type"] == "no_auth":
            return False
        elif self._host.auth_data["auth_type"] == "tls_server_client":
            return docker.tls.TLSConfig(
                ca_cert=(self.__host_auth_storage + '/ca.pem') % (APP_ROOT, self._host.id),
                client_cert=(
                    (self.__host_auth_storage + '/cert.pem') % (APP_ROOT, self._host.id),
                    (self.__host_auth_storage + '/key.pem') % (APP_ROOT, self._host.id)
                ),
                verify=True
            )
        elif self._host.auth_data["auth_type"] == "tls_client_only":
            return docker.tls.TLSConfig(
                client_cert=(
                    (self.__host_auth_storage + '/cert.pem') % (APP_ROOT, self._host.id),
                    (self.__host_auth_storage + '/key.pem') % (APP_ROOT, self._host.id)
                ),
                verify=True
            )
        elif self._host.auth_data["auth_type"] == "tls_server_only":
            return docker.tls.TLSConfig(
                ca_cert=(self.__host_auth_storage + '/ca.pem') % (APP_ROOT, self._host.id),
                verify=True
            )
        elif self._host.auth_data["auth_type"] == "tls_only":
            return True

    def __cache_auth_data(self):

        if self._host.auth_data["auth_type"] == "no_auth":
            return False

        host_path = self.__host_auth_storage % (APP_ROOT, self._host.id)

        if not self.__directory.exists(host_path):
            self.__directory.create(host_path)

        if not self.__file.exists("%s/cache_time.log" % host_path):
            self.__file.write("%s/cache_time.log" % host_path, "")

        cache_time = self.__file.read("%s/cache_time.log" % host_path)

        if cache_time != "%s,%s" % (str(self._host.created_at), str(self._host.updated_at)):
            self.__file.write("%s/cache_time.log" % host_path, "%s,%s" % (str(self._host.created_at), str(self._host.updated_at)))
            self.__file.write("%s/ca.pem" % host_path, self._host.auth_data["tls_ca_certificate"])
            self.__file.write("%s/cert.pem" % host_path, self._host.auth_data["tls_certificate"])
            self.__file.write("%s/key.pem" % host_path, self._host.auth_data["tls_key"])

        if not self.__file.exists("%s/ca.pem" % host_path) or \
                not self.__file.exists("%s/cert.pem" % host_path) or not self.__file.exists("%s/key.pem" % host_path):
            self.__file.write("%s/cache_time.log" % host_path, "%s,%s" % (str(self._host.created_at), str(self._host.updated_at)))
            self.__file.write("%s/ca.pem" % host_path, self._host.auth_data["tls_ca_certificate"])
            self.__file.write("%s/cert.pem" % host_path, self._host.auth_data["tls_certificate"])
            self.__file.write("%s/key.pem" % host_path, self._host.auth_data["tls_key"])
