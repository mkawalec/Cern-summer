"""\
Module for commonly used functions for strings, e.g. removing/replacing
problematic characters for file name creation or LaTeX output.
"""

from decorators import deprecated

@deprecated("Is anybody using this function?")
def findInteger(string):
    """ this will return an integer contained as a substring in string,
        assuming that there is only one such substring in string
    """
    for i in xrange(len(string)):
        for j in xrange(len(string)):
            try:
                f = int(string[i:-j])
                # exit and return integer
                return f
            except ValueError:
                continue
    return None

@deprecated("Is anybody using this function?")
def sortParamNameList(plist):
    """ this will return a sorted version of plist. the sorting is done
        using substrings in the parameternames that can be converted to
        integers, otherwise, the returned list is sorted using sort()
    """
    temp = {}
    for i in plist:
        foundinteger = findInteger(i)
        if not foundinteger is None:
            temp[str(foundinteger)] = i
    if len(temp) == len(plist):
        return [temp[str(i)] for i in sorted(map(int, temp.keys()))]
    else:
        return sorted(plist)


def safeFilename(s, problems="/()", rep="_", striprep=True):
    """Replace characters that are problematic for file names.

    Parameters
    ----------
    problems : str, optional
        The problematic characters [default: "/()"]
    rep : str, optional
        Replace all characters in `problems` with `rep`.
    striprep : bool, optional
        Strip `rep` from the beginning and end of `s`.
    """
    for c in problems:
        s = s.replace(c, rep)
    if striprep:
        s = s.strip(rep)
    return s

def latex2mpl(s):
    """Make a latex string safe for matplotlib."""
    # map old => new
    replace = {"text" : "mathrm" }

    for old, new in replace.items():
        s = s.replace(old, new)
    return s

def latexEscape(s):
    """Escape special latex character sequences.

    E.g. "^" --> "\^{}"
    """
    escapes = {"^" : r"\^{}",
               "_" : r"\_"}

    for old, new in escapes.items():
        s = s.replace(old, new)
    return s
