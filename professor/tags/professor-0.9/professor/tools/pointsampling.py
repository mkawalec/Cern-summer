import logging
import numpy, random
from professor.tools import parameter, formulas

## Set up logging
logging.basicConfig(level=20, format="%(message)s")
logging.debug("This is not RivetRunner\n")

class PointGenerator(list):
    def __init__(self, ranges=None):
        super(PointGenerator, self).__init__()
        self._paramranges = ranges

    def getParamRanges(self):
        return self._paramranges

class RandomPointGenerator(PointGenerator):
    """ ranges may also be a Hypercube object
    """
    def __init__(self, ranges, N):
        self._N = N
        super(RandomPointGenerator, self).__init__(ranges)
        for i in xrange(N):
            self.append(self.chooseRandomParams())

    def chooseRandomParams(self, rangefrac=1):
        """Make a random set of parameter values."""
        paramset = {}
        for k, v in self.getParamRanges().iteritems():
            low, high = min(v), max(v)
            rangewidth = high - low
            rangelow  = low + (1-rangefrac)/2.0 * rangewidth
            rangehigh = high - (1-rangefrac)/2.0 * rangewidth
            val = random.uniform(rangelow, rangehigh)
            paramset[k] = val
        return paramset

class ScanPointGenerator(PointGenerator):
    """ Providing methods to sample points from a hypercube.
    """
    def __init__(self, hypercube, N, minres=None):
        self._N = N
        self._minres = minres
        # self._hypercube = hypercube
        # self._piercing_fname = piercing_fname
        super(ScanPointGenerator, self).__init__(hypercube)

    def generateLine(self, gradients_offsets=None, rangefrac = 1.0):
        if gradients_offsets is None:
            logging.info("calculating gradients and offsets for body diagonal")
            gradients, offsets = self.getGradientsForDiagonal()
        else:
            gradients, offsets = gradients_offsets

        # define control parameter ts first
        tStart = 0 - (rangefrac-1) / 2.0
        tEnd = 1 + (rangefrac-1) / 2.0
        ts = numpy.linspace(tStart, tEnd, self._N, endpoint=True)
        # use gradients and offsets to calculate p = gradient*t + offset
        for t in ts:
            paramset = {}
            paramset["PROF_SCAN_PARAM"] = t
            for k in self.getParamRanges().keys():
                paramset[k] = offsets[k] + gradients[k]*t
            self.append(paramset)

    def getGradientsForDiagonal(self):
        """ prepare gradients and offsets so that they can be used in
            generateLine(), i.e. line calculation against a control parameter
        """
        offsets, gradients = {}, {}
        for k, v in self.getParamRanges().iteritems():
            offsets[k] = v[0]
            gradients[k] = v[1] - v[0]
        return gradients, offsets

    def getGradientsForExtremalScan(self, direction, symmetric):
        """ prepare gradients and offsets so that they can be used in
            generateLine(), i.e. line calculation against a control parameter
            one can choose whether the scan is to be performed along the
            direction of the largest or the smallest uncertainty
        """
        offsets, gradients = {}, {}
        p1, p2 = self.getPiercingPoints(direction, symmetric)

        s = "Sampling between end points:"
        maxlen = max(map(len, p1.keys()))
        for k in sorted(p1.keys()):
            s += "\n        %s   %f   %f" % (k.ljust(maxlen), p1[k], p2[k])
        logging.info(s)

        for pname in self.getParamRanges().keys():
            offsets[pname] = p1[pname]
            gradients[pname] = p2[pname] - p1[pname]
        return gradients, offsets

    def getExtremalGradient(self, direction):
        """ return dictionary that holds definition of a vector of length 1
            It's direction is calculated based on a MinimizationResults
            covariance matrix by looking for the largest or smallest (in
            absolute values) eigenvalue
        """
        if self._minres is None:
            raise ValueError("Must specify MinimizationResult!")
        grad = {}
        ## calculate the gradient vector
        grad_temp= formulas.getExtremalDirection(self._minres.getCovMatrix(),
                                                 direction=direction)
        ## store it as user friendly dictionary
        for num, param in enumerate(self._minres.getFreeParameters()):
            # convert 1x1 matrix to float
            grad[param] = float(grad_temp[num])
        for param in self._minres.getFixedParameters():
            grad[param] = 0.0
        return grad

    def getPiercingPoints(self, direction, symmetric):
        """Get line endpoints of line along min/max covariance direction.

        The endpoints are the intersection points of the line with the
        surrounding hypercube. The line goes through the given
        MinimizationResult.

        If the hypercube is centered around the MinimizationResult this
        points should be symmetric around the center of the hypercube.
        """
        center = self._minres.asDict(scaled=False)
        grad = self.getExtremalGradient(direction)
        freeparamters = self._minres.getFreeParameters()

        # calculate distance of the points of intersection for every
        # hypercube plane
        # x_i = center_i + grad_i * t  => t parameterises distance

        # arrays of t-values of intersection points
        tlows= numpy.nan*numpy.ones(len(freeparamters))
        thighs = numpy.nan*numpy.ones(len(freeparamters))
        for i, pname in enumerate(freeparamters):
            tlows[i] = (self._paramranges[pname][0] - center[pname])/grad[pname]
            thighs[i] = (self._paramranges[pname][1] - center[pname])/grad[pname]
        # test that this worked
        if numpy.isnan(tlows).any() or numpy.isnan(thighs).any():
            raise ValueError("Low or high parameterisations is NaN!")
        # print "l:", tlows
        # print "h:", thighs

        ts = numpy.concatenate((tlows, thighs))

        # Now we need the smallest and second-smallest abs(t-values) with
        # opposite signs.
        i1 = numpy.argmin(abs(ts))
        t1 = ts[i1]
        # t2 is minimum of all t-values with opposite sign of t1
        if t1 < 0.0:
            t2 = (ts[ts > 0.0]).min()
        else:
            t2 = (ts[ts < 0.0]).max()
        # print "1[%s]  2[%s]" % (t1, t2)

        if symmetric:
            logging.info("Making line end points symmetric around given center")
            if abs(t1) > abs(t2):
                t1 = -t2
            else:
                t2 = -t1
        # print "1[%s]  2[%s]" % (t1, t2)

        low = {}
        high = {}
        for pname in freeparamters:
            low[pname] = center[pname] + grad[pname]*t1
            high[pname] = center[pname] + grad[pname]*t2
        for pname in self._minres.getFixedParameters():
            pindex = self._minres.getIndex(pname)
            pvalue = self._minres.parunscaled[pindex]
            low[pname] = pvalue
            high[pname] = pvalue

        return low, high


class Hypercube(dict):
    """
    """
    @classmethod
    def fromTwoPoints(cls, p1, p2, excess=.0):
        temp = {}
        # TODO: check if p1.keys() == p2.keys()
        g = cls.getGradientFromTwoPoints(p1,p2)
        dl = dict((k, excess*v) for k, v in g.iteritems())

        for k in p1.keys():
            temp[k] = (p1[k] - dl[k], p2[k] + dl[k])
        return cls(temp)

    def __init__(self, ranges=None):
        if ranges is None:
            super(Hypercube, self).__init__({})
        else:
            super(Hypercube, self).__init__(ranges)

    def __str__(self):
        msg = "Hypercube in %i-dimensional parameter space:\n\n"%(
                len(self.keys()))
        for k in sorted(self.keys()):
            msg += "\t %s: %f ... %f\n"%(k, self[k][0],
                    self[k][1])
        return msg

    def getRanges(self):
        return self.copy()

    @classmethod
    def getLengthBetweenPoints(self, p1, p2):
        """ return the length of the line between two points (dict typt)
        """
        a = numpy.array([p1[k] - p2[k] for k in p1.keys()])
        return numpy.sqrt(numpy.dot(a,a))

    @staticmethod
    def getGradientFromTwoPoints(p1, p2):
        """ return gradient of the line between two points p1 and p2
        """
        gradient = {}
        for k in p1.keys():
            gradient[k] = p2[k] - p1[k]
        return gradient

    def getGradient(self):
        """return gradient of the line between points that define
            the hypercube
        """
        gradient = {}
        for k, v in self.getRanges().iteritems():
            gradient[k] = v[1] - v[0]
        return gradient

    def getOffset(self):
        """ return offset of the line bewtween points that define
            the hypercube, which is  one of the hypercube defining
            points
            TODO: * remove this???
        """
        offset = {}
        for k, v in self.getRanges().iteritems():
            offset[k] = v[0]
        return offset

    def write(self, fname='hypercube.params'):
        f=open(fname, 'w')
        f.write("# hypercube\n")
        for k in sorted(self.keys()):
            f.write("%s   %f   %f\n"%(k, self[k][0], self[k][1]))
        f.close()
        logging.info("written hypercube params to %s"%fname)

class SymmetricHypercube(Hypercube):
    """The largest hypercube that is symmetric around a given center point
    and fits in another hypercube.

    TODO: overwrite write method
    """
    @classmethod
    def fromMinimizationResult(cls, ranges, minres):
        return cls(ranges, minres.asDict(scaled=True))

    @classmethod
    def fromFlatFile(cls, ranges, thefile):
        return cls(ranges, parameter.ppFromFile(thefile, ranges).asDict(scaled=True))

    def __init__(self, ranges, center, scaler=None):
        """
        center  -- a dictionary with *scaled* parameter values.
        """
        if sorted(ranges.keys()) != sorted(center.keys()):
            raise ValueError("Ranges and center have different parameter names!")

        self._center = center
        for name, val in center.items():
            if val < 0.0 or val > 1.0:
                raise ValueError("Parameter '%s' is outside of the cube"
                                 " (scaled value not in [0.0, 1.0]." % (name))

        if scaler is None:
            logging.warning("creating scaler from cube definition")
            self._scaler = parameter.Scaler(ranges)
        else:
            self._scaler = scaler

        super(SymmetricHypercube, self).__init__(self.getLargestCube())

    # helper for __init__
    def getCenter(self):
        return self._center

    # helper for __init__
    def getClosestDistance(self):
        """ calculate the closest distance (in the scaled world) of the center
            to any of the parameter axes defined via ranges
        """
        center = self.getCenter().values()
        temp = (min(center), min(numpy.ones(len(center)) - center))
        return min(temp)

    # helper for __init__
    def getLargestCube(self):
        """ return the largest possible symmetric hypercube centered around
            center which still completely fits into the original hypercube
            defined via ranges.
            Return values are unscaled.
        """
        tempmin, tempmax = dict.fromkeys(self), dict.fromkeys(self)
        center = self.getCenter()
        dist = self.getClosestDistance()
        for param, value in center.iteritems():
            tempmin[param] = center[param] - dist
            tempmax[param] = center[param] + dist
        # convert dicts to ParameterPoints for rescaling
        Pmin = parameter.ParameterPoint(tempmin, self._scaler, scaled=True)
        Pmax = parameter.ParameterPoint(tempmax, self._scaler, scaled=True)
        # create dict {param:(plow, phigh),...} as return value
        ret = dict.fromkeys(self)
        for k in self._scaler.getKeys():
            ret[k]=(Pmin.asDict(scaled=False)[k], Pmax.asDict(scaled=False)[k])
        return ret
