"""
A simple wrapper around Python's logging module. It's to share logging
initialisation between the prof-... scripts.
"""

from logging import *

# Simon Plaetzer reported that importing all from logging is not working on
# openSuse 11.1/11.2 . The following is a heuristic: if basicConfig is
# available we assume that the above import worked.
try:
    basicConfig(level=INFO, format = "%(levelname)s %(message)s")
except NameError:
    from logging import basicConfig
    from logging import INFO, WARNING, ERROR, CRITICAL
    from logging import log, warn, warning, debug, info, error
    from logging import Formatter
    from logging import getLogger

    basicConfig(level=INFO, format = "%(levelname)s %(message)s")


## Extra-low logging level
TRACE = 5


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
    if hasattr(values, "DEBUG"):
        warn("Use of deprecated log level switch in command line. Fix the"
             " called script to use addLoggingCLOptions, please")
        if values.DEBUG:
            values.LOGLEVEL = DEBUG

    if hasattr(values, "LOGLEVEL"):
        logger = getLogger()
        logger.setLevel(values.LOGLEVEL)
        ## Set a more informative logging format.
        if values.LOGLEVEL < INFO:
            fmt =  Formatter("%(module)s: %(levelname)s %(message)s")
            for hndl in logger.handlers:
                hndl.setFormatter(fmt)

    ## This for old scripts that don't use addLoggingCLOptions
    else:
        error(str(values))
        error(str(dir(values)))
        raise ValueError("Values instance has no 'DEBUG' or 'LOGLEVEL' attribute!")
