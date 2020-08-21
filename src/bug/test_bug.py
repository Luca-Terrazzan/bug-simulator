import unittest
from datetime import date
from unittest.mock import patch

import src.bug.enums as enums
from .bug import Bug


class TestBug(unittest.TestCase):

    def test_bug_creation(self):
        with patch('src.datemngr.date_mngr.DateMngr') as dateMngrMock:
            Bug(enums.Priority.LOW, 0.5, enums.Technology.LEGACY,
                enums.Type.BACKEND, dateMngrMock)
            self.assertTrue(dateMngrMock.today.assert_called_once,
                            'Creation date not set')

    def test_bug_invalid_creation(self):
        invalid_complexity = -1
        with patch('src.datemngr.date_mngr.DateMngr') as dateMngrMock:
            try:
                Bug(enums.Priority.LOW, invalid_complexity,
                    enums.Technology.LEGACY, enums.Type.BACKEND, dateMngrMock)
            except ValueError:
                pass
            else:
                self.fail()
            self.assertEqual(dateMngrMock.today.call_count,
                             0, 'Dependency called')

    def test_bug_lifecycle(self):
        with patch('src.datemngr.date_mngr.DateMngr') as DateMngrMock:
            datemngrmock = DateMngrMock()
            datemngrmock.today.return_value = date(year=2019, month=1, day=1)

        bug = Bug(enums.Priority.LOW, 0.5, enums.Technology.LEGACY,
                  enums.Type.BACKEND, datemngrmock)
        self.assertTrue(datemngrmock.today.assert_called_once,
                        'Creation date not set')

        # Assign the bug an ETA
        eta = date(year=2019, month=1, day=16)
        bug.assign_eta(eta)
        self.assertEqual(bug.status, enums.Status.ETA)

        # Put the bug in progress by a dev
        with patch('src.team.dev.dev.Dev') as DevMock:
            dev = DevMock()
        bug.start(dev)
        self.assertEqual(bug.status, enums.Status.INPROGRESS)

        # Dev completes fix
        bug.finish()
        self.assertEqual(bug.status, enums.Status.CODEREVIEW)

        # Another dev performs the code review
        with patch('src.team.dev.dev.Dev') as DevMock:
            reviewer = DevMock()
            reviewer.type = enums.Type.BACKEND
        bug.review(reviewer)
        self.assertEqual(bug.status, enums.Status.QA)

        # QC performs testing
        bug.release()
        self.assertEqual(bug.status, enums.Status.DONE)


if __name__ == '__main__':
    unittest.main()
