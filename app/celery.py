"""
Celery Configs
"""

# standard library
import os
from importlib import import_module

# Third party
from celery import Celery
from celery.signals import task_success


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.basic")


app = Celery('app')

# namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@task_success.connect
def after_task(sender=None,result=None,**kwargs):
    if sender.request.id and "status" in result and "result" in result:
        p = import_module("app.modules.core.task")
        c = getattr(p, "Task")
        c().update_task_with_uuid(
            sender.request.id, {
            "status": result["status"],
            "result": result["result"]
        })