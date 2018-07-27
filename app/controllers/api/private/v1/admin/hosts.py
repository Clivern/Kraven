"""
Hosts API Endpoint
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


class Hosts(View):

    __request = Request()
    __response = Response()
    __helpers = Helpers()
    __form = Form()
    __logger = None
    __user_id = None
    __host_module = Host_Module()


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)


    def post(self, request):
        pass



class Host(View):

    __request = Request()
    __response = Response()
    __helpers = Helpers()
    __form = Form()
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = Host_Module()


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)


    def post(self, request, host_id):
       pass


    def delete(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__host_module.delete_host(self.__host_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Host deleted successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting a host.")
            }]))

