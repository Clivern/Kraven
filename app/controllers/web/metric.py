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
from app.modules.core.decorators import protect_metric_with_auth_key
from app.modules.core.metric import Metric


class Metric(View):

    __prometheus = Prometheus()
    __metric = Metric()


    @redirect_if_not_installed
    @protect_metric_with_auth_key
    def get(self, request, type):

        if not type in ("prometheus"):
            raise Http404("Page not found.")

        if type == "prometheus":

            self.__prometheus.set_metrics([
                self.__metric.get_all_users(),
                self.__metric.get_all_profiles(),
                self.__metric.get_all_hosts(),
                self.__metric.get_all_tasks()
            ])

            return HttpResponse(self.__prometheus.get_plain_metrics(), content_type='text/plain')