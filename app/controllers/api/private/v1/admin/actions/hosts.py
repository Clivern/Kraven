"""
Hosts Actions API Endpoints
"""

# Django
from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.host import Host as Host_Module
from app.modules.service.docker.status import Status


class Health_Check(View):

    __request = Request()
    __response = Response()
    __helpers = Helpers()
    __form = Form()
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = Host_Module()
    __status = Status()


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)


    def get(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        health = self.__status.set_host(self.__host_id).ping()

        if health:
            return JsonResponse(self.__response.send_private_success([], {"status": "up"}))
        else:
            return JsonResponse(self.__response.send_private_success([], {"status": "down"}))