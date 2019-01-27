import unittest
from unittest.mock import patch

from .bug import Bug
from .enums import *

class TestBug(unittest.TestCase):

    def test_bug_creation(self):
        with patch('src.datemngr.date_mngr.DateMngr') as dateMngrMock:
            bug = Bug(Priority.LOW, 0.5, Technology.LEGACY, Type.BACKEND, dateMngrMock)
            self.assertTrue(dateMngrMock.today.assert_called_once, 'Creation date not set')

    def test_bug_invalid_creation(self):
        invalid_complexity = -1
        with patch('src.datemngr.date_mngr.DateMngr') as dateMngrMock:
            try:
                bug = Bug(Priority.LOW, invalid_complexity, Technology.LEGACY, Type.BACKEND, dateMngrMock)
            except ValueError:
                self.assertTrue(True)
            else:
                self.assertTrue(False)
            self.assertEquals(dateMngrMock.today.call_count, 0, 'Dependency called')

if __name__ == '__main__':
    unittest.main()