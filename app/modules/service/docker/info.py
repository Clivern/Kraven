"""
Info Module
"""

import docker

class Info():

    __client = None

    def __init__(self, server, auth_data={}):
        self.__client = docker.DockerClient(base_url=server)

    def get_version(self):
        return self.__client.version()