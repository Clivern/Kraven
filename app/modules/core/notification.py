"""
Task Module
"""

# standard library
import json
from datetime import timedelta

# local Django
from app.modules.util.helpers import Helpers
from app.modules.util.humanize import Humanize
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.notification_entity import Notification_Entity
from django.utils.translation import gettext as _


class Notification():

    __notification_entity = Notification_Entity()
    __option_entity = Option_Entity()
    __helpers = Helpers()
    __humanize = Humanize()
    __app_name = None
    __logger = None


    def __init__(self):
        self.__logger = self.__helpers.get_logger(__name__)
        option = self.__option_entity.get_one_by_key("app_name")
        self.__app_name = option.value if option != False else ""


    def create_notification(self, data):
        return self.__notification_entity.insert_one(data)


    def user_latest_notifications(self, user_id, count=5):

        notifications = self.__notification_entity.get_many_by_user(user_id, "created_at", False, count)

        result = {
            "notifications": [],
            "status": "read"
        }

        for notification in notifications:
            if not notification.delivered:
                result["status"] = "unread"

            result["notifications"].append({
                "id": notification.id,
                "type": notification.type,
                "highlight": self.__humanize_highlight(notification.highlight, notification.host),
                "description": notification.notification,
                "url": notification.url,
                "delivered": notification.delivered,
                "time": self.__humanize_updated_at(notification.created_at)
            })

        return result


    def update_task_notification(self, task_id, type, delivered=False):
        return self.__notification_entity.update_one_by_task_id(task_id, {
            "type": type,
            "delivered": delivered
        })


    def mark_notification(self, user_id, notification_id):
        if self.__notification_entity.get_one_by_id_and_user(notification_id, user_id):
            return self.__notification_entity.update_one_by_id(notification_id, {"delivered": True})

        return False


    def __humanize_highlight(self, highlight, host):
        if host:
            return host.name

        if highlight == "$APP_NAME":
            return self.__app_name

        return highlight


    def __humanize_updated_at(self, created_at):
        return self.__humanize.datetime(created_at)
