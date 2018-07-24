"""
Forgot Password Module
"""

# standard library
from datetime import timedelta

# Django
from django.utils import timezone

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.user_entity import User_Entity
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.job_entity import Job_Entity
from app.modules.entity.reset_request_entity import Reset_Request_Entity


class Forgot_Password():

    __reset_request_entity = None
    __option_entity = None
    __user_entity = None
    __job_entity = None
    __helpers = None

    __reset_expire_option = 24
    __messages_count_option = 5


    def __init__(self):
        self.__reset_request_entity = Reset_Request_Entity()
        self.__option_entity = Option_Entity()
        self.__helpers = Helpers()
        self.__user_entity = User_Entity()
        self.__job_entity = Job_Entity()

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
        return self.__job_entity.insert_one({
            "name": "reset_password_msg_for_%s" % (email),
            "executor": "forgot_password_email.Forgot_Password_Email",
            "parameters": {"recipient_list": [email], "token": token},
            "interval": {"type": Job_Entity.ONCE}
        })