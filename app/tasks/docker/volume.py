"""
Docker Volume Tasks
"""

# Third party
from celery import shared_task

# Django
from django.utils.translation import gettext as _

# Local Django
from app.modules.service.docker.volume import Volume as Volume_Module


@shared_task
def create_volume(host_id, name, driver, driver_opts={}, labels={}):
    try:
        _volume = Volume_Module()

        if not _volume.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _volume.create(
            name,
            driver,
            driver_opts=driver_opts,
            labels=labels
        )

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
def remove_volume_by_id(host_id, volume_id, force=False):
    try:
        _volume = Volume_Module()

        if not _volume.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        _volume.remove(volume_id, force)

        return {
            "status": "passed",
            "result": "{}",
            "notify_type": "passed"
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
def prune_unused_volumes(host_id):
    try:
        _volume = Volume_Module()

        if not _volume.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _volume.prune()

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
