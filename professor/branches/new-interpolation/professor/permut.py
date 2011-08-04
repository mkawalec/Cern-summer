"""permut.py

"""
from __future__ import generators
# from professor.competition import Competition as Comp
import random, numpy, time

def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc

def randomUniqueCombinations(items, n, howmany):
    """ this will create a list of lists of sorted listindices from which
    runcombinationlist can be constructed with the same result as
    xuniqueCombinations does, but a little less intelligent, but hopefully
    faster in higher dimensions
    """
    t0 = time.time()
    listindices = []
    # print 'len(items): ', len(items)
    for i in xrange(howmany):
        temp = []
        while len(temp) < n:
            # print 'len(temp): ', len(temp)
            rand = random.randint(0, len(items)-1)
            if not rand in temp:
                temp.append(rand)
                # print 'len(temp): after ', len(temp)
        temp.sort() # this is to ensure noun(unique) of combinations
        if not temp in listindices and Comp.goodRunnums([items[j] for j in temp]):
            listindices.append(temp)
    # print listindices
    # now building the runnumlist
    runnumlist = []
    for i in listindices:
        runnumlist.append([items[j] for j in i])
    print 'the whole shitta-shitta-bang-bang took %f seconds'%(time.time()-t0)
    return runnumlist

def shuffledCombinations(items, n, length=False):
    temp = [item for item in xuniqueCombinations(items,n)]
    random.shuffle(temp)
    return temp

