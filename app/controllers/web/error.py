"""
Error Web Controller
"""

# standard library
import os

# Django
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.util.helpers import Helpers


def handler500(request, exception=None, template_name='templates/500.html'):

    helpers = Helpers()
    logger = helpers.get_logger(__name__)

    if exception is not None:
        logger.error("Server Error: %s" % exception)

    template_name = 'templates/500.html'

    context = Context()

    context.autoload_options()
    context.push({
        "page_title": _("500 · %s") % context.get("app_name", os.getenv("APP_NAME", "Kraven"))
    })

    return render(request, template_name, context.get(), status=500)
