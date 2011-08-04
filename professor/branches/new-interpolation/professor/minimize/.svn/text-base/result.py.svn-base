"""results.py

"""

import numpy

# import parameter handling tools
import professor.tools.parameter
from professor.tools.elementtree import ET

# import our central config/logging module
from professor.tools.config import Config as _conf
_logger = _conf().getLogger('minimize')


class MinimizationResult(professor.tools.parameter.FixedSortedKeys):
    """minimzation result container.

    data stored (type)
    ==================
        - resulting chi2  (float)
        - parameter point (1D-numpy.array)
        - parameter errors* (2D-numpy.array)
          indices are:
            - 0: parameter index(=dimension),
            - 1: low/high error
          e.g. to get the lower unscaled error for param #2 you would use:

            >>> minresult.errunscaled[1,0]

          lower+upper errors are positive
        - used run numbers* (list of strings)
        - used obsevables*  (list of strings)
        - used selection functions* (list of strings or list of functions)
        - used start point method (string)

        *: this data is optional(defaults to None)

    array layout
    ============
    Parameters and errors are stored scaled and unscaled:
     - (par|err)scaled
     - (par|err)unscaled

    Instance creation
    =================
        - L{withScaler}: create an instance from scaled parameters and a
          L{Scaler} instance. This is used after a minimization is performed
          to turn the scaled parameters and errors to unscaled values. Used
          in L{BaseMinimizer.minimize}.
        - L{fromXMLElement}: load instance data from an cElementTree.Element
          instance. Used in L{ResultList.fromXML}.
        - __init__ itself should not be needed.
    """
    @classmethod
    def withScaler(cls, chi2, scaler, parscaled, errscaled=None, runs=None,
            obs=None, selfuncs=None, spmethod=None):
        """create a MinimizationResult from a L{Scaler} and an array of
        scaled parameters.
        """
        parunscaled = scaler.descale(parscaled)
        errunscaled = None
        if errscaled is not None:
            t = -1. * numpy.ones((scaler.dim(), 2))
            errunscaled = -1. * numpy.ones((scaler.dim(), 2))
            for i, errs in enumerate(errscaled):
                t[i] = numpy.array(errs)
            if (t < 0).any():
                raise ValueError("Negative errors make no sense!")
            tmin = scaler.getMinVals()
            tmax = scaler.getMaxVals()
            # dp_scaled = dp_unscaled/(p_max - p_min)
            errunscaled[:,0] = t[:,0]*(tmax-tmin)
            errunscaled[:,1] = t[:,1]*(tmax-tmin)
            errscaled = t

        return cls(chi2, scaler.getKeys(), parscaled, parunscaled, errscaled,
                   errunscaled, runs, obs, selfuncs, spmethod)

    @classmethod
    def fromXMLElement(cls, elem):
        """Create from data stored in given cElementTree.Element.

        @type elem: cElementTree.Element
        """
        chi = float(elem.find('chi2').get('value'))

        parnames = []
        parscaled = []
        parunscaled = []
        errscaled = []
        errunscaled = []
        for pel in sorted(elem.findall('parameter'),
                          key=lambda i: i.get('name')):
            parnames.append(pel.get('name'))
            parscaled.append(float(pel.get('par_scaled')))
            parunscaled.append(float(pel.get('par_unscaled')))
            try:
                errscaled.append([float(pel.get('err_low_scaled')),
                                  float(pel.get('err_high_scaled'))])
                errunscaled.append([float(pel.get('err_low_unscaled')),
                                  float(pel.get('err_high_unscaled'))])
            except TypeError:
                pass
        if len(errscaled) == 0:
            errscaled = errunscaled = None
        else:
            errscaled = numpy.array(errscaled)
            errunscaled = numpy.array(errunscaled)

        runs = []
        for runel in elem.findall('run_number'):
            runs.append(runel.get('number'))
        if len(runs) == 0:
            runs = None

        obs = []
        for obsel in elem.findall('observable'):
            obs.append(obsel.get('name'))
        if len(obs) == 0:
            obs = None

        selfuncs = []
        for sfel in elem.findall('selection_function'):
            selfuncs.append(sfel.get('name'))
        if len(selfuncs) == 0:
            selfuncs = None


        try:
            ndof = int(elem.find('ndof').get('value'))
        except AttributeError:
            ndof = None

        try:
            spmethod = elem.find('start_point_method').get('name')
        except AttributeError:
            spmethod = None

        return cls(chi, parnames, parscaled, parunscaled, errscaled,
                   errunscaled, runs, obs, selfuncs, spmethod, ndof)

    def __init__(self, chi2, parnames, parscaled, parunscaled, errscaled=None,
                 errunscaled=None, runs=None, obs=None, selfuncs=None,
                 spmethod=None, ndof=None):
        super(MinimizationResult, self).__init__(parnames)
        if parnames != self.getKeys():
            raise ValueError("argument parnames must be sorted!")
        self.chi2 = chi2
        self.parscaled = numpy.array(parscaled)
        self.parunscaled = numpy.array(parunscaled)
        if errscaled is None:
            self.errscaled = self.errunscaled = None
        else:
            self.errscaled = numpy.array(errscaled)
            self.errunscaled = numpy.array(errunscaled)
        self.runs = runs
        self.obs = obs
        self.selfuncs = selfuncs
        self.spmethod = spmethod
        self.ndof = ndof

        # sort stored lists
        # self.runs.sort()
        # self.obs.sort()
        # self.selfuncs.sort()

    def __str__(self):
        r = "%s:\n"%(self.__class__.__name__)
        r += "    chi2 : %s"%(self.chi2)
        if self.ndof is None:
            r += "\n"
        else:
            r += "  ndof : %i\n"%(self.ndof)
        if self.errscaled is None:
            r += "    param      unscaled  scaled\n"
            def newline(i, name):
                return "    %s   %.4e  %.4e\n"%(name, self.parunscaled[i],
                        self.parscaled[i])
        else:
            r += "    param      unscaled                      scaled\n"
            def newline(i, name):
                return "    %s  %.4e +%.3e-%.3e   %.4e +%.3e-%.3e\n"%(name,
                       self.parunscaled[i], self.errunscaled[i,1],
                       self.errunscaled[i,0], self.parscaled[i],
                       self.errscaled[i,1], self.errscaled[i,0])


        for i,name in enumerate(self.getKeys()):
            r += newline(i, name)
        return r[:-1]

    def asXMLElement(self):
        """Return cElementTree.Element instance containing all information."""
        ret = ET.Element("minimization_result")

        ET.SubElement(ret, "chi2", {'value' :"%f"%(self.chi2)})
        for i, name in enumerate(self.getKeys()):
            d = {'name' : name,
                 'par_scaled' : '%e'%(self.parscaled[i]),
                 'par_unscaled' : '%e'%(self.parunscaled[i])}
            if self.errscaled is not None:
                d['err_low_scaled'] = "%e"%(self.errscaled[i,0])
                d['err_high_scaled'] = "%e"%(self.errscaled[i,1])
                d['err_low_unscaled'] = "%e"%(self.errunscaled[i,0])
                d['err_high_unscaled'] = "%e"%(self.errunscaled[i,1])

            ET.SubElement(ret, "parameter", d)
        if self.ndof is not None:
            ET.SubElement(ret, "ndof", {'value' : "%i"%(self.ndof)})
        if self.runs:
            for rnum in self.runs:
                ET.SubElement(ret, "run_number", {'number' : rnum})
        if self.obs:
            for obs in self.obs:
                ET.SubElement(ret, "observable", {'name': obs})
        if self.selfuncs:
            for sf in self.selfuncs:
                ET.SubElement(ret, "selection_function", {'name':"%s"%(sf)})
        if self.spmethod:
            ET.SubElement(ret, "start_point_method", {'name': self.spmethod})
        return ret

class ResultList(list):
    """Container class for storing list of MinimizationResults.

    usage examples::
    creating empty instance:

        >>> results = ResultList()
    
    adding a MinimizationResult:
        >>> results.append(minresult)
    
    writing filled list to xml file:
        >>> results.write("path/to/results.xml")

    creating instance from xml file:
        >>> results = ResultList.fromXML("path/to/results.xml")
    """
    @classmethod
    def fromXML(cls, path):
        """Load a ResultList instance from XML file.

        @param path: the path to the file
        """
        tree = ET.parse(path)
        return cls([MinimizationResult.fromXMLElement(el)
                    for el in tree.findall("minimization_result")])

    def __init__(self, results=None):
        if results is None:
            super(ResultList, self).__init__()
        else:
            super(ResultList, self).__init__(results)
        self.chi2sigma = None
        self.chi2mean = None

        self.isValid()

    def write(self, path):
        """Write MinimizationResults as xml data to file located at path.

        The cElementTree.write output is not formatted nicely (just one
        single line), you can use ::

            $ sed -e 's/>/>\\n/g' < INPUT.xml > OUTPUT.xml

        to add new line characters after each tag.
        """
        root = ET.Element('minimization_result_list')
        for r in self:
            root.append(r.asXMLElement())
        et = ET.ElementTree(element=root)
        et.write(path)

    def getUnique(self, chi2tol=1.e-10, paramtol=None):
        """Returns a ResultList instance with only one result per choice of
        runs.

        Fails if results for the same choice of runs differ.

        @param chi2tol: absolute tolerance for chi2 values.
        @param paramtol: list/array with absolute parameter tolerance values.
            If C{None} 1e-10 for all parameters.
        @raises ValueError: if results for the same choice of runs differ.
        """
        # dictionary mapping run numbers to results
        uniq = {}
        if paramtol is None:
            paramtol = 1.e-10 * numpy.ones(self[0].dim())
        for res in self:
            key = ''.join(sorted(res.runs))
            if not uniq.has_key(key):
                uniq[key] = res
                continue
            cmpres = uniq[key]
            if abs(cmpres.chi2 - res.chi2) >= chi2tol:
                raise ValueError("chi^2 for runs '%s' differ to much:"
                                 " %r vs. %r"%(res.runs, res.chi2, cmpres.chi2))
            for i, ptol  in enumerate(paramtol):
                if abs(cmpres.parunscaled[i] - res.parunscaled[i]) >= ptol:
                    raise ValueError("parameter #%i(%s) for runs '%s' differ to"
                                     " much: %r vs. %r"%(i, res.getKeys()[i],
                                         res.runs, res.parunscaled[i],
                                         cmpres.parunscaled[i]))
        return ResultList(uniq.values())

    def getRunCounts(self):
        """Return a list with the numbers of runs used for the results."""
        ret = []
        for r in self:
            l = len(r.runs)
            if l not in ret:
                ret.append(l)
        ret.sort()
        return ret

    def isValid(self):
        """Perform some validity checks:
        - checks if all stored results have the same parameters

        @raises FixedSortedKeysError: if results have different parameter names.
        """
        if len(self) > 0:
            t = self[0]
            # this might raise a FixedSortedKeysError
            [t.goodPartner(r) for r in self]
        return True

    def getParamNames(self):
        return self[0].getKeys()


    # old code, probably not used
    def updateChi2Mean(self):
        """Recalculate chi2 mean and std. deviation."""
        if len(self) == 0:
            return
        self.chi2mean = numpy.mean(map(lambda r: r.chi2, self))
        t = 0.
        for r in self:
            t += (r.chi2 - self.chi2mean)**2
        self.chi2sigma = numpy.sqrt(t/float(len(self)))

    def selectByChi2(self, highfac=None, lowfac=None):
        """Return a ResultList with results matching chi^2 limits.

        L{updateChi2Mean} is called before selection is performed

        @param highfac: C{float} defining the upper chi^2 limit or C{None}
        @param lowfac: C{float} defining the lower chi^2 limit or C{None}
        """
        self.updateChi2Mean()
        workrs = ResultList()
        for r in self:
            if (highfac is not None
                and r.chi2 > (self.chi2mean + highfac*self.chi2sigma)):
                continue
            if (lowfac is not None
                and r.chi2 < (self.chi2mean - lowfac*self.chi2sigma)):
                continue
            workrs.append(r)
        if len(workrs) == 0:
            raise ValueError("No results to work with: perhaps to strict"
                             " values for *fac")
        return workrs

    def getParams(self, highfac=None, lowfac=None, as_dict=True):
        """Return parameter means and standard deviations as dict or arrays.

        Calculation is done with the unscaled parameter values.

        dict layout: {param name : (value, std. dev.)}

        This is faster than the implementation with numpy according to
        hotshot.
        """
        # list with the results to work with
        numruns = len(self)
        dim = self[0].dim()
        pnames = self[0].getKeys()
        d = {}
        for pi, pname in enumerate(pnames):
            d[pname] = [None, None]
            pmean = .0
            for r in self:
                pmean += r.parunscaled[pi]
            pmean /= float(numruns)
            d[pname][0] = pmean
            pdev = .0
            for r in self:
                pdev += (r.parunscaled[pi] - pmean)**2
            pdev /= numruns
            pdev = numpy.sqrt(pdev)
            d[pname][1] = pdev
        if as_dict:
            return d

        pval = numpy.zeros(dim)
        pdev = numpy.zeros(dim)
        for pi, pname in enumerate(pnames):
            pval[pi] = d[pname][0]
            pdev[pi] = d[pname][1]
        return pval, pdev

    def getParamsNumpy(self, highfac=None, lowfac=None, as_dict=True):
        """Return parameter means and standard deviations as dict or arrays.

        Calculation is done with the unscaled parameter values.

        dict layout: {param name : (value, std. dev.)}

        @param highfac: C{float} defining the upper chi^2 limit or C{None}
        @param highfac: C{float} defining the lower chi^2 limit or C{None}
        """
        self.updateChi2Mean()
        # list with the results to work with
        workrs = self.selectByChi2(highfac, lowfac)
        numruns = len(workrs)
        if numruns == 0:
            raise ValueError("No results to work with: perhaps to strict"
                             " values for *fac")
        dim = workrs[0].dim()
        print "dim =", dim
        # indices: [parameter, run]
        tparams = numpy.zeros((dim, numruns))
        for i, r in enumerate(workrs):
            tparams[:,i] = r.parunscaled
        parammeans = tparams.mean(axis=1)
        paramdevs = numpy.zeros(dim)
        for i in xrange(dim):
            paramdevs[i] = numpy.sqrt(
                            (numpy.sum((tparams[i,:] - parammeans[i])**2)
                             /float(numruns)))
        if not as_dict:
            return (parammeans, paramdevs)
        d = {}
        for i, pname in enumerate(workrs[0].getKeys()):
            d[pname] = (parammeans[i], paramdevs[i])
        return d
