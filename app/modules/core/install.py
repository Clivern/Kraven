"""
Install Module
"""

# Django
from django.core.management import execute_from_command_line

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.user_entity import User_Entity


class Install():

    __option_entity = None
    __user_entity = None
    __options = [
        {"key": "app_installed", "value": "true", "autoload": True},
        {"key": "app_description", "value": "", "autoload": False},
        {"key": "google_analytics_account", "value": "", "autoload": True},
        {"key": "reset_mails_messages_count", "value": "5", "autoload": False},
        {"key": "reset_mails_expire_after", "value": "24", "autoload": False},
        {"key": "access_tokens_expire_after", "value": "48", "autoload": False}
    ]
    __admin = {
        "username" : "",
        "email" : "",
        "password" : "",
        "is_superuser": True,
        "is_active": True,
        "is_staff": False
    }
    __helpers = None
    __logger = None


    def __init__(self):
        self.__option_entity = Option_Entity()
        self.__user_entity = User_Entity()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)


    def is_installed(self):
        return False if self.__option_entity.get_one_by_key("app_installed") == False else True


    def set_app_data(self, name, email, url):
        self.__options.append({"key": "app_name", "value": name, "autoload": True})
        self.__options.append({"key": "app_email", "value": email, "autoload": True})
        self.__options.append({"key": "app_url", "value": url, "autoload": True})


    def set_admin_data(self, username, email, password):
        self.__admin["username"] = username
        self.__admin["email"] = email
        self.__admin["password"] = password


    def install(self):
        try:
            execute_from_command_line(["manage.py", "migrate"])
        except Exception as e:
            self.__logger.error("Error While Running Migrations: %s" % e)
            return False

        status = True
        status &= self.__option_entity.insert_many(self.__options)
        status &= (self.__user_entity.insert_one(self.__admin) != False)
        return status