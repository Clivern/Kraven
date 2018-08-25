"""
Login Web Controller
"""

# standard library
import os

# Django
from django.shortcuts import reverse
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.decorators import redirect_if_authenticated
from app.modules.core.decorators import redirect_if_not_installed


class Login(View):

    template_name = 'templates/login.html'
    __context = Context()
    __option_entity = Option_Entity()

    @redirect_if_not_installed
    @redirect_if_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.push({
            "page_title": _("Login · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Kraven"))
        })

        if "redirect" in request.GET:
            self.__context.push({
                "redirect_url": request.GET["redirect"]
            })
        else:
            self.__context.push({
                "redirect_url": reverse("app.web.admin.dashboard")
            })

        return render(request, self.template_name, self.__context.get())
