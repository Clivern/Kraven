"""
Auth Module
"""

import docker

class Auth():

    __client = None

    def connect(self, server, auth_data={}):
        try:
            self.__client = docker.DockerClient(base_url=server)
        except Exception as e:
            self.__client = False