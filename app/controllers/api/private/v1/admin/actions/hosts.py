"""
Hosts Actions API Endpoints
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.host import Host as Host_Module
from app.modules.service.docker.status import Status
from app.modules.core.task import Task as Task_Module
from app.modules.core.notification import Notification as Notification_Module
from app.modules.service.docker.image import Image as Image_Module


class Health_Check(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = None
    __status = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__status = Status()
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
            return JsonResponse(self.__response.send_private_success(
                [],
                {"status": "up"}
            ))
        else:
            return JsonResponse(self.__response.send_private_success(
                [],
                {"status": "down"}
            ))


class Pull_Image(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = None
    __task_module = None
    __notification_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__task_module = Task_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "image_name": ""
        })

        self.__form.add_inputs({
            'image_name': {
                'value': request_data["image_name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'not_empty': {
                        'error': _('Error! docker image is required!')
                    },
                    'length_between': {
                        'param': [1, 100],
                        'error': _('Error! a valid docker image is required!')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(
                self.__form.get_errors(with_type=True)
            ))

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        _image_name = self.__form.get_input_value("image_name")

        if ":" not in _image_name:
            _image_name = "%s:latest" % _image_name

        task = self.__task_module.delay("pull_image", {
            "host_id": self.__host_id,
            "image_name": _image_name
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": "pulling docker image %s" % _image_name,
                "url": "#",
                "type": Notification_Module.PENDING,
                "delivered": False,
                "user_id": self.__user_id,
                "host_id": self.__host_id,
                "task_id": task.id
            })

            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Request is in progress!")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong while creating request."
                )
            }]))


class Remove_Image(View):
    pass


class Get_Image(View):
    pass


class Get_Images(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = None
    __image_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__image_module = Image_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "repository": ""
        })

        self.__form.add_inputs({
            'repository': {
                'value': request_data["repository"],
                'validate': {
                    'not_empty': {
                        'error': _('Error! docker image is required!')
                    },
                    'length_between': {
                        'param': [1, 100],
                        'error': _('Error! a valid docker image is required!')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(
                self.__form.get_errors(with_type=True)
            ))

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__image_module.set_host(self.__host_id).check_health():
            result = self.__image_module.list()
            print(result)
            return JsonResponse(self.__response.send_private_success([], {}))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong with your host!"
                )
            }]))


class Tag_Image(View):
    pass


class Search_Community_Images(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = None
    __image_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__image_module = Image_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "term": ""
        })

        self.__form.add_inputs({
            'term': {
                'value': request_data["term"],
                'validate': {
                    'not_empty': {
                        'error': _('Error! Search term is required!')
                    },
                    'length_between': {
                        'param': [1, 100],
                        'error': _('Error! a valid search term is required!')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(
                self.__form.get_errors(with_type=True)
            ))

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__image_module.set_host(self.__host_id).check_health():
            result = self.__image_module.search(self.__form.get_input_value("term"))
            print(result)
            return JsonResponse(self.__response.send_private_success([], {}))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong with your host!"
                )
            }]))
