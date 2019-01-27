from datetime import date, timedelta

from src.bug.bug_builder import BugBuilder
from src.team.dev.dev import Dev
from src.team.dev.enums import Type as DevType
from src.datemngr.date_mngr import DateMngr

date_mngr = DateMngr()
bb = BugBuilder(date_mngr)
bug = bb.createBug()

print(bug)

dev = Dev(name='Pippo BE', type=DevType.BACKEND)
dev2 = Dev(name='Franco FS', type=DevType.FULLSTACK)

date_mngr.skip_days(2)

eta: date = date_mngr.today() + timedelta(weeks=2) + timedelta(days=(2-date_mngr.today().weekday()+7)%7)
bug.assignEta(eta)

date_mngr.finish_day()

bug.start(dev)

date_mngr.finish_day()

bug.finish()

bug.review(dev2)

date_mngr.skip_days(30)

bug.release()

print(bug)
