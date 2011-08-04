"""Helper module with static methods to check for directories and access rights,
and some helpers for file and directory creation and handling, with suitable
checks and permissions.

The :func:`makeDir` function is a handy way to create a readable/writeable
directory without having to manually do all the edge-case checks that the native
:module:`os` module tools require.

The `is*` tests return true or false, i.e. are just packaged versions of standard
I/O functions from `os` and `os.path`. The `assert*` tests, by contrast, raise
an :class:`IOTestFailed` exception if the condition is not met.

The `isFile*` tests actually test that the path is not a directory. This allows
use with pipes, links, etc. as well as actual files.

.. note::
    The exception is raised here and not in the functions where the
    checks are performed to save some typing, because usually such an IO
    error means that the script fails. If the script should continue,
    the exception can be 'excepted'.

.. todo::
    Allow user to pass in an error-handling function as an argument,
    rather than see the exception?

.. todo::
    Remove test* aliases for I/O asserts.
"""

import os
from professor.tools.errors import IOTestFailed
from professor.tools import log as logging


def makeDir(path):
    """Make sure that directory exists, creating it if it doesn't already.

    Parameters
    ----------
    path : str
           The path to check/create
    """
    path = os.path.normpath(path)
    if not isDirW(path):
        os.makedirs(path)
        logging.debug("Created directory '%s'" % path)


#####################


def isDirR(path):
    """Check that 'path' is a dir-like object and readable."""
    path = os.path.normpath(path)
    return (os.path.isdir(path) and os.access(path, os.R_OK|os.X_OK))
def assertDirR(path):
    """Assert that 'path' is a dir-like object and readable."""
    if not isDirR(path):
        raise IOTestFailed("Path not a directory or not readable: %s" % path)

def isDirW(path):
    """Check that 'path' is a dir-like object and writeable."""
    path = os.path.normpath(path)
    return (os.path.isdir(path) and os.access(path, os.W_OK|os.X_OK))
def assertDirW(path):
    """Assert that 'path' is a dir-like object and writeable."""
    if not isDirW(path):
        raise IOTestFailed("Path not a directory or not writable: %s" % path)

def isDirRW(path):
    """Check that 'path' is a dir-like object and readable & writeable."""
    path = os.path.normpath(path)
    return (os.path.isdir(path) and os.access(path, os.R_OK|os.W_OK|os.X_OK))
def assertDirRW(path):
    """Assert that 'path' is a dir-like object and readable & writeable."""
    if not isDirRW(path):
        raise IOTestFailed("Path not a directory or not readable & writable: %s" % path)


def isFileR(path):
    """Check that 'path' is a file-like object and readable."""
    path = os.path.normpath(path)
    return (not os.path.isdir(path) and os.access(path, os.R_OK))
def assertFileR(path):
    """Assert that 'path' is a file-like object and readable."""
    if not isFileR(path):
        raise IOTestFailed("Path is not a file-like object or not readable: %s" % path)

def isFileW(path):
    """Check that 'path' is a file-like object and writeable."""
    path = os.path.normpath(path)
    return (not os.path.isdir(path) and os.access(path, os.W_OK))
def assertFileW(path):
    """Assert that 'path' is a file-like object and writeable."""
    if not isFileW(path):
        raise IOTestFailed("Path is not a file-like object or not writeable: %s" % path)

def isFileRW(path):
    """Check that 'path' is a file-like object and readable and writeable."""
    path = os.path.normpath(path)
    return (not os.path.isdir(path) and os.access(path, os.R_OK|os.W_OK))
def assertFileRW(path):
    """Assert that 'path' is a file-like object and readable and writeable."""
    if not isFileRW(path):
        raise IOTestFailed("Path is not a file-like object or not readable & writeable: %s" % path)


## Aliases
testReadDir = assertDirR
testWriteDir = assertDirW
testReadWriteDir = assertDirRW
testReadFile = assertFileR
testWriteFile = assertFileW
testReadWriteFile = assertFileRW
