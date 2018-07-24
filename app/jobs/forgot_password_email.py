"""
Forgot Password Job
"""

# Django
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.template.loader import render_to_string

# local Django
from app.jobs.base import Base


class Forgot_Password_Email(Base):

    __data = {}
    __subject = _("%s Password Reset")
    __template = "mails/reset_password.html"


    def execute(self):

        if "app_name" not in self.__arguments or "app_email" not in self.__arguments or "app_url" not in self.__arguments:
            self.__logger.error("App name or app email or app url is missing!")
            return False

        if "recipient_list" not in self.__arguments or len(self.__arguments["recipient_list"]) < 1:
            self.__logger.error("Recipient List is Missing!")
            return False

        if "token" not in self.__arguments or self.__arguments["token"].strip() == "":
            self.__logger.error("Reset Token is Missing!")
            return False

        if "fail_silently" not in self.__arguments:
            self.__arguments["fail_silently"] = False

        self.__subject = self.__subject % (self.__arguments["app_name"])

        self.__data = {
            "app_name": self.__arguments["app_name"],
            "email_title": self.__subject,
            "app_url": self.__arguments["app_url"],
            "token": self.__arguments["token"]
        }

        try:
            send_mail(
                self.__subject,
                "",
                self.__arguments["app_email"],
                self.__arguments["recipient_list"],
                fail_silently=self.__arguments["fail_silently"],
                html_message=self.__get_message()
            )
            return True
        except Exception as e:
            self.__logger.error("Error while sending email: %s" % (e))
            return False


    def _get_message(self):
         return render_to_string(self.__template, self.__data)