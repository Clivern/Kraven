"""
Image Module
"""

import json

# local Django
from app.modules.service.docker.auth import Auth


class Image(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)

    def pull(self, repository, tag="latest", stream=True):
        return self._client.pull("%s:%s" % (repository, tag), stream=True)

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
