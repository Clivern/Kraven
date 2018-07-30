"""
Status Module
"""

import docker

# local Django
from app.modules.service.docker.auth import Auth

class Status():

    __client = None
    __retry = 3

    def check_health(self, server, auth_data={}):
        for x in range(0, self.__retry):
            if self.__ping(server, auth_data):
                return True

        return False


    def __ping(self, server, auth_data={}):
        try:
            self.__client = docker.DockerClient(base_url=server)
            return self.__client.ping()
        except Exception as e:
            return False