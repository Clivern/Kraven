"""
Host Networks API Endpoints
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
from app.modules.service.docker.network import Network as Network_Module


class Create_Network(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __network_id = None
    __host_module = None
    __network_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):
        pass


class Get_Network(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __network_id = None
    __host_module = None
    __network_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def get(self, request, host_id, network_id):
        pass


class Get_Networks(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __network_id = None
    __host_module = None
    __network_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def get(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__network_module.set_host(self.__host_id).check_health():
            _host = self.__host_module.get_one_by_id(host_id)
            return JsonResponse(self.__response.send_private_success([], {
                'networks': self.__format_networks(
                    self.__network_module.list(),
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
                'networks': []
            }))

    def __format_networks(self, networks_list, host_id, host_slug):
        _networks_list = []

        for network in networks_list:
            date = network["created"].split("T")
            network["created_at"] = date[0]
            network["url"] = "#"
            network["delete_url"] = "#"
            # network["url"] = reverse("app.web.admin.hosts.view.network", kwargs={'host_slug': host_slug, 'network_id': network['long_id']})
            # network["delete_url"] = reverse("app.api.private.v1.admin.action.host.delete_network.endpoint", kwargs={'host_id': host_id})
            _networks_list.append(network)

        return _networks_list


class Remove_Network(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __network_id = None
    __host_module = None
    __network_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "long_id": ""
        })

        self.__form.add_inputs({
            'long_id': {
                'value': request_data["long_id"],
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

        _long_id = self.__form.get_input_value("long_id")

        task = self.__task_module.delay("remove_network_by_id", {
            "host_id": self.__host_id,
            "long_id": _long_id
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Removing docker network"),
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


class Connect_Network_Container(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __network_id = None
    __host_module = None
    __network_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):
        pass


class Disconnect_Network_Container(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __network_id = None
    __host_module = None
    __network_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):
        pass


class Prune_Networks(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __network_id = None
    __host_module = None
    __network_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        task = self.__task_module.delay("prune_unused_networks", {
            "host_id": self.__host_id
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("prune unused networks."),
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
