"""
Forgot Password Module
"""

# standard library
from datetime import timedelta
import json

# Django
from django.utils import timezone
from django.utils.translation import gettext as _

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.user_entity import User_Entity
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.reset_request_entity import Reset_Request_Entity
from app.tasks import forgot_password_email
from app.modules.core.task import Task as Task_Core


class Forgot_Password():

    __reset_request_entity = None
    __option_entity = None
    __user_entity = None
    __task_core = None
    __helpers = None

    __reset_expire_option = 24
    __messages_count_option = 5


    def __init__(self):
        self.__reset_request_entity = Reset_Request_Entity()
        self.__option_entity = Option_Entity()
        self.__helpers = Helpers()
        self.__user_entity = User_Entity()
        self.__task_core = Task_Core()

        messages_count_option = self.__option_entity.get_one_by_key("reset_mails_messages_count")
        reset_expire_option = self.__option_entity.get_one_by_key("reset_mails_expire_after")

        if messages_count_option != False:
            self.__messages_count_option = int(messages_count_option.value)

        if reset_expire_option != False:
            self.__reset_expire_option = int(reset_expire_option.value)


    def check_email(self, email):
        return True if self.__user_entity.get_one_by_email(email) != False else False


    def reset_request_exists(self, email):
        return self.__reset_request_entity.get_one_by_email(email)


    def is_spam(self, request):
        if request.messages_count >= self.__messages_count_option and timezone.now() < request.expire_at:
            return True
        return False


    def update_request(self, request):

        # Delete Old Request
        self.__reset_request_entity.delete_one_by_id(request.id)

        # Create a Fresh Request
        if timezone.now() > request.expire_at:
            return self.create_request(request.email)

        # Create from the Old Request
        request = self.__reset_request_entity.insert_one({
            "email": request.email,
            "expire_at": request.expire_at,
            "messages_count": request.messages_count + 1

        })
        return request.token if request != False else False


    def create_request(self, email):
        request = self.__reset_request_entity.insert_one({
            "email": email,
            "expire_after": self.__reset_expire_option,
            "messages_count": 0

        })
        return request.token if request != False else False


    def send_message(self, email, token):

        app_name = self.__option_entity.get_value_by_key("app_name")
        app_email = self.__option_entity.get_value_by_key("app_email")
        app_url = self.__option_entity.get_value_by_key("app_url")
        user = self.__user_entity.get_one_by_email(email);

        parameters = {
            "app_name": app_name,
            "app_email": app_email,
            "app_url": app_url,
            "recipient_list": [email],
            "token": token,
            "subject": _("%s Password Reset") % (app_name),
            "template": "mails/reset_password.html",
            "fail_silently": False
        }

        task_result = forgot_password_email.delay(**parameters)

        if task_result.task_id != "":

            return self.__task_core.create_task({
                "name": "Password Reset",
                "uuid": task_result.task_id,
                "status": "pending",
                "executor": "app.tasks.forgot_password_email",
                "parameters": json.dumps(parameters),
                "result": '{}',
                "user_id": user.id
            }) != False

        return False