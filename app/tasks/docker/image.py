"""
Docker Image Tasks
"""

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
            return {
                "status": "passed",
                "result": "{}",
                "notify_type": "passed"
            }
        else:
            return {
                "status": "failed",
                "result": "{}",
                "notify_type": "failed"
            }
    except Exception as e:
        return {
            "status": "error",
            "result": {
                "error": str(e)
            },
            "notify_type": "error"
        }



@shared_task
def build_image(host_id):
    pass


@shared_task
def prune_images(host_id):
    pass


@shared_task
def remove_image(host_id):
    pass
