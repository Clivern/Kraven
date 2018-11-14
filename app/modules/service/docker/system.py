"""
System Module
"""

# local Django
from .auth import Auth


class System(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)

    def info(self):
        return self._client.info()

    def version(self):
        return self._client.version()
