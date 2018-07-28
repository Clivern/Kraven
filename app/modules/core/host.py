"""
Host Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.host_entity import Host_Entity


class Host():

    __helpers = Helpers()
    __logger = None
    __host_entity = Host_Entity()


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)


    def user_owns(self, host_id, user_id):
        return self.__host_entity.user_owns(host_id, user_id)


    def delete_host(self, host_id):
        return self.__host_entity.delete_one_by_id(host_id)


    def slug_used(self, slug, user_id):
        return (self.__host_entity.get_one_by_slug_user_id(slug, user_id) != False)


    def slug_used_elsewhere(self, host_id, slug, user_id):
        host = self.__host_entity.get_one_by_slug_user_id(slug, user_id)
        return False if host == False or host.id == host_id else True


    def get_one_by_slug_user_id(self, slug, user_id):
        return self.__host_entity.get_one_by_slug_user_id(slug, user_id);


    def insert_one(self, host):
        return self.__host_entity.insert_one(host)


    def get_many_by_user(self, user_id, order_by, asc):
        return self.__host_entity.get_many_by_user(user_id, order_by, asc)


    def update_one_by_id(self, host_id, new_data):
        return self.__host_entity.update_one_by_id(host_id, new_data)