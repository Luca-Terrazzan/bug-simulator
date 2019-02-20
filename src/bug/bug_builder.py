from .bug import Bug
from .enums import *

from src.datemngr.date_mngr import DateMngr


class BugBuilder:

    def __init__(self, date_mngr: DateMngr):
        self.__date_mngr = date_mngr

    def create_bug(self) -> Bug:
        return Bug(Priority.LOW, 0.5, Technology.LEGACY, Type.BACKEND, self.__date_mngr)
