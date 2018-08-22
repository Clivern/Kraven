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
from app.modules.core.task import Task as Task_Core


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



class Pull_Image(View):

    __request = Request()
    __response = Response()
    __helpers = Helpers()
    __form = Form()
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = Host_Module()
    __task_core = Task_Core()


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)


    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "repository" : ""
        })

        self.__form.add_inputs({
            'repository': {
                'value': request_data["repository"],
                'validate': {}
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        task = self.__task_core.delay("pull_image", {
            "host_id": self.__host_id,
            "repository": self.__form.get_input_value("repository")
        }, self.__user_id)

        if task:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Request is In Progress!")
            }], {
                "task_id": task.id
            }))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating request.")
            }]))



class Remove_Image(View):
    pass



class Get_Image(View):
    pass



class Get_Images(View):
    pass



class Tag_Image(View):
    pass



class Search_Community_Images(View):
    pass








