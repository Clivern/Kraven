"""
Hosts API Endpoint
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
from app.modules.service.docker.status import Status


class Hosts(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
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

    def get(self, request):

        self.__user_id = request.user.id

        return JsonResponse(self.__response.send_private_success([], {
            'hosts': self.__format_host(self.__host_module.get_many_by_user(self.__user_id, "created_at", False))
        }))

    def post(self, request):

        self.__user_id = request.user.id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "name": "",
            "slug": "",
            "server": "",
            "type": "",
            "auth_type": "",
            "tls_ca_certificate": "",
            "tls_certificate": "",
            "tls_key": ""
        })

        self.__form.add_inputs({
            'name': {
                'value': request_data["name"],
                'validate': {
                    'host_name': {
                        'error': _("Error! Host Name is invalid.")
                    },
                    'length_between': {
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
                    'length_between': {
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
                    'length_between': {
                        'param': [3, 60],
                        'error': _('Error! Host server length must be from 4 to 20 characters.')
                    }
                }
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of': {
                        'param': [["docker"]],
                        'error': _('Error! Host type is invalid.')
                    }
                }
            },
            'auth_type': {
                'value': request_data["auth_type"],
                'validate': {
                    'any_of': {
                        'param': [["no_auth", "tls_server_client", "tls_client_only", "tls_server_only", "tls_only"]],
                        'error': _('Error! Auth type is invalid.')
                    }
                }
            },
            'tls_ca_certificate': {
                'value': request_data["tls_ca_certificate"],
                'validate': {
                    'optional': {},
                    'tls_certificate': {
                        'error': _('Error! TLS CA Certificate is invalid.')
                    }
                }
            },
            'tls_certificate': {
                'value': request_data["tls_certificate"],
                'validate': {
                    'optional': {},
                    'tls_certificate': {
                        'error': _('Error! TLS Certificate is invalid.')
                    }
                }
            },
            'tls_key': {
                'value': request_data["tls_key"],
                'validate': {
                    'optional': {},
                    'tls_certificate': {
                        'error': _('Error! TLS Key is invalid.')
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
                "auth_type": self.__form.get_input_value("auth_type"),
                "tls_ca_certificate": self.__form.get_input_value("tls_ca_certificate"),
                "tls_certificate": self.__form.get_input_value("tls_certificate"),
                "tls_key": self.__form.get_input_value("tls_key")
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

    def __format_host(self, hosts_list):
        _hosts_list = []

        for host in hosts_list:
            _status = "up" if self.__status.set_host(host.id).ping() else "down"
            _hosts_list.append({
                "id": host.id,
                "name": host.name,
                "slug": host.slug,
                "status": _status,
                "type": host.type.capitalize(),
                "created_at": host.created_at.strftime("%b %d %Y %H:%M:%S"),
                "view_url": reverse("app.web.admin.hosts.view", kwargs={'host_slug': host.slug}),
                "edit_url": reverse("app.web.admin.hosts.edit", kwargs={'host_slug': host.slug}),
                "delete_url": reverse("app.api.private.v1.admin.host.endpoint", kwargs={'host_id': host.id})
            })

        return _hosts_list


class Host(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __host_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__host_module = Host_Module()
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
            "name": "",
            "slug": "",
            "server": "",
            "type": "",
            "auth_type": "",
            "tls_ca_certificate": "",
            "tls_certificate": "",
            "tls_key": ""
        })

        self.__form.add_inputs({
            'name': {
                'value': request_data["name"],
                'validate': {
                    'host_name': {
                        'error': _("Error! Host Name is invalid.")
                    },
                    'length_between': {
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
                    'length_between': {
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
                    'length_between': {
                        'param': [3, 60],
                        'error': _('Error! Host server length must be from 4 to 20 characters.')
                    }
                }
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of': {
                        'param': [["docker"]],
                        'error': _('Error! Host type is invalid.')
                    }
                }
            },
            'auth_type': {
                'value': request_data["auth_type"],
                'validate': {
                    'any_of': {
                        'param': [["no_auth", "tls_server_client", "tls_client_only", "tls_server_only", "tls_only"]],
                        'error': _('Error! Auth type is invalid.')
                    }
                }
            },
            'tls_ca_certificate': {
                'value': request_data["tls_ca_certificate"],
                'validate': {
                    'optional': {},
                    'tls_certificate': {
                        'error': _('Error! TLS CA Certificate is invalid.')
                    }
                }
            },
            'tls_certificate': {
                'value': request_data["tls_certificate"],
                'validate': {
                    'optional': {},
                    'tls_certificate': {
                        'error': _('Error! TLS Certificate is invalid.')
                    }
                }
            },
            'tls_key': {
                'value': request_data["tls_key"],
                'validate': {
                    'optional': {},
                    'tls_certificate': {
                        'error': _('Error! TLS Key is invalid.')
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
                "auth_type": self.__form.get_input_value("auth_type"),
                "tls_ca_certificate": self.__form.get_input_value("tls_ca_certificate"),
                "tls_certificate": self.__form.get_input_value("tls_certificate"),
                "tls_key": self.__form.get_input_value("tls_key")
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
