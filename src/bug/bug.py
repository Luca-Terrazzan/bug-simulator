from typing import Optional
from datetime import date, timedelta

from .enums import *

from src.team.dev.dev import Dev
from src.team.dev.enums import Type as DevType

from src.datemngr.date_mngr import DateMngr

""" Represent a bug and its properties
"""
class Bug():

    def __init__(
        self,
        priority: Priority,
        difficulty: float,
        technology: Technology,
        type: Type,
        date_mngr: DateMngr
    ) -> None:
        self.__validate_attributes__(
            priority=priority,
            difficulty=difficulty
        )

        self.__date_mngr = date_mngr

        self.__priority: Priority = priority
        self.__difficulty: float = difficulty
        self.__technology: Technology = technology
        self.__type: Type = type

        self.__assignee: Optional[Dev] = None
        self.__reviewer: Optional[Dev] = None
        self.__eta: Optional[date] = None
        self.__dateStarted: Optional[date] = None
        self.__dateFinished: Optional[date] = None

        self.__status: Status = Status.NEW
        self.__created: date = self.__date_mngr.today()
        self.__overdue: bool = False

    def __validate_attributes__(self, **kwargs) -> None:
        if kwargs['difficulty'] < 0 or kwargs['difficulty'] > 1:
            raise ValueError('Difficulty must be within 0 and 1')

    # Properties
    @property
    def status(self) -> Status:
        return self.__status
    @property
    def eta(self) -> date:
        return self.eta
    @property
    def created(self) -> date:
        return self.__created
    # more...

    def assignEta(self, eta: date) -> None:
        if self.__status != Status.NEW:
            raise PermissionError('Cannot give ETA to a bug whose status is not NEW')
        if self.__eta:
            raise PermissionError('ETA already assigned')
        if eta <= self.__created:
            raise ValueError('ETA cannot be before bug creation')
        if eta <= self.__created + timedelta(weeks=2):
            raise ValueError('ETA must be at least 2 weeks')
        if eta.weekday() != 2:
            raise ValueError('ETA must be a wednesday')

        self.__status = Status.ETA
        self.__eta = eta

    def start(self, dev: Dev) -> None:
        if self.__status != Status.ETA:
            raise PermissionError('Cannot start a bug whose status is not ETA')

        self.__status = Status.INPROGRESS
        self.__assignee = dev
        self.__dateStarted = self.__date_mngr.today()

    def finish(self) -> None:
        if self.__status != Status.INPROGRESS:
            raise PermissionError('Cannot finish a bug whose status is not IN PROGRESS')

        self.__status = Status.CODEREVIEW

    def review(self, reviewer: Dev) -> None:
        if self.__status != Status.CODEREVIEW:
            raise PermissionError('Cannot review a bug whose status is not CODE REVIEW')
        if reviewer == self.__assignee:
            raise ValueError('Cannot self review')
        if reviewer.type != DevType.FULLSTACK and reviewer.type != self.__type:
            raise TypeError(f'Only a fullstack or a {self.__type} developer can review this')

        self.__status = Status.QA
        self.__reviewer = reviewer

    def release(self) -> None:
        if self.__status != Status.QA:
            raise PermissionError('Cannot release a bug whose status is not QA')

        self.__status = Status.DONE
        self.__dateFinished = self.__date_mngr.today()

        if self.__eta is None:
            raise AttributeError('A bug without ETA cannot be completed')

        self.__overdue = self.__dateFinished > self.__eta # type: ignore

    def __str__(self):
        return f"""Status: {self.__status}
        ETA: {self.__eta}
        Overdue: {self.__overdue}
        Assignee: {self.__assignee}
"""
