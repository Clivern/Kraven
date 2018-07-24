"""
Kraven Info Command

see https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/
"""

# standard library
import time
import json
from importlib import import_module

# Django
from django.core.management.base import BaseCommand, CommandError

# local Django
from app.settings.info import *
from app.modules.util.helpers import Helpers
from app.modules.entity.job_entity import Job_Entity


class Command(BaseCommand):

    help = "Run Kraven Schedule!"

    available = [
        "run"
    ]

    __job_entity = Job_Entity()
    __helpers = Helpers()
    __logger = None


    def add_arguments(self, parser):
        """Config Command Args"""
        parser.add_argument('command', type=str, nargs='+', help='Available commands are %s' % ", ".join(self.available))


    def handle(self, *args, **options):
        self.__logger = self.__helpers.get_logger(__name__)
        """Command Handle"""
        if len(options['command']) == 0 or options['command'][0] not in self.available:
            raise CommandError('Command Does not exist! Please use one of the following: python manage.py schedule [%s]' % ", ".join(self.available))

        if options['command'][0] == "run":
            self.stdout.write(self.style.SUCCESS("█ Running Kraven Schedule...\n"))
            while True:
                job = self.get_job()
                if job != False:
                    self.run(job)
                time.sleep(2)


    def get_job(self):
        """Get a Job To Run"""
        return self.__job_entity.get_one_to_run()


    def run(self, job):
        """Run The Job"""
        try:
            job_module = job.executor.split(".")
            p = import_module("app.jobs.%s" % (job_module[0]))
            c = getattr(p, job_module[1])
            instance = c(json.loads(job.parameters))
            if instance.execute():
                return self.__job_entity.update_after_run(job, Job_Entity.PASSED)
            else:
                return self.__job_entity.update_after_run(job, Job_Entity.FAILED)
        except Exception as e:
            self.__logger.error("Error while running job#%s: %s" % (job.pk, e))
            return self.__job_entity.update_after_run(job, Job_Entity.ERROR)