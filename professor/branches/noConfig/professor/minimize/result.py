"""results.py

"""

import os
import re
import logging

import numpy

# import parameter handling tools
import professor.tools.parameter
from professor.tools.elementtree import ET

# some statistical formulas
from professor.tools import formulas

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
        - covariance matrix* (dictionary)
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
            obs=None, selfuncs=None, spmethod=None, covariance=None):
        """create a MinimizationResult from a L{Scaler} and an array of
        scaled parameters.
        """

        logging.debug("Creating MinimizationResult:")
        logging.debug("  scaler: %s"%(scaler))
        logging.debug("  scaled values: %s"%(parscaled))
        parunscaled = scaler.descale(parscaled)
        logging.debug("  unscaled values: %s"%(parunscaled))
        logging.debug("  covariance matrix: %s", str(covariance))
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
                   errunscaled, runs, obs, selfuncs, spmethod, covariance=covariance)

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
        for pel in sorted(elem.findall('parameter'), key=lambda i: i.get('name')):
            parnames.append(pel.get('name'))
            parscaled.append(float(pel.get('par_scaled')))
            parunscaled.append(float(pel.get('par_unscaled')))

            ## Handle scaled errors
            try:
                errscaled.append([float(pel.get('err_low_scaled')), float(pel.get('err_high_scaled'))])
            except TypeError:
                errscaled.append(None)

            ## Handle unscaled errors
            try:
                errunscaled.append([float(pel.get('err_low_unscaled')), float(pel.get('err_high_unscaled'))])
            except TypeError:
                errscaled.append(None)

        ## Convert error containers to numpy arrays (why?)
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

        try:
            temp = elem.find('covariance_matrix')
            cov = {}
            for k, v in temp.items():
                cov[(k.split('_')[0], k.split('_')[1])] = float(v)
            covariance = cov
        except AttributeError:
            covariance = None

        return cls(chi, parnames, parscaled, parunscaled, errscaled,
                   errunscaled, runs, obs, selfuncs, spmethod, ndof, covariance=covariance)


    def __init__(self, chi2, parnames, parscaled, parunscaled, errscaled=None,
                 errunscaled=None, runs=None, obs=None, selfuncs=None,
                 spmethod=None, ndof=None, covariance=None):
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
        self.covariance = covariance

        # sort stored lists
        def sortNotNone(l):
            if l is not None:
                l.sort()
        sortNotNone(self.runs)
        sortNotNone(self.obs)


    def __str__(self):
        r = "%s:\n" % self.__class__.__name__
        r += "chi2: %s" % self.chi2
        if self.ndof:
            r += "Ndf: %i    chi2/Ndf: %e" % (self.ndof, self.chi2/self.ndof)
        r += "\n"

        if self.errscaled is None:
            r += "param".ljust(30) + " unscaled" + 26*" " + "scaled\n"
            def newline(i, name):
                return "%s %.4e  %.4e\n" % (
                    name.ljust(30), 
                    self.parunscaled[i],
                    self.parscaled[i] )
        else:
            r += "param".ljust(30) + " unscaled" + 26*" " + "scaled\n"
            def newline(i, name):
                return "%s %.4e +%.3e-%.3e   %.4e +%.3e-%.3e\n" % (
                        name.ljust(30),
                        self.parunscaled[i], self.errunscaled[i,1],
                        self.errunscaled[i,0], self.parscaled[i],
                        self.errscaled[i,1], self.errscaled[i,0])

        for i,name in enumerate(self.getKeys()):
            r += newline(i, name)
        return r[:-1]


    def getCovMatrix(self):
        """ return the covariance matrix as a numpy array """
        # initialize empty matrix (array) first
        V = numpy.diag(numpy.zeros(self.dim()))
        # integerpattern
        intpat = re.compile(r'[0-9]+')
        # little helper function to turn 'MP01' into 1 etc.
        def getInt(string):
            return int(intpat.findall(string)[0])
        # fill yet empty covariance matrix
        for k, v in self.covariance.iteritems():
            V[getInt(k[0])][getInt(k[1])] = v
        return V


    def asXMLElement(self):
        """Return cElementTree.Element instance containing all information."""
        ret = ET.Element("minimization_result")

        ET.SubElement(ret, "chi2", {'value' :"%f"%(self.chi2)})
        for i, name in enumerate(self.getKeys()):
            d = { 'name' : name,
                  'par_scaled' : '%e' % self.parscaled[i],
                  'par_unscaled' : '%e' % self.parunscaled[i] }
            if self.errscaled is not None:
                try:
                    d['err_low_scaled'] = "%e" % self.errscaled[i,0]
                    d['err_high_scaled'] = "%e" % self.errscaled[i,1]
                except IndexError:
                    pass

                try:
                    d['err_low_unscaled'] = "%e" % self.errunscaled[i,0]
                    d['err_high_unscaled'] = "%e" % self.errunscaled[i,1]
                except IndexError:
                    pass

            ET.SubElement(ret, "parameter", d)
        if self.ndof is not None:
            ET.SubElement(ret, "ndof", {'value' : "%i"%(self.ndof)})
        if self.covariance is not None:
            temp = {}
            for k, v in self.covariance.iteritems():
                temp['%s_%s'%(k[0], k[1])] = '%e'%v
            ET.SubElement(ret, "covariance_matrix", temp)
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

    def forParamFile(self):
        """ create a string that, if written to a file, can directly be used
        with, e.g. rivetgun. Only a parameter's name and its value will be
        included.
        """
        # a little sorting first
        pattern = re.compile(r'[0-9]+')
        def byInt(sa, sb):
            if int(pattern.findall(sa)[0]) < int(pattern.findall(sb)[0]):
                return -1
            else:
                return 1

        temp = {}
        for param in self.getKeys():
            temp[param] = self.parunscaled[self.getIndex(param)]
        # this has to be done in this way because otherwise the assignement
        # param->value may be broken
        temp2 = temp.keys()
        temp2.sort(cmp=byInt)

        # start creating the return string
        ret = ""
        for param in temp2:
            ret += "%s   %f\n"%(param, temp[param])
        return ret

    def asDict(self, scaled=True, includeerrors=False):
        """ return minimization result as simple dictionary """
        temp = dict.fromkeys(self._keys)
        for param in self._keys:
            if scaled:
                v = self.parscaled[self.getIndex(param)]
                if includeerrors:
                    e_low = self.errscaled[self.getIndex(param)][0]
                    e_high= self.errscaled[self.getIndex(param)][1]
                    temp[param] = [v, e_low, e_high]
                else:
                    temp[param] = v
            else:
                v = self.parunscaled[self.getIndex(param)]
                if includeerrors:
                    e_low = self.errunscaled[self.getIndex(param)][0]
                    e_high= self.errunscaled[self.getIndex(param)][1]
                    temp[param] = [v, e_low, e_high]
                else:
                    temp[param] = v
        return temp

    def asFlat(self, fname, scaled=False, includeerrors=True):
        """ write minimization result to a flat file 'fname'"""
        f=open(fname, 'w')
        d = self.asDict(scaled=scaled, includeerrors=includeerrors)
        for k in self.getKeys():
            if includeerrors:
                f.write("%s   %f   %f   %f\n"%(k, d[k][0], d[k][1], d[k][2]))
            else:
                f.write("%s   %f\n"%(k, d[k]))
        f.close()
        logging.debug("Written result to %s."%fname)

    def isInRange(self, rangedict):
        """ find out whether minimization result is inside ranges specified
            via rangedict
        """
        L_s = len(self.getKeys())
        L_r = len(rangedict.keys())
        if L_s == L_r:
            sharedkeys = [k for k in self.getKeys() if rangedict.has_key(k)]
        elif L_s > L_r:
            sharedkeys = [k for k in rangedict.keys() if k in self.getKeys()]
        else:
            raise StandardError("check your files!")

        MR_d = self.asDict(scaled=False)
        for k in sharedkeys:
        #for k,v in self.asDict(scaled=False).iteritems():
            m = min(rangedict[k])
            M = max(rangedict[k])
            if MR_d[k] >= m  and MR_d[k] <= M:
                continue
            else:
                logging.info("result not appended due to %s=%.3f being outside range (%.3f...%.3f)"%(k,MR_d[k],m,M))
                return False
        return True


class ResultList(list):
    """Container class for storing list of MinimizationResults.

    It is expected that all results were created with the same set of
    observables (and weighting).

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
    @classmethod
    def fromDirectory(cls, directory='.', identifier='results'):
        """ Create a ResultList instance from all identifier*.xml files
            found in the directory specified via directory
            NOTE: you need to know what you are doing here, validation is
            switched of here!
        """
        # find all the suitable xml files in the directory first
        resultfiles = [f for f in os.listdir(directory)
                if f.endswith('.xml') and f.startswith(identifier)]
        # iteratre over all files and store each MinimizationResult in a list
        results = []
        for f in resultfiles:
            tree = ET.parse(f)
            for el in tree.findall("minimization_result"):
                results.append(MinimizationResult.fromXMLElement(el))
        return cls(results, validate=False)


    def __init__(self, results=None, validate=True):
        if results is None:
            super(ResultList, self).__init__()
        else:
            super(ResultList, self).__init__(results)
        self.chi2sigma = None
        self.chi2mean = None

        if validate:
            self.isValid()

    def __str__(self):
        r = "Summary of %i minimization results:\n\n" % len(self)
        for param in self.getParamNames():
            w_mean, w_err = self.mean(param)
            r += "%s = %f +- %f (%.3f %%)\n" % (param, w_mean, w_err, 100 * float(w_err/w_mean))
        return r

    def getMinimum(self):
        """ return minimizationresult that yields the smallest chi2/ndof value """
        def chi2(mr):
            return mr.chi2/mr.ndof
        return min(self, key=chi2)

    def write(self, path):
        """Write MinimizationResults as xml data to file located at path.

        The cElementTree.write output is not formatted nicely (just one
        single line), you can use ::

            $ sed -e 's/>/>\\n/g' < INPUT.xml > OUTPUT.xml

        or::

            $ xmllint --format INPUT.xml > OUTPUT.xml

        to add new line characters after each tag. Remenber that INPUT and
        OUTPUT must not be the same!
        """
        root = ET.Element('minimization_result_list')
        for r in self:
            root.append(r.asXMLElement())
        et = ET.ElementTree(element=root)
        et.write(path, )

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
        """Return a list with the different numbers of runs used for the
        results.
        """
        ret = []
        for r in self:
            l = len(r.runs)
            if l not in ret:
                ret.append(l)
        ret.sort()
        return ret

    def isValid(self):
        """Perform some validity checks.

        - Checks if all stored results have the same parameters.
        - Checks if all stored results have the same set of observables.

        @raises FixedSortedKeysError: if results have different parameter names
                @see{FixedSortedKeys.goodPartner()}.
        @raises ValueError: if results have different sets of observables.
        """
        if len(self) > 0:
            first = self[0]
            # this might raise a FixedSortedKeysError
            [first.goodPartner(mr) for mr in self]
            for mr in self:
                if first.obs != mr.obs:
                    raise ValueError("Observables in result list miss-match!")

        return True

    def getObservables(self):
        return self[0].obs

    def getParamNames(self):
        return self[0].getKeys()

    def getKBest(self,K):
        """ return the K results that have the lowest chi2
            @param K: an integer that specifies how many results you want
        """
        best = []
        chi2s = [result.chi2 for result in self]
        chi2s.sort()

        for result in self:
            if result.chi2 in chi2s[:K]:
                best.append(result)
        return best

    def getResultsInsideRange(self, rangedict):
        """ return only those Minimization Results that are inside parameter
            ranges specified via rangedict
        """
        clean = [i for i in self if i.isInRange(rangedict)]
        return ResultList(clean)


    def getParamValues(self, param, K='all', unscaled = True):
        """ return all parameter values of a certain parameter param from
            either all results in the resultlist or the K best (in terms of
            chi2)
            @param param: string, the desired Parameter
            @param K: either 'all' to return paramvalues of the complete list
                or an integer, to return the k best results only
            @param unscaled: bool, True to return unscaled paramvalues
                everything else returns scaled values
        """
        if K == 'all':
            data = [result for result in self]
        elif type(K) == int and K >0 and K <= len(self):
            data = self.getKBest(K)
        else:
            raise ValueError("K has to be either 'all' or an integer between 1 "
                    "and %i"%len(self))
        if unscaled:
            return numpy.array([res.parunscaled[
                self.getParamNames().index(param)] for res in data])
        else:
            return numpy.array([res.parscaled[
                self.getParamNames().index(param)] for res in data])

    def translateCovariance(self, covdict, translator):
        """ translate paramnames as given in the translator dict """
        newdict = {}
        for k, v in covdict.iteritems():
            temp = [translator[name] for name in k]
            newdict[tuple(temp)] = v
        return newdict

    def getCovariances(self, retranslate=False):
        """ return a list of the covariance matrices as calculated by minuit """
        if not self[0].covariance is None:
            if retranslate:
                # create dictionary between minuit parnames and the real ones
                translator = {}
                keys = self[0].covariance.keys()
                minuitpars = []
                for k in keys:
                    for param in k:
                        if not param in minuitpars:
                            minuitpars.append(param)
                minuitpars.sort()
                for num, mpar in enumerate(minuitpars):
                    translator[mpar] = self.getParamNames()[num]

                return [self.translateCovariance(i.covariance, translator) for i in self if not i.covariance is None]
            else:
                return [i.covariance for i in self if not i.covariance is None]
        else:
            return None

    def getCorrelationMatrix(self, covmat):
        """ return a matrix of parameter correlation coefficients calculated
            from a covariance matrix covmat
        """
        corrmat = {}
        for i in covmat.keys():
            corrmat[i] = formulas.getCorrelation(covmat, i[0], i[1])
        return corrmat

    def getCorrelations(self, retranslate=False, meansonly=False):
        """ Return a list of matrices of correlation coefficients for all
            MinimizationResults in the ResultList.
            If retranslate is set to True, then the common parameter names are
            used otherwise the minuit names will be used.
            If meansonly is set to yes, only the mean and the rms of the
            calculated correlation coefficients are returned for each pair
            of parameters.
        """
        if not self.getCovariances() is None:
            corrmats = map(self.getCorrelationMatrix, self.getCovariances(retranslate))
            if meansonly:
                statdict = {}
                for key in corrmats[0].keys():
                    temp = [d[key] for d in corrmats]
                    statdict[key] = (numpy.mean(temp), formulas.rms(temp))
                return statdict
            else:
                return corrmats
        else:
            return None


    def mean(self, param):
        """ Return weighted mean of param values and the mean of the largest
            and the smallest uncertainty as typical error.
        """
        temp = []
        for i in self:
            value = i.parunscaled[i.getIndex(param)]
            idx = i.getIndex(param)
            maxerror = max(abs(i.errunscaled[idx]))
            temp.append((value, maxerror))
        E = numpy.array(temp)[:,1]
        return formulas.weightedMean(temp)[0], 0.5*(max(E)+min(E))


    def suggestScan(self, reslist):
        borders = {}
        for paramname in self.getParamNames():
            values = []
            for result in reslist:
                values.append(result.parunscaled[result.getIndex(paramname)])
            borders[paramname] = (min(values), max(values))
        return borders

    # TODO: (re)move this or make it a staticmethod or ...
    def writeSuggestion(self, result_dict, outfile):
        f = open(outfile, 'w')
        for name, partuple in result_dict.iteritems():
            f.write('%s    %f    %f \n'%(name, partuple[0], partuple[1]))
        f.close()
