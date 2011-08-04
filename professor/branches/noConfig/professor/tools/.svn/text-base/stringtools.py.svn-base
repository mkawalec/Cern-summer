""" stringtools.py
    some string handling tools needed for tuned plots
"""

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

