"""
Docker Image Tasks
"""

# Django
from django.utils.translation import gettext as _

# Third party
from celery import shared_task


@shared_task
def pull_image(host_id):
    pass



@shared_task
def build_image(host_id):
    pass



@shared_task
def prune_images(host_id):
    pass



@shared_task
def remove_image(host_id):
    pass