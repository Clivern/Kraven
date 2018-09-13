"""
Host Volumes API Endpoints
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