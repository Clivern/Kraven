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
        self.__task_module = Task_Module()
        self.__network_module = Network_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "network_name": "",
            "network_driver": ""
        })

        self.__form.add_inputs({
            'network_name': {
                'value': request_data["network_name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'network_driver': {
                'value': request_data["network_driver"],
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

        _network_name = self.__form.get_input_value("network_name")
        _network_driver = self.__form.get_input_value("network_driver")

        task = self.__task_module.delay("create_network", {
            "host_id": self.__host_id,
            "network_name": _network_name,
            "network_driver": _network_driver
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Creating a new network"),
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
        self.__task_module = Task_Module()
        self.__network_module = Network_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def get(self, request, host_id, network_id):

        self.__user_id = request.user.id
        self.__host_id = host_id
        self.__network_id = network_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__network_module.set_host(self.__host_id).check_health():
            _network = self.__network_module.get(self.__network_id)

            return JsonResponse(self.__response.send_private_success([], {
                'network': _network
            }))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong with your host!"
                )
            }], {
                'network': {}
            }))


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
        self.__task_module = Task_Module()
        self.__network_module = Network_Module()
        self.__notification_module = Notification_Module()
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
            network["url"] = reverse("app.web.admin.hosts.view.network", kwargs={'host_slug': host_slug, 'network_id': network['id']})
            network["delete_url"] = reverse("app.api.private.v1.admin.action.host.delete_network.endpoint", kwargs={'host_id': host_id})
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
        self.__task_module = Task_Module()
        self.__network_module = Network_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "network_id": ""
        })

        self.__form.add_inputs({
            'network_id': {
                'value': request_data["network_id"],
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

        _network_id = self.__form.get_input_value("network_id")

        task = self.__task_module.delay("remove_network_by_id", {
            "host_id": self.__host_id,
            "network_id": _network_id
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
        self.__task_module = Task_Module()
        self.__network_module = Network_Module()
        self.__notification_module = Notification_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "network_id": "",
            "container_id": ""
        })

        self.__form.add_inputs({
            'network_id': {
                'value': request_data["network_id"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'container_id': {
                'value': request_data["container_id"],
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

        _network_id = self.__form.get_input_value("network_id")
        _container_id = self.__form.get_input_value("container_id")

        task = self.__task_module.delay("connect_network_container", {
            "host_id": self.__host_id,
            "network_id": _network_id,
            "container_id": _container_id
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Connecting docker container to network"),
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
        self.__task_module = Task_Module()
        self.__network_module = Network_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "network_id": "",
            "container_id": ""
        })

        self.__form.add_inputs({
            'network_id': {
                'value': request_data["network_id"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'container_id': {
                'value': request_data["container_id"],
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

        _network_id = self.__form.get_input_value("network_id")
        _container_id = self.__form.get_input_value("container_id")

        task = self.__task_module.delay("connect_network_container", {
            "host_id": self.__host_id,
            "network_id": _network_id,
            "container_id": _container_id
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Disconnecting docker container from network"),
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
        self.__task_module = Task_Module()
        self.__network_module = Network_Module()
        self.__notification_module = Notification_Module()
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
                "notification": _("Prune unused networks"),
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
