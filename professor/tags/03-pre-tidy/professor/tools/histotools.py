#!/usr/bin/python
"""histotools.py

"""
## tools for histos

def getBinsWithNotMoreThanErrorR(histo, R):
    """ return a list of bin-numbers that match relative error threshold
    criterion
    R is meant to be in percent
    """
    if R < 0:
        raise StandardError('relative error cannot be negative!')
    else:
        return [i for i, bin in enumerate(histo) if bin.getYVal() !=0 and
                bin.getYErr()/bin.getYVal() <= R/100.]

## these take tuningdata-objects as argument

def compareAllMC(td, use_obs, R):
    """ return a list of bin-numbers that match threshold criterion in all
        MCHistos
        @param use_obs: the observable
        @param R: threshold, only Bins whose content is >= R are accepted
    """
    allbins = numpy.arange(len(td.getRefHisto(use_obs)))
    alllists = [getBinsWithNotMoreThanErrorR(
        histo, R) for histo in td.getMCHistos(use_obs).values()]
    return [item for item in allbins if itemIsInAllLists(
        item, alllists)]

def getPlotRange(td, obs, for_cmap=True):
    """ return x-values for plotting
        use this for colormaps - workaround for the pylab.colormap
        bin-definition
        assuming TuningData.isValid() was called before
    """
    if for_cmap:
        rng = [i[0] for i in td.getBinRanges(td.getRefHisto(obs))]
        rng.append(td.getBinRanges(td.getRefHisto(obs))[-1][1])
    else:
        rng = [bin.getBinCenter() for bin in td.getRefHisto(obs)]
    return rng

## helper functions

def itemIsInAllLists(item, lists):
    """ check whether a certain item is contained in all of several
        lists
        @param item: the item to check for
        @param lists: a list of lists
    """
    for i in lists:
        if item in i:
            continue
        else:
            return False
    return True
