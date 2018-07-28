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

        self.__user_id = request.user.id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "name" : "",
            "slug" : "",
            "server": "",
            "type": "",
            "auth_type": ""
        })

        self.__form.add_inputs({
            'name': {
                'value': request_data["name"],
                'validate': {
                    'host_name': {
                        'error': _("Error! Host Name is invalid.")
                    },
                    'length_between':{
                        'param': [3, 41],
                        'error': _("Error! Host slug length must be from 4 to 40 characters.")
                    }
                }
            },
            'slug': {
                'value': request_data["slug"],
                'validate': {
                    'host_slug': {
                        'error': _('Error! Host slug is not valid.')
                    },
                    'length_between':{
                        'param': [3, 21],
                        'error': _('Error! Host slug length must be from 4 to 20 characters.')
                    }
                }
            },
            'server': {
                'value': request_data["server"],
                'validate': {
                    'host_server': {
                        'error': _('Error! Host server is not valid.')
                    },
                    'length_between':{
                        'param': [3, 21],
                        'error': _('Error! Host server length must be from 4 to 20 characters.')
                    }
                }
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of':{
                        'param': [["docker"]],
                        'error': _('Error! Host type is invalid.')
                    }
                }
            },
            'auth_type': {
                'value': request_data["auth_type"],
                'validate': {
                    'any_of':{
                        'param': [["no"]],
                        'error': _('Error! Auth type is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        if self.__host_module.slug_used(self.__form.get_input_value("slug"), self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Host slug is already used.")
            }]))


        result = self.__host_module.insert_one({
            "name": self.__form.get_input_value("name"),
            "slug": self.__form.get_input_value("slug"),
            "server": self.__form.get_input_value("server"),
            "type": self.__form.get_input_value("type"),
            "auth_data": self.__helpers.json_dumps({
                "auth_type": self.__form.get_input_value("auth_type")
            }),
            "user_id": self.__user_id
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Host created successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating host.")
            }]))



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


        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "name" : "",
            "slug" : "",
            "server": "",
            "type": "",
            "auth_type": ""
        })

        self.__form.add_inputs({
            'name': {
                'value': request_data["name"],
                'validate': {
                    'host_name': {
                        'error': _("Error! Host Name is invalid.")
                    },
                    'length_between':{
                        'param': [3, 41],
                        'error': _("Error! Host slug length must be from 4 to 40 characters.")
                    }
                }
            },
            'slug': {
                'value': request_data["slug"],
                'validate': {
                    'host_slug': {
                        'error': _('Error! Host slug is not valid.')
                    },
                    'length_between':{
                        'param': [3, 21],
                        'error': _('Error! Host slug length must be from 4 to 20 characters.')
                    }
                }
            },
            'server': {
                'value': request_data["server"],
                'validate': {
                    'host_server': {
                        'error': _('Error! Host server is not valid.')
                    },
                    'length_between':{
                        'param': [3, 21],
                        'error': _('Error! Host server length must be from 4 to 20 characters.')
                    }
                }
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of':{
                        'param': [["docker"]],
                        'error': _('Error! Host type is invalid.')
                    }
                }
            },
            'auth_type': {
                'value': request_data["auth_type"],
                'validate': {
                    'any_of':{
                        'param': [["no"]],
                        'error': _('Error! Auth type is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        if self.__host_module.slug_used_elsewhere(self.__host_id, self.__form.get_input_value("slug"), self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Host slug is already used.")
            }]))

        result = self.__host_module.update_one_by_id(self.__host_id, {
            "name": self.__form.get_input_value("name"),
            "slug": self.__form.get_input_value("slug"),
            "server": self.__form.get_input_value("server"),
            "type": self.__form.get_input_value("type"),
            "auth_data": self.__helpers.json_dumps({
                "auth_type": self.__form.get_input_value("auth_type")
            }),
            "user_id": self.__user_id
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Host updated successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating host.")
            }]))


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

