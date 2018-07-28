"""
Host Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User


class Host(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )

    TYPE_CHOICES = (
        ('docker', 'DOCKER'),
    )

    STATUS_CHOICES = (
        ('running', 'RUNNING'),
        ('down', 'DOWN'),
    )

    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.SlugField(max_length=60, db_index=True, verbose_name="Slug")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="docker", verbose_name="Type")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="running", verbose_name="Status")
    server = models.CharField(max_length=200, verbose_name="Connection")
    auth_data = models.TextField(verbose_name="Auth Data")
    last_status_check = models.DateTimeField(auto_now_add=True, verbose_name="Last Status Check")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")