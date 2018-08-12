"""
Settings Module
"""

# standard library
import time

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.user_entity import User_Entity
from app.modules.entity.profile_entity import Profile_Entity
from app.modules.entity.host_entity import Host_Entity
from app.modules.entity.task_entity import Task_Entity


class Metric():

    __option_entity = Option_Entity()
    __user_entity = User_Entity()
    __host_entity = Host_Entity()
    __task_entity = Task_Entity()
    __profile_entity = Profile_Entity()
    __helpers = Helpers()
    __logger = None
    __app_name = ""


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)
        self.__app_name = self.__option_entity.get_value_by_key("app_name").lower()


    def get_all_users(self):
        return {
            "type": "count",
            "record": "%s_all_users" % self.__app_name,
            "count": self.__user_entity.count_all_users(),
            "comment": "Current All Users on System"
        }


    def get_all_profiles(self):
        return {
            "type": "count",
            "record": "%s_all_profiles" % self.__app_name,
            "count": self.__profile_entity.count_all_profiles(),
            "comment": "Current All Profiles on System"
        }


    def get_all_tasks(self):
        return {
            "type": "count",
            "record": "%s_all_tasks" % self.__app_name,
            "count": self.__task_entity.count_all_tasks(),
            "comment": "Current All Tasks on System"
        }


    def get_all_hosts(self):
        return {
            "type": "count",
            "record": "%s_all_hosts" % self.__app_name,
            "count": self.__host_entity.count_all_hosts(),
            "comment": "Current All Hosts on System"
        }