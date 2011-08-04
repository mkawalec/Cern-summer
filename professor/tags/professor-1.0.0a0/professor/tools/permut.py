"""permut.py

"""
from __future__ import generators
import random


def xuniqueCombinations(items, n):
    """Recursively construct all combinations, without
    explicitly holding them all in memory. Deterministic,
    highly-correlated ordering of results."""
    if n == 0:
        yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]] + cc


def shuffledCombinations(items, n, length=False):
    temp = [item for item in xuniqueCombinations(items,n)]
    random.shuffle(temp)
    return temp


def nCr(n, r):
    from scipy.misc import comb
    rtn = comb(n, r)
    return rtn


def xrandomUniqueCombinations(items, nchoose, howmany=None):
    """Iterate through a list of unique sets of nchoose elements selected from items."""
    seencombs = []
    maxnum = nCr(len(items), nchoose)
    if howmany is None or howmany > maxnum:
        howmany = maxnum
    while len(seencombs) < howmany:
        temp = random.sample(items, nchoose)
        temp.sort()
        if not sorted(temp) in seencombs:
            seencombs.append(temp)
            yield temp


def randomUniqueCombinations(items, nchoose, howmany=None):
    """Create a list of unique sets of nchoose elements selected from items."""
    rtn = []
    for i in xrandomUniqueCombinations(items, nchoose, howmany):
        rtn.append(i)
    return rtn


def getIntersection(*lists):
    """ return the intersection of an arbitrary number of lists """
    if len(lists) == 1:
        return lists[0]
    else:
        sets = map(set, lists)
        temp = set.intersection(sets[0], sets[1])
        for i in sets[1:]:
            temp = set.intersection(set(temp), i)
        return list(temp)
