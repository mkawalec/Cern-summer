"""envelope.py\n

"""
import numpy, logging
from professor.tools.config import Config



class EnvelopeError(StandardError):
    pass

class Envelope:
    """ In this class all the methods are to be found needed for generating an
        envelope plot. For each envelope plot, representing Histos of a certain
        observable, a new Envelope object has to be created.

        use 'saveenvelopes.py' and 'makegallery.py' for userfriendly plotting
    """

    def __init__(self, td, observable=-1, plotwhat=(True, True, False),
            show=False, logscale=(False, False)):
        """ @param td: this is considered to be a TuningData object
            @param observable: this is to select one of the observables stored
            in the TuningData object to plot the envelope for.
        """
        self._use_latex=False
        self._td = td
        self._params = [i for i in self._td._params.values()[0].keys()]
        self._params.sort()
        if not observable==-1 and observable in self._td.getMCHistoNames():
            self._obs = observable
        elif type(observable)==int and int(observable) in xrange(len(
            self._td.getMCHistoNames())):
            self._obs = self._td.getMCHistoNames()[int(observable)]
        else:
            print 'Could not find observalbe', observable
            self._obs = self._td.getMCHistoNames()[0]
        self._allxranges = self.getAllXRanges()
        self._histdata = [run for run in self._td.getMCHistos(
            self._obs).values()]

    def getRange(self, bins):
        """ returns the minimum and maximum of the bins xranges of one histo
            @param bins: this is a list of Bin objects given by Histo.getBins()
        """
        temp = [bin.getXRange() for bin in bins]
        return temp, min(temp), max(temp)

    def getTotalXRange(self):
        """ returns the minimum and the maximum of the bins xranges of all
            histos found in the TuningData object to the Observable stored in
            Envelope._obs
        """
        mins = [self.getRange(histo.getBins())[1] for histo in self._td.getMCHistos(self._obs).values()]
        maxs = [self.getRange(histo.getBins())[2] for histo in self._td.getMCHistos(self._obs).values()]
        return min(mins), max(maxs)

    def getConfidencePatch(self, xlow, xhigh, cl, logy='no'):
        """ return a single patch that resemples a central CL
        """
        ## create an array that holds YVals as 1st column ans YErrs as 2nd column
        binvalues = []
        # iterate over all mcruns
        for histo in self._td.getMCHistos(self._obs).values():
            for bin in histo.getBins():
                if bin.getXRange() == (xlow, xhigh):
                    binvalues.append(bin.getYVal())

        # Sort binvalues (ascending)
        binvalues.sort()
        # Determine indices to cut, since we want a central CL band
        d = (100 - cl)/200
        startindex = int(numpy.round(d * len(binvalues)))
        stopindex =  int(numpy.round((1. - d) * len(binvalues)))

        vmin = binvalues[startindex]
        vmax = binvalues[stopindex]

        # values enclosing patch
        vpatch = [(xlow, vmax) , (xhigh, vmax), (xhigh, vmin) , (xlow, vmin)]

        if logy != 'no' and (vmax <=0 or vmin <=0):
            logging.debug("encountered bad bin at %f...%f, vmax=%f, vmin=%f, vpemax=%f, vpemax_low=%f"%(xlow, xhigh, vmax, vmin))
            return None
        else:
            return vpatch

    def getPatch(self, xlow, xhigh, logy='no'):
        """ return a single patch that encloses the values from all mc histos
            of a given observable, specified via self._obs, in a bin given by xlow
            and xhigh
        """
        ## create an array that holds YVals as 1st column ans YErrs as 2nd column
        # iterate over all mchistos
        vne = numpy.array([[(bin.getYVal(), abs(bin.getYErr()))
            for bin in histo.getBins() if bin.getXRange() == (xlow, xhigh) ]
            for histo in self._td.getMCHistos(self._obs).values()])
        vmax = self.getExtremalValueFromList(vne[:,0][:,0], 'max', logy)
        vmin = self.getExtremalValueFromList(vne[:,0][:,0], 'min', logy)
        vpemax = self.getExtremalValueFromList(
                vne[:,0][:,0] + vne[:,0][:,1], 'max', logy)
        vpemax_low = self.getExtremalValueFromList(
                vne[:,0][:,0] - vne[:,0][:,1], 'min', logy)
        # values enclosing patch
        vpatch = [(xlow, vmax) , (xhigh, vmax), (xhigh, vmin) , (xlow, vmin)]
        # upper values and errors enclosing patch
        uvpepatch = [(xlow, vpemax),(xhigh, vpemax),(xhigh, vmax),(xlow, vmax)]
        # lower values and errors enclosing patch
        lvpepatch = [(xlow, vmin),(xhigh, vmin),
                (xhigh, vpemax_low),(xlow, vpemax_low)]

        if logy != 'no' and (vmax <=0 or vmin <=0 or vpemax <=0 or vpemax_low <=0):
            logging.debug("encountered bad bin at %f...%f, vmax=%f, vmin=%f, vpemax=%f, vpemax_low=%f"%(xlow, xhigh, vmax, vmin, vpemax, vpemax_low))
            return None, None, None
        else:
            return vpatch, uvpepatch, lvpepatch

    def getExtremalValueFromList(self, thelist, mm='max', logy='no'):
        if logy == 'no':
            if mm == 'max':
                return max(thelist)
            elif mm == 'min':
                return min(thelist)
            else:
                print error("mm has tobe either 'min' or 'max")
        else:
            if mm == 'max':
                temp = [i for i in thelist if i > 0]
                if len(temp) > 0:
                    return max(temp)
                else:
                    return 0
            elif mm == 'min':
                temp = [i for i in thelist if i > 0]
                if len(temp) > 0:
                    return min(temp)
                else:
                    return 0
            else:
                print error("mm has tobe either 'min' or 'max")


    def getAllXRanges(self):
        """ assuming a valid td, we want an observables Xranges """
        runkey = self._td.getMCHistos(self._obs).keys()[0]
        return [bin.getXRange()
                for bin in self._td.getMCHistos(self._obs)[runkey]]

