"""
Event Module
"""

import json
# local Django
from .auth import Auth


class Event(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)

    def list(self, since=None, until=None):
        events = self._client.events(
            since=int(since) if since is not None else since,
            until=int(until) if until is not None else until
        )
        final_events = []
        for event in events:
            final_events.append(json.loads(event))
        return final_events
