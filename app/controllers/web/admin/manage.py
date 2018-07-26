"""
Manage Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context


class Manage(View):

    template_name = 'templates/admin/manage.html'
    __context = Context()
    __user_id = None


    def get(self, request):

        self.__user_id = request.user.id

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Manage · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Kraven"))
        })

        return render(request, self.template_name, self.__context.get())