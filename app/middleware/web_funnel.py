"""
Logging Middleware
"""

# Django
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from app.modules.util.helpers import Helpers
from app.modules.core.funnel import Funnel
from app.modules.core.response import Response
from app.modules.entity.option_entity import Option_Entity


class Web_Funnel():

    __helpers = Helpers()
    __logger = None
    __funnel = Funnel()
    __roles = {

    }


    def __init__(self, get_response):
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)


    def __call__(self, request):

        self.__funnel.set_rules(self.__roles)
        self.__funnel.set_request(request)

        if self.__funnel.action_needed():
            return self.__funnel.fire()

        response = self.get_response(request)

        return response