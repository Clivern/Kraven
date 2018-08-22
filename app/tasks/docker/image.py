"""
Docker Image Tasks
"""

# Django
from django.utils.translation import gettext as _

# Third party
from celery import shared_task

# Local Django
from app.modules.service.docker.image import Image


@shared_task
def pull_image(host_id, repository):
    try:
        _image = Image()
        result = _image.set_host(host_id).pull(repository)
        if result:
            return {"status": "passed", "result": "{}"}
        else:
            return {"status": "failed", "result": "{}"}
    except Exception as e:
        return {"status": "failed", "result": str(e)}


@shared_task
def build_image(host_id):
    pass



@shared_task
def prune_images(host_id):
    pass



@shared_task
def remove_image(host_id):
    pass