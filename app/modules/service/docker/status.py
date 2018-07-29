"""
Status Module
"""

import docker

# local Django
from app.modules.service.docker.auth import Auth

class Status():

    __client = None

    def connect(self, server, auth_data={}):
        try:
            self.__client = docker.DockerClient(base_url=server)
            self.__client.ping()
        except Exception as e:
            self.__client = False

    def check_health(self, server, auth_data={}):
        self.connect(server, auth_data)

        if self.__client == False:
            return False

        return True