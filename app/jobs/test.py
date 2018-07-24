"""
Test Job
"""

# local Django
from app.jobs.base import Base
from app.modules.util.helpers import Helpers


class Test(Base):


    def execute(self):
        self.__logger.debug(self._arguments["text"] if "text" in self._arguments else "Text not in arguments")
        return True