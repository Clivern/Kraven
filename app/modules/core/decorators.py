"""
Custom Decorators
"""

# Django
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from app.modules.util.helpers import Helpers
from app.modules.core.response import Response
from app.modules.entity.option_entity import Option_Entity


def redirect_if_authenticated(function):
    def wrap(controller, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return redirect("app.web.admin.dashboard")
        return function(controller, request, *args, **kwargs)
    return wrap


def stop_request_if_authenticated(function):
    def wrap(controller, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            response = Response()
            return JsonResponse(response.send_private_failure([{
                "type": "error",
                "message": _("Error! Access forbidden for authenticated users.")
            }]))
        return function(controller, request, *args, **kwargs)
    return wrap


def redirect_if_not_installed(function):
    def wrap(controller, request, *args, **kwargs):
        installed = False if Option_Entity().get_one_by_key("app_installed") == False else True
        if not installed:
            return redirect("app.web.install")
        return function(controller, request, *args, **kwargs)
    return wrap


def stop_request_if_installed(function):
    def wrap(controller, request, *args, **kwargs):
        installed = False if Option_Entity().get_one_by_key("app_installed") == False else True
        if installed:
            response = Response()
            return JsonResponse(response.send_private_failure([{
                "type": "error",
                "message": _("Error! Application is already installed.")
            }]))
        return function(controller, request, *args, **kwargs)
    return wrap


def log_request_data(function):
    def wrap(controller, request, *args, **kwargs):
        _helper = Helpers()
        _logger = _helper.get_logger(__name__)
        _logger.debug(_("Request Method: %s") % request.method)
        _logger.debug(_("Request URL: %s") % request.path)
        _logger.debug(_("Request Body: %s") % request.body)
        return function(controller, request, *args, **kwargs)
    return wrap