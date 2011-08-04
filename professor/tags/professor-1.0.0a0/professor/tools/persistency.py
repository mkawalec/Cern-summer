"""Wrapper module for whatever system Professor is using for data persistency,
i.e. storing from memory to disk and reading back in again. The current system
is the native Python 'pickle' operation."""

from professor.tools import log as logging

try:
    import cPickle as pickle
except ImportError:
    logging.debug("Module 'cPickle' not available, loading slower 'pickle' instead")
    import pickle
