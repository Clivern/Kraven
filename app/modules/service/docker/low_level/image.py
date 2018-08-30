"""
Image Module
"""

# local Django
from .client import Client


class Image(Client):

    def __init__(self, host_id=None):
        Client.__init__(self, host_id)

    def pull(self, repository, tag="latest", stream=True):
        return self._client.pull("%s:%s" % (repository, tag), stream=True)
