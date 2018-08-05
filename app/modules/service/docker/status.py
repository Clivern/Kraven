"""
Status Module
"""

import docker

# local Django
from .auth import Auth

class Status(Auth):


    def __init__(self, host_id = None):
        Auth.__init__(self, host_id)


    def ping(self):
        return self.check_health()