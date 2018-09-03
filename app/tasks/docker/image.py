"""
Docker Image Tasks
"""

# Third party
from celery import shared_task

# Django
from django.utils.translation import gettext as _

# Local Django
from app.modules.service.docker.image import Image as Image_Module


@shared_task
def pull_image(host_id, image_name):
    try:
        _image = Image_Module()

        if not _image.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        image_name = image_name.split(":")
        result = _image.pull(
            image_name[0],
            image_name[1]
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
def build_image(host_id, fileobj, tag, rm=False, nocache=False):
    try:
        _image = Image_Module()

        if not _image.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _image.build(
            fileobj=fileobj,
            tag=tag,
            rm=rm,
            nocache=nocache
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
def prune_unused_images(host_id):
    try:
        _image = Image_Module()

        if not _image.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _image.prune_unused()

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
def prune_all_unused_images(host_id):
    try:
        _image = Image_Module()

        if not _image.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _image.prune_all_unused()

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
def remove_image_by_id(host_id, long_id, force=False, noprune=False):
    try:
        _image = Image_Module()

        if not _image.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _image.remove_by_id(
            long_id=long_id,
            force=force,
            noprune=noprune
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
def remove_image_by_name(host_id, repository, tag, force=False, noprune=False):
    try:
        _image = Image_Module()

        if not _image.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _image.remove_by_name(
            repository=repository,
            tag=tag,
            force=force,
            noprune=noprune
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
def tag_image_by_id(host_id, long_id, repository, tag=None, force=False):
    try:
        _image = Image_Module()

        if not _image.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _image.tag_by_id(
            long_id=long_id,
            repository=repository,
            tag=tag,
            force=force
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
