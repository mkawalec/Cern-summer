import os
from professor.tools.errors import IOTestFailed


class IOTests(object):
    """Helper with static methods to check for directories and access rights.

    If a test fails, an IOTestFailed exception is raised. Note: The
    exception is raised here and not in the functions where the checks are
    performed to save some typing, because usually such an IO error means
    that the script fails. If the script should continue, the exception can
    be 'excepted'.

    Implemented checks are:
    ReadDir - is directory and readable.
    WriteDir - is directory and readable.
    RWDir - is directory and readable and writable.
    ReadFile - is file-like and readable.
    WriteFile - is file-like and writable.
    """

    @staticmethod
    def ReadDir(path):
        if not os.path.isdir(path) or not os.access(path, os.R_OK|os.X_OK):
            raise IOTestFailed("Path not a directory or not readable:"
                               " %s" % (path))

    @staticmethod
    def WriteDir(path):
        if not os.path.isdir(path) or not os.access(path, os.W_OK|os.X_OK):
            raise IOTestFailed("Path not a directory or not writable:"
                               " %s" % (path))

    @staticmethod
    def RWDir(path):
        if not os.path.isdir(path) or not os.access(path, os.R_OK|os.W_OK|os.X_OK):
            raise IOTestFailed("Path not a directory or or not readable not writable:"
                               " %s" % (path))

    @staticmethod
    def ReadFile(path):
        """Check that 'path' is a file-like object and readable.

        Actually, it is tested that 'path' is not a directory. This allows
        to use this with pipes, links, etc. as well.
        """
        if os.path.isdir(path) or not os.access(path, os.R_OK):
            raise IOTestFailed("Path is not a file-like object or not readable:"
                               " %s" % (path))

    @staticmethod
    def WriteFile(path):
        """Check that 'path' is a file-like object and writable.

        Actually, it is tested that 'path' is not a directory. This allows
        to use this with pipes, links, etc. as well.
        """
        if os.path.isdir(path) or not os.access(path, os.W_OK):
            raise IOTestFailed("Path is not a file-like object or not writable:"
                               " %s" % (path))
