"""
Ping API Endpoint
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
from app.modules.core.profile import Profile as Profile_Module
from app.modules.core.context import Context


class Auth(View):


    def get(self):
        # To get current refresh token
        pass


    def post(self):
        # To Get your new API token in case it is expired
        pass