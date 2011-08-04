#!/usr/bin/python
# vim:fileencoding=utf-8
"""permut.py

"""
from __future__ import generators

def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc
