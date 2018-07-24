"""
Response Module
"""

# Django
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from app.modules.util.helpers import Helpers


class Response():

    __private = {}
    __public = {}
    __helpers = None
    __logger = None


    def __init__(self):
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)


    def send_private_success(self, messages, payload={}):
        self.__private["status"] = "success"
        self.__private["messages"] = messages
        if len(payload) > 0:
            self.__private["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(self.__private) + "\n")
        return self.__private


    def send_private_failure(self, messages, payload={}):
        self.__private["status"] = "failure"
        self.__private["messages"] = messages
        if len(payload) > 0:
            self.__private["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(self.__private) + "\n")
        return self.__private


    def send_public_success(self, messages, payload={}):
        self.__public["status"] = "success"
        self.__public["messages"] = messages
        if len(payload) > 0:
            self.__public["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(self.__public) + "\n")
        return self.__public


    def send_public_failure(self, messages, payload={}):
        self.__public["status"] = "failure"
        self.__public["messages"] = messages
        if len(payload) > 0:
            self.__public["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(self.__public) + "\n")
        return self.__public