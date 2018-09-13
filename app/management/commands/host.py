"""
Hosts Management Command

see https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/
"""
# Django
from django.core.management.base import BaseCommand, CommandError
from app.modules.service.docker.image import Image as Image_Module
from app.modules.service.docker.volume import Volume as Volume_Module
from app.modules.util.io import File
import json


class Command(BaseCommand):

    help = "Manage Hosts!"

    available = [
        "exec"
    ]

    def add_arguments(self, parser):
        """Config Command Args"""
        parser.add_argument('command', type=str, nargs='+', help='Available commands are %s' % ", ".join(self.available))

    def handle(self, *args, **options):
        """Command Handle"""
        if len(options['command']) == 0 or options['command'][0] not in self.available:
            raise CommandError('Command Does not exist! Please use one of the following: python manage.py health [%s]' % ", ".join(self.available))

        try:
            configs = {}
            for param in options["command"]:
                if "=" in param:
                    param = param.split("=")
                    configs[param[0]] = param[1]

            if options['command'][0] == "exec":
                getattr(self, options["command"][1])(configs)
        except Exception as e:
            print("Something goes wrong: %s" % str(e))

    def pull_image(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.pull(configs["repository"], configs["tag"]))

    def list_images(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.list())

    def prune_unused_images(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.prune_unused())

    def prune_all_unused_images(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.prune_all_unused())

    def remove_image_by_name(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.remove_by_name(configs["repository"], configs["tag"]))

    def remove_image_by_id(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.remove_by_id(configs["image_id"], configs["force"] == "True"))

    def get_image_by_id(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.get_by_id(configs["image_id"]))

    def tag_image_by_id(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.tag_by_id(configs["image_id"], configs["repository"], configs["tag"]))

    def build_image(self, configs={}):
        _image = Image_Module()
        if _image.set_host(configs["host_id"]).check_health():
            print(_image.build(File().read(configs["dockerfile"]), configs["tag"]))

    def list_volumes(self, configs={}):
        _volume = Volume_Module()
        if _volume.set_host(configs["host_id"]).check_health():
            print(_volume.list())

    def get_volume(self, configs={}):
        _volume = Volume_Module()
        if _volume.set_host(configs["host_id"]).check_health():
            print(_volume.get(configs["volume_id"]))

    def remove_volume(self, configs={}):
        _volume = Volume_Module()
        if _volume.set_host(configs["host_id"]).check_health():
            print(_volume.remove(configs["volume_id"], configs["force"] == "True"))

    def prune_volumes(self, configs={}):
        _volume = Volume_Module()
        if _volume.set_host(configs["host_id"]).check_health():
            print(_volume.prune())

    def create_volume(self, configs={}):
        _volume = Volume_Module()
        if _volume.set_host(configs["host_id"]).check_health():
            print(_volume.create(
                name=configs["name"],
                driver=configs["driver"] if "driver" in configs else "local",
                driver_opts=json.loads(configs["driver_opts"]) if "driver_opts" in configs else {},
                labels=json.loads(configs["labels"]) if "labels" in configs else {}
            ))
