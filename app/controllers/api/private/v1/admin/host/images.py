"""
Host Images API Endpoints
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
from app.modules.service.docker.image import Image as Image_Module


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


class Build_Image(View):

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
            "tag": "",
            "dockerfile": "",
            "rm": "",
            "nocache": ""
        })

        self.__form.add_inputs({
            'tag': {
                'value': request_data["tag"],
                'sanitize': {

                },
                'validate': {
                }
            },
            'dockerfile': {
                'value': request_data["dockerfile"],
                'sanitize': {
                },
                'validate': {
                }
            },
            'rm': {
                'value': request_data["rm"],
                'sanitize': {
                },
                'validate': {
                }
            },
            'nocache': {
                'value': request_data["nocache"],
                'sanitize': {
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

        _tag = self.__form.get_input_value("tag")
        _fileobj = self.__form.get_input_value("dockerfile")
        _rm = bool(self.__form.get_input_value("rm") == "1")
        _nocache = bool(self.__form.get_input_value("nocache") == "1")

        task = self.__task_module.delay("build_image", {
            "host_id": self.__host_id,
            "fileobj": _fileobj,
            "tag": _tag,
            "rm": _rm,
            "nocache": _nocache
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": "building docker image %s" % _tag,
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


class Remove_Image_By_Id(View):

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
            "long_id": "",
            "force": "",
            "noprune": ""
        })

        self.__form.add_inputs({
            'long_id': {
                'value': request_data["long_id"],
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
            },
            'noprune': {
                'value': request_data["noprune"],
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
        _force = bool(self.__form.get_input_value("force") == "1")
        _noprune = bool(self.__form.get_input_value("noprune") == "1")

        task = self.__task_module.delay("remove_image_by_id", {
            "host_id": self.__host_id,
            "long_id": _long_id,
            "force": _force,
            "noprune": _noprune
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Removing docker image"),
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


class Remove_Image_By_Name(View):

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
            "repository": "",
            "tag": "",
            "force": "",
            "noprune": ""
        })

        self.__form.add_inputs({
            'repository': {
                'value': request_data["repository"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'tag': {
                'value': request_data["tag"],
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
            },
            'noprune': {
                'value': request_data["noprune"],
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

        _repository = self.__form.get_input_value("repository")
        _tag = self.__form.get_input_value("tag")
        _force = self.__form.get_input_value("force")
        _noprune = self.__form.get_input_value("noprune")

        task = self.__task_module.delay("remove_image_by_name", {
            "host_id": self.__host_id,
            "repository": _repository,
            "tag": _tag,
            "force": _force,
            "noprune": _noprune
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Removing docker image %s:%s") % (_repository, _tag),
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


class Prune_Unused_Images(View):

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

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        task = self.__task_module.delay("prune_unused_images", {
            "host_id": self.__host_id
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("prune unused docker images"),
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


class Prune_All_Unused_Images(View):

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

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        task = self.__task_module.delay("prune_all_unused_images", {
            "host_id": self.__host_id
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("prune all unused docker images"),
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


class Get_Image(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __host_id = None
    __image_id = None
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

    def get(self, request, host_id, image_id):

        self.__user_id = request.user.id
        self.__host_id = host_id
        self.__image_id = image_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__image_module.set_host(self.__host_id).check_health():
            _image = {
                'long_id': self.__image_id
            }
            return JsonResponse(self.__response.send_private_success([], {
                'image': _image
            }))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong with your host!"
                )
            }], {
                'image': {}
            }))


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

    def get(self, request, host_id):

        self.__user_id = request.user.id
        self.__host_id = host_id

        if not self.__host_module.user_owns(self.__host_id, self.__user_id):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        if self.__image_module.set_host(self.__host_id).check_health():
            _host = self.__host_module.get_one_by_id(host_id)
            return JsonResponse(self.__response.send_private_success([], {
                'images': self.__format_image(self.__image_module.list(), host_id, _host.slug)
            }))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _(
                    "Error! Something goes wrong with your host!"
                )
            }], {
                'images': []
            }))

    def __format_image(self, images_list, host_id, host_slug):
        _image_list = []

        for image in images_list:
            date = image["created"].split("T")
            image["created_at"] = date[0]
            image["size"] = image["size"]["MB"]
            _tags = []
            for tag in image["tags"]:
                tag = tag.split(":")
                _tags.append({"name": tag[0], "version": tag[1]})
            image["tags"] = _tags
            image["url"] = reverse("app.web.admin.hosts.view.image", kwargs={'host_slug': host_slug, 'image_id': image['long_id']})
            image["delete_url"] = reverse("app.api.private.v1.admin.action.host.delete_image.endpoint", kwargs={'host_id': host_id})
            _image_list.append(image)

        return _image_list


class Tag_Image_By_Id(View):

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
            "long_id": "",
            "repository": "",
            "tag": "",
            "force": ""
        })

        self.__form.add_inputs({
            'long_id': {
                'value': request_data["long_id"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'repository': {
                'value': request_data["repository"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                }
            },
            'tag': {
                'value': request_data["tag"],
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

        _long_id = self.__form.get_input_value("long_id")
        _repository = self.__form.get_input_value("repository")
        _tag = self.__form.get_input_value("tag")
        _force = self.__form.get_input_value("force")

        task = self.__task_module.delay("tag_image_by_id", {
            "host_id": self.__host_id,
            "long_id": _long_id,
            "repository": _repository,
            "tag": _tag,
            "force": _force
        }, self.__user_id)

        if task:

            self.__notification_module.create_notification({
                "highlight": "",
                "notification": _("Tag docker image as %s:%s") % (_repository, _tag),
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
                "message": _("Error! Something goes wrong with your host!")
            }]))
