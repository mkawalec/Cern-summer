#!/usr/bin/python
"""checkbins.py

"""
import numpy

def getBinRange(histo):
    return numpy.array([bin.getXRange() for bin in histo])

def getBinCenters(histo):
    return numpy.array([bin.getBinCenter() for bin in histo])

def getMCRanges(adict):
    return numpy.array([getBinRange(histo.getBins()) for histo in adict.values()])

def getAllRanges(td, obs):
    refrange = getBinRange(td.getRefHisto(obs))
    mcranges = getMCRanges(td.getMCHistos(obs))
    return refrange, mcranges

def allMCandRefHaveSameRanges(td, obs):
    ref, mc = getAllRanges(td, obs)
    for array in mc:
        if (array - ref).all() == numpy.zeros((len(ref), 2)).all():
            continue
        else:
            return False
    return True

def getPrintRange(td, obs, for_cmap=True):
    """ use this for colormaps """
    if allMCandRefHaveSameRanges(td, obs):
        if for_cmap:
            rng = [i[0] for i in getBinRange(td.getRefHisto(obs))]
            rng.append(getBinRange(td.getRefHisto(obs))[-1][1])
        else:
            rng = getBinCenters(td.getRefHisto(obs))
    else:
        raise StandardError('bins - uiuiuiiuiui!')
        # hier ne warning und standardding zurueck?
    return rng#numpy.array(rng)

#def getNiceXticks(td, obs):
#    rng = getPrintRange(td, obs)

