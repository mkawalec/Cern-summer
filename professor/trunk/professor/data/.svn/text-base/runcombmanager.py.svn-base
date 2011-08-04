"""
A helper for reading combinations of available runs from a standardised
run-combination files.
"""

from professor.tools import log as logging
from professor.tools import io


class RunCombManager(object):
    """A simple helper for reading combinations of available runs from a
    standardised run-combination file format: one combination per line, where
    each combination is a whitespace-separated list of run IDs."""

    def __init__(self):
        self.runcombs = []


    @classmethod
    def mkFromFile(cls, path):
        new = cls()
        new.loadRunCombs(path)
        return new


    def loadRunCombs(self, rcfile):
        """Populate the runcombs collection from a filename or file object."""
        isfileobj = hasattr(rcfile, "readline")
        f = rcfile
        if not isfileobj:
            io.testReadFile(rcfile)
            f = open(rcfile, 'r')
        for rawline in f:
            ## Strip leading/trailing white spaces, e.g. newline
            line = rawline.strip()
            if not line or line.startswith('#'):
                continue
            comb = line.split()
            self.runcombs.append(comb)
        if not isfileobj:
            f.close()


    @property
    def firstruncomb(self):
        if not self.runcombs:
            return None
        return self.runcombs[0]


    def __str__(self):
        wstring = "Run combinations:\n"
        for r in self.runcombs:
            wstring += "%s\n" % r
        return wstring
