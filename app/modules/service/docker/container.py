"""
Container Module
"""

# local Django
from .auth import Auth


class Container(Auth):

    def __init__(self, host_id=None):
        Auth.__init__(self, host_id)
