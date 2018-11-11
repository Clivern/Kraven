"""
Docker Network Tasks
"""

# Third party
from celery import shared_task

# Django
from django.utils.translation import gettext as _

# Local Django
from app.modules.service.docker.network import Network as Network_Module


@shared_task
def create_network(host_id, network_name, network_driver):
    try:
        _network = Network_Module()

        if not _network.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _network.create(network_name, driver=network_driver)

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
def remove_network_by_id(host_id, network_id):
    try:
        _network = Network_Module()

        if not _network.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

            _network.remove(network_id)

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
def connect_network_container(host_id, network_id, container_id):
    try:
        _network = Network_Module()

        if not _network.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

            _network.connect(network_id, container_id)

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
def disconnect_network_container(host_id, network_id, container_id):
    try:
        _network = Network_Module()

        if not _network.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

            _network.disconnect(network_id, container_id)

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
def prune_unused_networks(host_id):
    try:
        _network = Network_Module()

        if not _network.set_host(host_id).check_health():
            return {
                "status": "failed",
                "result": {
                    "error": _("Error, Unable to connect to docker host!")
                },
                "notify_type": "failed"
            }

        result = _network.prune()

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
