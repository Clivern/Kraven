"""
Metric Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.http import HttpResponse
from django.http import Http404

# local Django
from app.modules.service.prometheus import Prometheus
from app.modules.core.decorators import redirect_if_not_installed


class Metric(View):

    __prometheus = Prometheus()


    @redirect_if_not_installed
    def get(self, request, type):

        if not type in ("prometheus"):
            raise Http404("Page not found.")

        if type == "prometheus":

            self.__prometheus.set_metrics([
                {"type": "count","record": "users", "count": 2, "timestamp": 2346271, "comment": "Track Users"},
                {"type": "count","record": "hosts", "count": 2, "timestamp": 2346271}
            ])

            return HttpResponse(self.__prometheus.get_plain_metrics(), content_type='text/plain')