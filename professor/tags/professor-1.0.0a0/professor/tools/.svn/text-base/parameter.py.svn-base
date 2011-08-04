"""parameter.py

This file contains 3 classes which allow us to handle parameters in a
controlled way:
    - class L{FixedSortedKeys}:
        Stores an alphabetically sorted list of key names, normally the
        parameter names.
        It's the base class for classes dealing with parameter vectors.

    - class L{Scaler}:
        Stores upper and lower boundaries for parameter scaling.

    - class L{ParameterPoint}:
        Stores scaled and unscaled versions of the given parameter
        point.

"""

__all__ = ["Scaler", "ParameterError", "ParameterPoint", "ParameterRange",
           "prettyPrintParameter", "readParameterFile"]

import re
import numpy

from professor.tools.errors import ParameterError
from professor.tools.fixedsortedkeys import FixedSortedKeys


class Scaler(FixedSortedKeys):
    def __init__(self, data):
        """
        @param data: A C{list} with the parameter names, this Scaler
            instance should handle. If it's a C{dict}, it must contain
            C{{"param name" : (min, max)}} pairs.
            If it's a C{list} lower boundaries are set to 0 upper to 1. So
            NO scaling takes place.
        @type data: C{dict} or C{list}
        @raise TypeError: If data is of wrong type.
        """
        if type(data) == list:
            super(Scaler, self).__init__(data)
            self._min = numpy.zeros(len(self))
            self._max = numpy.ones(len(self))

        elif type(data) == dict:
            super(Scaler, self).__init__(data.keys())
            self._min = numpy.zeros(len(self))
            self._max = numpy.zeros(len(self))
            for i, name in enumerate(self.getKeys()):
                self._min[i] = data[name][0]
                self._max[i] = data[name][1]

        else:
            raise TypeError("data must be a list or dict!")

    def setVal(self, name, min=None, max=None):
        """Set a new minimal and/or maximal value.

        @param name: the parameter name.
        @param min: the new lower boundary
        @param max: the new upper boundary
        """
        i = self.getIndex(name)
        if min is not None:
            self._min[i] = min
        if max is not None:
            self._max[i] = max

    def getMinVals(self):
        return self._min

    def getMaxVals(self):
        return self._max

    def getMinVal(self, name):
        return self._min[self.getIndex(name)]

    def getMaxVal(self, name):
        return self._max[self.getIndex(name)]

    def scale(self, vec):
        return (vec - self._min)/(self._max - self._min)

    def scaleComponent(self, scaledval, paramid):
        """Descale the given scaled parameter value.

        paramid can be an int (=> parameter index)
        or a string (=> parameter name).
        """
        if type(paramid) != int:
            paramid = self.getIndex(paramid)
        return (scaledval - self._min[paramid])/(self._max[paramid] - self._min[paramid])

    def descale(self, vec):
        return vec*(self._max - self._min) + self._min

    def descaleComponent(self, scaledval, paramid):
        """Descale the given scaled parameter value.

        paramid can be an int (=> parameter index)
        or a string (=> parameter name).
        """
        if type(paramid) != int:
            paramid = self.getIndex(paramid)
        return scaledval*(self._max[paramid] - self._min[paramid]) + self._min[paramid]

    def __str__(self):
        r = "Scaler:\n"
        r += "    param   lower  upper\n"
        for key in self.getKeys():
            r += "    %s   %e  %e\n"%(key, self.getMinVal(key), self.getMaxVal(key))
        return r[:-1]


class ParameterPoint(FixedSortedKeys):
    @classmethod
    def fromList(cls, plist, scaler, scaled=False):
        """Build a ParameterPoint instance from a list with parameter values.

        Uses the given scaler to get the parameter names.

        @param plist: C{list}-like object with the parameter values.
        """
        d = {}
        for i, pname in enumerate(scaler.getKeys()):
            d[pname] = plist[i]
        return cls(d, scaler, scaled)

    @classmethod
    def fromFile(cls, paramfile, ranges, scaled=False):
        """Load parameters from a file.

        Parameters
        ----------
            paramfile : str
                The path of the parameter file.
            ranges : Scaler, str, dict
                The sampling ranges. If a str is given, the path of the
                range file is expected.
        """
        params = readParameterFile(paramfile)
        if type(ranges) != Scaler:
            if type(ranges) == str:
                ranges = readParameterFile(ranges)
            elif type(ranges) != dict:
                raise TypeError("Argument ranges has wrong type: '%s' of"
                                " type %s" % (ranges, type(ranges)))
            scaler = Scaler(ranges)
        return cls(params, scaler, scaled)

    def __init__(self, data, scaler, scaled=False):
        """
        Parameter data is stored scaled AND unscaled! But the unscaled
        values are regarded as constant whereas the scaled values can
        changed, e.g. when new scaling boundaries are chosen.

        @param data: C{dict} with parmeter name - value pairs.
        @param scaler: L{Scaler} instanced, used to scale this
            parameter point.
        @param scaled: Flag indicating if the given data is scaled.
        @raise ValueError: If give data and scaler don't have the same
            keys.
        """
        super(ParameterPoint, self).__init__(data.keys())

        # Check if I and the given scaler share the same parameter names.
        FixedSortedKeys.goodPartner(self, scaler)
        self._scaler = scaler

        t = numpy.zeros(self.dim())
        for i, name in enumerate(self.getKeys()):
            t[i] = data[name]

        if scaled:
            self._scaled = t
            self._unscaled = self._scaler.descale(t)
        else:
            self._scaled = self._scaler.scale(t)
            self._unscaled = t

    def getScaler(self):
        return self._scaler

    def getScaled(self):
        return self._scaled.copy()

    def getUnscaled(self):
        return self._unscaled.copy()

    def rescale(self):
        """Recalculate the scaled values.

        Use this if scaling boundaries change.
        """
        self._scaled = self._scaler.scale(self._unscaled)

    def __str__(self):
        if hasattr(self, "_scaled") and hasattr(self, "_unscaled"):
            jwidth = max(map(len, self.getKeys()))
            r = "%s:\n"%(self.__class__.__name__)
            r += "    param   unscaled  scaled\n"
            for i, name in enumerate(self.getKeys()):
                r += "    %s   %e  %e\n" % (name.ljust(jwidth),
                                            self._unscaled[i],
                                            self._scaled[i])
            return r[:-1]
        else:
            return "<Partly initialised ParameterPoint instance>"

    def goodPartner(self, candidate):
        """Checks if self and candidate have the same keys and scalers.

        @type candidate: ParameterPoint
        """
        super(ParameterPoint, self).goodPartner(candidate)
        if not self._scaler is candidate._scaler:
            raise ParameterError("scalers differ: no good partner!")
        return True

    def asDict(self, scaled=True):
        """ return parameter point as simple dictionary """
        temp = dict.fromkeys(self.getKeys())
        for param in self.getKeys():
            if scaled:
                temp[param] = self.getScaled()[self.getIndex(param)]
            else:
                temp[param] = self.getUnscaled()[self.getIndex(param)]
        return temp

    def distanceToP0(self, p0, scaled=False):
        """Calculate the length of self-p0.

        Arguments
        ---------
            p0 : ParameterPoint
            scaled : bool
                If True, calculate the distance in the space of scaled
                parameters.
        """
        if scaled:
            dist = self._scaled - p0._scaled
        else:
            dist = self._unscaled - p0._unscaled
        return numpy.norm(dist)


class ParameterRange(FixedSortedKeys):
    """Wrapper for parameter range hypercube."""
    def __init__(self, rangedict):
        super(ParameterRange, self).__init__(rangedict.keys())
        self._ranges = rangedict.copy()
        self.keys = self.getKeys

    def __getitem__(self, paramname):
        return self._ranges[paramname]

    def getLowerBound(self, paramname):
        return self._ranges[paramname][0]

    def getUpperBound(self, paramname):
        return self._ranges[paramname][1]

    def __str__(self):
        jwidth = max(map(len, self.keys()))
        s = ""
        for name in self.keys():
            s += "%s  %e  %e\n" % (name.ljust(jwidth),
                                   self.getLowerBound(name),
                                   self.getUpperBound(name))
        s = s[:-1]
        return s

    def getDiagonal(self):
        """Return the length of the body diagonal."""
        diag2 = 0.0
        for v in self._ranges.values():
            diag2 += (v[0] - v[1])**2
        return numpy.sqrt(diag2)


def prettyPrintParameter(arg):
    """Pretty multiline formatted string version of arg.

    Parameters
    ----------
        arg : dict, ParameterPoint
    """
    if type(arg) == dict:
        s = ""
        # length of longes parameter name
        jwidth = max(map(len, arg.keys()))
        for name in sorted(arg.keys()):
            s += name.ljust(jwidth)
            val = arg[name]
            try:
                for v in val:
                    s += "  %e" % v
                s += "\n"
            except TypeError:
                s += "  %e\n" % val
        # strip last newline
        s = s[:-1]
        return s
    return str(arg)


def readParameterFile(path, checklog=False):
    """Read a parameter file and return the according dictionary."""
    pfile = open(path, 'r')

    params = {}
    logs = []
    for line in pfile:
        line = re.sub(r'(^.*?)#.*', r'\1', line) # strip comments
        line = re.sub(r'=+', r' ', line) # collapse equal signs
        line = line.strip() # strip leading/trailing white spaces
        if len(line) == 0:
            continue
        tokens = line.split()
        if len(tokens) == 2:
            params[tokens[0]] = float(tokens[1])
        elif len(tokens) == 3:
            params[tokens[0]] = numpy.array([float(tokens[1]), float(tokens[2])])
        elif len(tokens) == 4:
            if checklog and tokens[3] in ["L","l","log","LOG"]:
                params[tokens[0]] = numpy.array([float(tokens[1]), float(tokens[2])])
                logs.append(tokens[0])
            else:
                params[tokens[0]] = numpy.array([float(tokens[1]), float(tokens[2]), float(tokens[3])])
    ## consistency check:
    for k, v in params.iteritems():
        if not type(params[params.keys()[0]]) == type(v):
            raise Exception("Parameter file faulty in param %s!" % (k))
    pfile.close()
    if checklog:
        return params, logs
    else:
        return params
