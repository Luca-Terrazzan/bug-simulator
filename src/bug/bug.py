from datetime import date, timedelta
from typing import Optional

from src.datemngr.date_mngr import DateMngr
from src.team.dev.dev import Dev
from src.team.dev.enums import Type as DevType

import src.bug.enums as enums


class Bug:

    def __init__(self, priority: enums.Priority, difficulty: float, technology: enums.Technology,
                 bug_type: enums.Type, date_mngr: DateMngr ) -> None:
        self.__validate_attributes__(
            priority=priority,
            difficulty=difficulty
        )

        self.__date_mngr = date_mngr

        self.__priority: enums.Priority = priority
        self.__difficulty: float = difficulty
        self.__technology: enums.Technology = technology
        self.__type: enums.Type = bug_type

        self.__assignee: Optional[Dev] = None
        self.__reviewer: Optional[Dev] = None
        self.__eta: Optional[date] = None
        self.__date_started: Optional[date] = None
        self.__date_finished: Optional[date] = None

        self.__status: enums.Status = enums.Status.NEW
        self.__created: date = self.__date_mngr.today()
        self.__overdue: bool = False

    @staticmethod
    def __validate_attributes__(**kwargs) -> None:
        if kwargs['difficulty'] < 0 or kwargs['difficulty'] > 1:
            raise ValueError('Difficulty must be within 0 and 1')

    # Properties
    @property
    def status(self) -> enums.Status:
        return self.__status

    @property
    def eta(self) -> date:
        return self.eta

    @property
    def created(self) -> date:
        return self.__created
    # more...

    def assign_eta(self, eta: date) -> None:
        if self.__status != enums.Status.NEW:
            raise PermissionError(
                'Cannot give ETA to a bug whose status is not NEW')
        if self.__eta:
            raise PermissionError('ETA already assigned')
        if eta <= self.__created:
            raise ValueError('ETA cannot be before bug creation')
        if eta <= self.__created + timedelta(weeks=2):
            raise ValueError('ETA must be at least 2 weeks')
        if eta.weekday() != 2:
            raise ValueError('ETA must be a wednesday')

        self.__status = enums.Status.ETA
        self.__eta = eta

    def start(self, dev: Dev) -> None:
        if self.__status != enums.Status.ETA:
            raise PermissionError('Cannot start a bug whose status is not ETA')

        self.__status = enums.Status.INPROGRESS
        self.__assignee = dev
        self.__date_started = self.__date_mngr.today()

    def finish(self) -> None:
        if self.__status != enums.Status.INPROGRESS:
            raise PermissionError(
                'Cannot finish a bug whose status is not IN PROGRESS')

        self.__status = enums.Status.CODEREVIEW

    def review(self, reviewer: Dev) -> None:
        if self.__status != enums.Status.CODEREVIEW:
            raise PermissionError(
                'Cannot review a bug whose status is not CODE REVIEW')
        if reviewer == self.__assignee:
            raise ValueError('Cannot self review')
        if reviewer.type != DevType.FULLSTACK and reviewer.type != self.__type:
            raise TypeError(
                f'Only a fullstack or a {self.__type} developer can review this')

        self.__status = enums.Status.QA
        self.__reviewer = reviewer

    def release(self) -> None:
        if self.__status != enums.Status.QA:
            raise PermissionError(
                'Cannot release a bug whose status is not QA')

        self.__status = enums.Status.DONE
        self.__date_finished = self.__date_mngr.today()

        if self.__eta is None:
            raise AttributeError('A bug without ETA cannot be completed')

        self.__overdue = self.__date_finished > self.__eta  # type: ignore

    def __str__(self):
        return f"""Status: {self.__status}
        ETA: {self.__eta}
        Overdue: {self.__overdue}
        Assignee: {self.__assignee}
"""
