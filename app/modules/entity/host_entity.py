"""
Host Entity Module
"""

# Django
from django.contrib.auth.models import User

# local Django
from app.models import Host
from app.models import Host_Meta
from app.modules.util.helpers import Helpers

# Third party
from app.modules.util.crypto import Crypto


class Host_Entity():

    __crypto = Crypto()

    def insert_one(self, host):
        """Insert a New Host"""
        token = self.__crypto.get_token()
        host = Host(
            name=host["name"],
            slug=host["slug"],
            type=host["type"],
            server=self.__crypto.encrypt(host["server"], token),
            auth_data=self.__crypto.encrypt(host["auth_data"], token),
            user=User.objects.get(pk=host["user_id"]),
            token=token
        )

        host.save()
        return False if host.pk is None else host


    def insert_many(self, hosts):
        """Insert Many Hosts"""
        status = True
        for host in hosts:
            status &= True if self.insert_one(host) != False else False
        return status


    def get_one_by_id(self, id):
        """Get Host By ID"""
        try:
            host = Host.objects.get(pk=id)
            host.server = self.__crypto.decrypt(host.server, host.token)
            host.auth_data = self.__crypto.decrypt(host.auth_data, host.token)
            return False if host.pk is None else host
        except:
            return False


    def user_owns(self, host_id, user_id):
        """Get Host By ID and User ID"""
        try:
            host = Host.objects.get(pk=host_id, user=user_id)
            return False if host.pk is None else True
        except:
            return False


    def get_one_by_slug_user_id(self, slug, user_id):
        """Get Host By Slug"""
        try:
            host = Host.objects.get(slug=slug, user=user_id)
            host.server = self.__crypto.decrypt(host.server, host.token)
            host.auth_data = self.__crypto.decrypt(host.auth_data, host.token)
            return False if host.pk is None else host
        except:
            return False


    def get_many_by_user(self, user_id, order_by, asc):
        """Get Many Hosts By User ID"""
        hosts = Host.objects.filter(user=user_id).order_by(order_by if asc else "-%s" % order_by)
        return hosts


    def update_one_by_id(self, id, new_data):
        """Update Host By ID"""
        host = self.get_one_by_id(id)
        if host != False:
            if "name" in new_data:
                host.name = new_data["name"]

            if "slug" in new_data:
                host.slug = new_data["slug"]

            if "type" in new_data:
                host.type = new_data["type"]

            if "status" in new_data:
                host.status = new_data["status"]

            if "server" in new_data:
                host.server = self.__crypto.encrypt(new_data["server"], host.token)

            if "auth_data" in new_data:
                host.auth_data = self.__crypto.encrypt(new_data["auth_data"], host.token)

            if "user_id" in new_data:
                host.user = User.objects.get(pk=new_data["user_id"])

            host.save()
            return True
        return False


    def delete_one_by_id(self, id):
        """Delete Host By ID"""
        host = self.get_one_by_id(id)
        if host != False:
            count, deleted = host.delete()
            return True if count > 0 else False
        return False


    def count_all_hosts(self):
        return Host.objects.count()