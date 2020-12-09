
import logging
from functools import partialmethod
#---------------------------------------------------------------------------
# see config/settings.py LOGGING for configuration. /tmp/polls_debug.log
#---------------------------------------------------------------------------
# Customize and activate Logging.
# See config/settings.py for LOGGING dictConfig
# Logging Level ranges for for defining a custom handler:
# 50 = CRITICAL
# 40 = ERROR
# 30 = WARNING
# 20 = INFO
# 10 = DEBUG
#  0 = NOTSET
#
# using partialmethod we can define a funtion in Logger on the fly
#---------------------------------------------------------------------------

logging.DONE = 15
logging.addLevelName(logging.DONE, 'DONE')
logging.Logger.done = partialmethod(logging.Logger.log, logging.DONE)

# wrap some shell specific coloration around the name
logging.addLevelName(logging.DEBUG, "\033[1;35m%8s\033[0m" %
                     logging.getLevelName(logging.DEBUG))
logging.addLevelName(logging.DONE, "\033[32m%8s\033[0m" %
                     logging.getLevelName(logging.DONE))
logging.addLevelName(logging.INFO, "\033[36m%8s\033[0m" %
                     logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[33m%8s\033[0m" %
                     logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;31m%8s\033[0m" %
                     logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.CRITICAL, "\033[5;34;41m%8s\033[0m" %
                     logging.getLevelName(logging.CRITICAL))

# log INFO (and higher) TO CONSOLE by default unless setLevel otherwise
POLLS = logging.getLogger('polls')
# log INFO (and higher immutably) TO FILE and propagate to 'polls'
POLLS_FILE = logging.getLogger('polls.file')
# log DEBUG TO CONSOLE and INFO TO FILE (/tmp/polls_debug.log)
POLLS_BOTH = logging.getLogger('polls.both')
# log >= DEBUG to console, >= INFO to FILE (/tmp/polls_signals.log)
POLLS_BOTH_SIGNALS = logging.getLogger('polls.signals')
#logger.setLevel(logging.DEBUG)
