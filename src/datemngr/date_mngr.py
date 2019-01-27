from datetime import date, timedelta

class DateMngr():

    def __init__(self, start_date: date = date.today()):
        self.__today: date = start_date
        self.__tomorrow: date = self.__today + timedelta(days=1)

    def today(self) -> date:
        return self.__today

    def finish_day(self) -> None:
        self.__today += timedelta(days=1)

    def skip_days(self, amount: int) -> None:
        if type(amount) is not int:
            raise TypeError()
        if amount < 2:
            raise ValueError('Must skip at least 2 days')

        self.__today += timedelta(days=amount)
