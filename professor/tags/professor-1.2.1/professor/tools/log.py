"""
A simple wrapper around Python's logging module. It's to share logging
initialisation between the prof-... scripts.
"""

## Default log message format
MSGFORMAT = "%(module)s: %(levelname)s %(message)s"

## Import logging module contents, with a workaround for OpenSuse 11.1/11.2
import sys
from logging import *
try:
    basicConfig(level=INFO, format=MSGFORMAT)
except NameError:
    from logging import basicConfig
    from logging import INFO, WARNING, ERROR, CRITICAL
    from logging import log, warn, warning, debug, info, error
    from logging import Formatter
    from logging import getLogger
    basicConfig(level=INFO, format=MSGFORMAT)

## Extra-low logging level
TRACE = 5


## Add coloured logging facility
## The background is set with 40 plus the number of the color, and the foreground with 30
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
COLORS = {
    'DEBUG': CYAN,
    'INFO': BLACK,
    'WARNING': YELLOW,
    'CRITICAL': MAGENTA,
    'ERROR': RED
    }

class ColoredFormatter(Formatter):
    def __init__(self, msg, use_color=True):
        Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        message = Formatter.format(self, record)
        if self.use_color and sys.stderr.isatty() and levelname in COLORS:
            message = COLOR_SEQ % (30 + COLORS[levelname]) + message + RESET_SEQ
        return message

## Apply colourised formatting
FORMATTER = Formatter(MSGFORMAT)
try:
    MSGFORMAT = "%(message)s"
    FORMATTER = ColoredFormatter(MSGFORMAT)
except:
    debug("Failed to configure coloured logging formatter")


def addLoggingCLOptions(parser, logoswitch=False):
    """
    Add logging control options to OptionParser parser.
    """
    from optparse import OptionGroup
    g = OptionGroup(parser, "Logging")
    g.add_option("-q", "--quiet", dest="LOGLEVEL", default=INFO, action = "store_const", const=WARNING,
                 help="Turn logging off except for warnings and errors")
    g.add_option("-v", "--verbose", dest="LOGLEVEL", default=INFO, action = "store_const", const=DEBUG,
                 help="Turn on verbose logging")
    g.add_option("--debug", dest="LOGLEVEL", default=INFO, action = "store_const", const=TRACE,
                 help="Turn on *really* verbose debug logging")
    if logoswitch:
        g.add_option("-l", "--no-logo", dest="SHOW_LOGO", default=True, action = "store_false",
                     help="Don't show the amusing logos of professors")
    parser.add_option_group(g)


def trace(msg, *args, **kwargs):
    return log(TRACE, msg, args, kwargs)


def setPriority(values):
    """Set the priority according to the values in options.

    The OptionParser that built the values must have one of the following
    option names:
    * a 'DEBUG' option, that is True or False (deprecated)
    * a 'LOGLEVEL' option, that evaluates to a log level constant of the
      logging module.

    Parameters
    ----------
        values : optparse.Values
    """
    global FORMATTER
    if hasattr(values, "DEBUG"):
        warn("Use of deprecated log level switch in command line. Fix the"
             " called script to use addLoggingCLOptions, please")
        if values.DEBUG:
            values.LOGLEVEL = DEBUG

    if hasattr(values, "LOGLEVEL"):
        logger = getLogger()
        logger.setLevel(values.LOGLEVEL)
        ## Set a more informative logging format for verbose mode
        if values.LOGLEVEL < INFO:
            MSGFORMAT = "%(module)s: %(message)s"
            FORMATTER = ColoredFormatter(MSGFORMAT)
        for hndl in logger.handlers:
            hndl.setFormatter(FORMATTER)

    ## This for old scripts that don't use addLoggingCLOptions
    else:
        error(str(values))
        error(str(dir(values)))
        raise ValueError("Values instance has no 'DEBUG' or 'LOGLEVEL' attribute!")
