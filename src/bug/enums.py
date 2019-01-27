from enum import Enum

class Priority(Enum):
    LOW = 'glitch'
    AVERAGE = 'with workaround'
    HIGH = 'without workaround'
    CRITICAL = 'critical'

class Technology(Enum):
    LEGACY = 'legacy'
    HYDRA = 'hydra'
    BOTH = 'both'

class Type(Enum):
    FRONTEND = 'frontend'
    BACKEND = 'backend'
    BOTH = 'both'

class Status(Enum):
    NEW = 'new'
    ETA = 'eta'
    INPROGRESS = 'inprogress'
    CODEREVIEW = 'codereview'
    QA = 'qa'
    DONE = 'done'
