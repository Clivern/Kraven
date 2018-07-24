"""
Base Job
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.option_entity import Option_Entity


class Base():

    __option_entity = Option_Entity()
    __helpers = Helpers()
    __logger = None
    __arguments = {
        "app_name": "",
        "app_email": "",
        "app_url": ""
    }


    def __init__(self, arguments):
        self.__logger = self.__helpers.get_logger(__name__)
        self.__arguments.update(arguments)
        self.__load_options()


    def __load_options(self):
        options = self.__option_entity.get_many_by_keys(["app_name", "app_email", "app_url"])
        for option in options:
            if option.key in self.__arguments.keys():
                self.__arguments[option.key] = option.value