"""
Settings Web Controller
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
from app.modules.core.upgrade import Upgrade
from app.modules.core.context import Context


class Settings(View):

    template_name = 'templates/admin/settings.html'
    __context = Context()
    __upgrade = Upgrade()


    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.load_options({
            "app_name": "",
            "app_email": "",
            "app_url": "",
            "app_description": "",
            "google_analytics_account": "",
            "reset_mails_messages_count": "",
            "reset_mails_expire_after": "",
            "access_tokens_expire_after": ""
        })

        self.__context.push({
            "current": self.__upgrade.get_current_version(),
            "latest": self.__upgrade.get_latest_version()
        })

        self.__context.push({
            "page_title": _("Settings · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Kraven"))
        })

        return render(request, self.template_name, self.__context.get())