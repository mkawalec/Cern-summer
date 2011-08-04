"""
A brain-dead simple wrapper around Python's logging module. It's to share
logging initialisation between the prof-... scripts.
"""

from logging import *

basicConfig(level=INFO, format = "%(module)s: %(levelname)s %(message)s")


## Extra-low logging level
TRACE = 5


def trace(msg, *args, **kwargs):
    return log(TRACE, msg, args, kwargs)


def setPriority(values):
    """Set the priority according to the values in options.

    The OptionParser that built the values must have one of the following
    option names:
    * a 'debug' option, that is True or False.
    * a 'loglevel' option, that evaluates to a log level constant of the
      logging module.

    Parameters
    ----------
        values : optparse.Values
    """
    if hasattr(values, "debug"):
        if values.debug:
            getLogger().setLevel(DEBUG)
    elif hasattr(values, "loglevel"):
        getLogger().setLevel(values.loglevel)
    else:
        error(str(values))
        error(str(dir(values)))
        raise ValueError("Given Values instance misses 'debug' or 'loglevel'"
                         " attribute!")
