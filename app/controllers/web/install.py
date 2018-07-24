"""
Install Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.install import Install as Install_Module


class Install(View):

    template_name = 'templates/install.html'
    __context = Context()
    __install = Install_Module()
    __option_entity = Option_Entity()


    def get(self, request):

        if self.__install.is_installed():
            return redirect("app.web.login")

        self.__context.push({
            "page_title": _("Installation · %s") % self.__option_entity.get_value_by_key("app_name", os.getenv("APP_NAME", "Kraven"))
        })

        return render(request, self.template_name, self.__context.get())