"""
Health Check Command

see https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/
"""

# standard library
import os
import sys

# Django
from django.core.management import utils
from django.core.management.base import BaseCommand, CommandError

# local Django
from app.settings.info import *


class Command(BaseCommand):

    help = "Health Check Kraven!"

    available = [
        "check"
    ]


    def add_arguments(self, parser):
        """Config Command Args"""
        parser.add_argument('command', type=str, nargs='+', help='Available commands are %s' % ", ".join(self.available))


    def handle(self, *args, **options):
        """Command Handle"""
        if len(options['command']) == 0 or options['command'][0] not in self.available:
            raise CommandError('Command Does not exist! Please use one of the following: python manage.py health [%s]' % ", ".join(self.available))


        if options['command'][0] == "check":
            print("Hello")