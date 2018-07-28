"""
Hosts Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.http import Http404

# local Django
from app.modules.util.helpers import Helpers
from app.modules.core.context import Context
from app.modules.core.host import Host as Host_Module


class Hosts_List(View):

    template_name = 'templates/admin/hosts/list.html'
    __context = Context()
    __host_module = Host_Module()


    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Hosts · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Kraven"))
        })

        self.__context.push({
            "hosts": self.__host_module.get_many_by_user(request.user.id, "created_at", True)
        })

        return render(request, self.template_name, self.__context.get())


class Host_Create(View):

    template_name = 'templates/admin/hosts/create.html'
    __context = Context()
    __host_module = Host_Module()


    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Create a Host · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Kraven"))
        })

        return render(request, self.template_name, self.__context.get())


class Host_Edit(View):

    template_name = 'templates/admin/hosts/edit.html'
    __context = Context()
    __host_module = Host_Module()
    __helpers = Helpers()


    def get(self, request, host_slug):

        host = self.__host_module.get_one_by_slug_user_id(host_slug, request.user.id)

        if host == False or request.user.id != host.user.id:
            raise Http404("Host not found.")

        host.auth_data = self.__helpers.json_loads(host.auth_data);

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit %s Host · %s") % (host.name, self.__context.get("app_name", os.getenv("APP_NAME", "Kraven"))),
            "host": host
        })

        return render(request, self.template_name, self.__context.get())



class Host_View(View):

    template_name = 'templates/admin/hosts/view.html'
    __context = Context()
    __host_module = Host_Module()


    def get(self, request, host_slug):

        host = self.__host_module.get_one_by_slug_user_id(host_slug, request.user.id)

        if host == False or request.user.id != host.user.id:
            raise Http404("Host not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("%s Host · %s") % (host.name, self.__context.get("app_name", os.getenv("APP_NAME", "Kraven"))),
            "host": host
        })

        return render(request, self.template_name, self.__context.get())