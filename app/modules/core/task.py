"""
Task Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.task_entity import Task_Entity


class Task():

    __task_entity = Task_Entity()
    __helpers = Helpers()
    __logger = None


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)


    def update_task_with_uuid(self, uuid, task):
        return self.__task_entity.update_one_by_uuid(uuid, task)


    def create_task(self, task):
        return self.__task_entity.insert_one(task)