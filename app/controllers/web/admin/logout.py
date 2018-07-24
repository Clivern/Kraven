"""
Logout Web Controller
"""

# Django
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context


class Logout(View):

    __context = Context()


    def get(self, request):
        logout(request)
        messages.success(request, _("You've been logged out successfully"))
        return redirect("app.web.login")