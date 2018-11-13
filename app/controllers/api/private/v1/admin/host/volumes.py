"""
Host Volumes API Endpoints
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.urls import reverse

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.host import Host as Host_Module
from app.modules.core.task import Task as Task_Module
from app.modules.core.notification import Notification as Notification_Module
from app.modules.service.docker.volume import Volume as Volume_Module


class Create_Volume(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __volume_id = None
    __host_module = None
    __volume_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__task_module = Task_Module()
        self.__volume_module = Volume_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "volume_name": "",
            "volume_driver": ""
        })

        self.__form.add_inputs({
            'volume_name': {
                'value': request_data["volume_name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'volume_driver': {
                'value': request_data["volume_driver"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
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

        _volume_name = self.__form.get_input_value("volume_name")
        _volume_driver = self.__form.get_input_value("volume_driver")

        task = self.__task_module.delay("create_volume", {
            "host_id": self.__host_id,
            "name": _volume_name,
            "driver": _volume_driver
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Creating a new volume"),
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


class Get_Volume(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __volume_id = None
    __host_module = None
    __volume_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__task_module = Task_Module()
        self.__volume_module = Volume_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def get(self, request, host_id, volume_id):

        self.__user_id = request.user.id
        self.__host_id = host_id
        self.__volume_id = volume_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__volume_module.set_host(self.__host_id).check_health():
            _volume = self.__volume_module.get(self.__volume_id)

            return JsonResponse(self.__response.send_private_success([], {
                'volume': _volume
            }))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong with your host!"
                )
            }], {
                'volume': {}
            }))


class Get_Volumes(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __volume_id = None
    __host_module = None
    __volume_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__volume_module = Volume_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def get(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__volume_module.set_host(self.__host_id).check_health():
            _host = self.__host_module.get_one_by_id(host_id)
            return JsonResponse(self.__response.send_private_success([], {
                'volumes': self.__format_volumes(
                    self.__volume_module.list(),
                    host_id,
                    _host.slug
                )
            }))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong with your host!"
                )
            }], {
                'volumes': []
            }))

    def __format_volumes(self, volumes_list, host_id, host_slug):
        _volumes_list = []

        for volume in volumes_list:
            date = volume["created"].split("T")
            volume["created_at"] = date[0]
            volume["url"] = reverse("app.web.admin.hosts.view.volume", kwargs={'host_slug': host_slug, 'volume_id': volume['long_id']})
            volume["delete_url"] = reverse("app.api.private.v1.admin.action.host.delete_volume.endpoint", kwargs={'host_id': host_id})
            if volume["short_id"] in volume["name"]:
                volume["name"] = volume["short_id"]
            _volumes_list.append(volume)

        return _volumes_list


class Remove_Volume(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __volume_id = None
    __host_module = None
    __volume_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__task_module = Task_Module()
        self.__volume_module = Volume_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "volume_id": "",
            "force": ""
        })

        self.__form.add_inputs({
            'volume_id': {
                'value': request_data["volume_id"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'force': {
                'value': request_data["force"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
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

        _volume_id = self.__form.get_input_value("volume_id")
        _force = self.__form.get_input_value("force")

        task = self.__task_module.delay("remove_volume_by_id", {
            "host_id": self.__host_id,
            "volume_id": _volume_id,
            "force": (_force == "on")
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Removing docker volume"),
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


class Prune_Volumes(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __volume_id = None
    __host_module = None
    __volume_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__volume_module = Volume_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        task = self.__task_module.delay("prune_unused_volumes", {
            "host_id": self.__host_id
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Prune unused volumes."),
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
