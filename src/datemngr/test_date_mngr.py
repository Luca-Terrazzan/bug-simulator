import unittest
from datetime import date, timedelta

from .date_mngr import DateMngr


class TestDateManager(unittest.TestCase):

    def test_date_manager_creation(self):
        date_mngr = DateMngr()
        self.assertIsInstance(date_mngr, DateMngr)

    def test_day_flow(self):
        start_date = date(year=2019, month=1, day=1)

        # Create a date manager starting on 2019.1.1
        date_mngr = DateMngr(start_date)

        # Test that start date has set
        self.assertEqual(start_date, date_mngr.today())

        # Test that passing a day works
        date_mngr.finish_day()
        tomorrow = start_date + timedelta(days=1)
        self.assertEqual(tomorrow, date_mngr.today(), 'Wrong day passed')

    def test_days_skip(self):
        start_date = date(year=2019, month=1, day=1)

        # Create a date manager starting on 2019.1.1
        date_mngr = DateMngr(start_date)

        # Test that start date has set
        self.assertEqual(start_date, date_mngr.today())

        # Test that skipping days works
        date_mngr.skip_days(7)
        next_week = start_date + timedelta(days=7)
        self.assertEqual(next_week, date_mngr.today(), 'Wrong days passed')


if __name__ == '__main__':
    unittest.main()
