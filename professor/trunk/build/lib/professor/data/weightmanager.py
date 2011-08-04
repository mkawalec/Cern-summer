"""
System for managing weight-like quantities -- e.g. observable weights, extra
error ("epsilon") factors, etc. -- which can need to be specified on a
per-observable or per-range basis.
"""

import re
import numpy

from professor.tools.errors import WeightError
from professor.tools import log as logging


class Weight(object):
    """A simple object that holds a dict with binrange:weight pairs.

    The weights have been extended to be general bin properties since the first
    design, and a reworking of this class design is probably overdue."""

    def __init__(self, obs):
        self.obs = obs
        self._props = {}


    def binRanges(self):
        return self._props.keys()


    def _binRangeIsOk(self, binrange):
        """
        Check if newly to be added range is not in conflict/identical to already existing one.

        TODO: *Allow* overlaps, so that overriding can be done
        """
        ## Check for exact same definitions given multiple times
        if binrange in self.binRanges():
            raise WeightError("Weight already set for %s:%s" % (self.obs, binrange))
        ## Make sure intervals don't overlap
        else:
            ## Lower and upper edge of the binrange to be inspected
            low  = float(binrange[0])
            high = float(binrange[1])

            ## Make sure that low edge really is lower than upper edge
            if low > high:
                raise WeightError("Lower edge (%f) of bin range larger than upper"
                                  " edge: %s:%s" % (low, self.obs, binrange,))

            ## Check for overlaps
            for br in self.binRanges():
                ## Case A, low overlap
                if low < float(br[0]) and high > float(br[0]):
                    raise WeightError("Upper edge (%f) of binrange %s conflicts with"
                                      " binrange %s:%s" % (
                                      high, self.obs, binrange, br))
                ## Case B, high overlap
                if low < float(br[1]) and high > float(br[1]):
                    raise WeightError("Lower edge (%f) of binrange %s conflicts with"
                                      " binrange %s:%s" % (
                                      slow, elf.obs, binrange, br))
                ## Case C, nesting
                if low >= float(br[0]) and high <= float(br[1]):
                    raise WeightError("Binrange (%f --- %f) %s fully overlaps"
                                      " with binrange %s:%s" % (
                                      low, high, self.obs, binrange, br))


    def setProperty(self, binrange, propname, propvalue):
        """Set a property for the given bin range. The numerical weight is the
        most common property, for which the `propname` is "weight".
        """
        self._props.setdefault(binrange, { "weight" : 0.0 })[propname] = propvalue


    def setProperties(self, binrange, *args, **kwargs):
        """Set several properties at once, by supplying either a single dict
        object or via keyword arguments.
        """
        mydict = None
        if args:
            assert len(args) == 1 and isinstance(args[0], dict)
            mydict = args[0]
        elif kwargs:
            mydict = kwargs
        else:
            raise Exception("Bad arguments to Weight.setProperties")
        for k, v in mydict.iteritems():
            self.setProperty(binrange, k, v)


    def getProperties(self, bincenter):
        """Get the properties for a given observable value, excluding the "weight" property.
        """
        rtn = None
        # TODO: Can be made more efficient by using an efficient search/OrderedDict?
        for k, v in self._props.iteritems():
            if float(k[0]) <= bincenter and bincenter < float(k[1]):
                rtn = v
                break
        #if rtn and "weight" in rtn:
        #    del rtn["weight"]
        return rtn


    def setWeight(self, bincenter, weight):
        """Set the bin range weight property."""
        self.setProperty(bincenter, "weight", weight)


    def getWeight(self, bincenter):
        """ Evaluate the weight for bincenter by iterating over
            binrange:Weight definitions
            If the bincenter is outside the ranges, return 0
        """
        # TODO: Can be made more efficient by using an efficient search/OrderedDict?
        for k, v in self._props.iteritems():
            if float(k[0]) <= bincenter and bincenter < float(k[1]):
                return v["weight"]
        return 0.0


    def __str__(self):
        out = ""
        for binrange in self.binRanges():
            out += self.obs
            if binrange != (-numpy.inf, numpy.inf):
                out += ":"
                if binrange[0] != -numpy.inf:
                    out += "%2.1f" % binrange[0]
                out += ":"
                if binrange[1] != numpy.inf:
                    out += "%2.1f" % binrange[1]
            out += " %2.1f\n" % self.getWeight(sum(binrange)/2.0)
        return out



class WeightManager(object):
    """
    This simple object loads observable weight/property files and stores a
    dictionary with observable:Weight pairs
    """

    def __init__(self):
        self._weightdict = {}


    @classmethod
    def mkFromFile(cls, path):
        new = cls()
        new.loadWeightsFile(path)
        return new


    def loadWeightsFile(self, wfile):
        ## General line format: "/path/to/histo[:[$xlow][:[$xhigh]]] <$weight|weight=$weight> [key=$val]
        bindef_re = re.compile(r"([^#:\s]+)\s*(:[-+\de\.]*)?(:[-+\de\.]*)?(.*)", re.I)
        arg_re = re.compile(r"([\w]+=)?([-+\de\.\w%]+)(.*)", re.I)

        f = open(wfile, 'r')
        for rawline in f:
            ## Strip leading/trailing white spaces, e.g. newline
            line = rawline.strip()
            if len(line) == 0 or line.startswith('#'):
                continue
            if "#" in line:
                line = line[:line.index("#")].strip()
            try:
                bindef_groups = bindef_re.search(line).groups()
            except Exception, e:
                logging.error("Could not parse line '%s' from observable file '%s'" % (line, wfile))
                raise e

            ## Extract bin definitions
            path = bindef_groups[0]
            def get_limit(x, default):
                if x is None:
                    return default
                x = x.replace(":", "").strip()
                if x == "":
                    return default
                return float(x)
            low = get_limit(bindef_groups[1], -numpy.inf)
            high = get_limit(bindef_groups[2], numpy.inf)
            #print low, high

            ## Extract extra arguments
            args = bindef_groups[-1]
            remaining = args
            argnum = 0
            props = {}
            while True:
                argnum += 1
                match = arg_re.search(remaining)
                if not match:
                    remaining = None
                    break
                argname, argvalue, remaining = match.groups()
                if argname is None:
                    if argnum == 1:
                        argname = "weight"
                    else:
                        raise WeightError("Unnamed bin property in non-standard position: %s in position %d" % (argvalue, argnum))
                else:
                    argname = argname.replace("=", "")
                props[argname] = argvalue
            #print props

            ## Extract weight and catch ill-defined weights
            weight = props.get("weight", 1.0)
            if "weight" in props:
                del props["weight"]
            try:
                weight = float(weight)
            except:
                raise WeightError("Invalid weight definition (%s) in '%s'" % (weight, line))

            ## Add the weight definition to the WM
            self.addBinRangeWeight(path, (low, high), weight, **props)


    def addBinRangeWeight(self, observable, binrange=(-numpy.inf, numpy.inf), weight=1.0, **kwargs):
        """Set the weights for bins of 'observable' in 'binrange'.

        Parameters
        ----------
        observable : str
            Path of the observable.
        binrange : tuple of floats
            The x-value bin range.
        weight : float
            Weight for the bins.
        kwargs : dict
            Extra named arguments, passed to be Weight properties with those names.
        """
        w = self._weightdict.setdefault(observable, Weight(observable))
        kwargs["weight"] = weight # official weight arg always wins
        w.setProperties(binrange, kwargs)


    """
    Accessor for sorted list of observables, including those with zero weight.
    """
    observables = property(lambda self: sorted(self._weightdict.keys()))


    """
    Indexing operator for weight lookup. Also useable as `wm["obsname"]`.

    If `obsvalue` is not given or is None, this function returns a Weight object,
    or None if there is no matching observable to the `obs` string. If `obsvalue`
    is given, return the numerical weight for that observable value, obtained via
    the `Weights.getWeight` method.
    """
    def getWeight(self, obs, obsvalue=None):
        w = self._weightdict.get(obs)
        if obsvalue is None:
            return w
        x = float(obsvalue)
        return w.getWeight(x)


    ## Array-like element access operator syntax
    """
    An array-like operator for accessing bin-range weights values. Behaves the
    same as `getWeight`, but since only one argument can be supplied, the optional
    `obsvalue` parameter is encoded as part of the `obs` string, with syntax
    `/path/to/obsname:42` for an observable value of 42.
    """
    def __getitem__(self, obs):
        obsvalue = None
        if ":" in obs:
            obs, obsvalue = obs.split(":", 0)
        return self.getWeight(obs, obsvalue)


    def __str__(self):
        wstring = "Observables/weights:\n"
        for obs in sorted(self.observables):
            v = self.getWeight(obs)
            wstring += str(v)
        return wstring
