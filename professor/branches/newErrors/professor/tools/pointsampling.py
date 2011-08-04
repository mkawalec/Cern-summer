from professor.tools import parameter, formulas
import os, sys, re, logging, commands, glob, shutil, time
import numpy, random

## Set up logging
logging.basicConfig(level=20, format="%(message)s")
logging.debug("This is not RivetRunner\n")

class PointGenerator(list):
    """
    """
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
    def __init__(self, hypercube, N, minres=None, piercing_fname="piercing.params"):
        self._N = N
        self._minres = minres
        self._hypercube = hypercube
        self._piercing_fname = piercing_fname
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
        ts = numpy.linspace(tStart, tEnd, self._N)
        # use gradients and offsets to calculate p = gradient*t + offset
        for t in ts:
            paramset = {}
            paramset["PROF_SCAN_PARAM"] = t
            for k in self.getParamRanges().keys():
                paramset[k] = offsets[k]
                paramset[k] += gradients[k] * t
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

    def getGradientsForExtremalScan(self, direction):
        """ prepare gradients and offsets so that they can be used in
            generateLine(), i.e. line calculation against a control parameter
            one can choose whether the scan is to be performed along the
            direction of the largest or the smallest uncertainty
        """
        offsets, gradients = {}, {}
        p1, p2 = self.getPiercingPoints(
                self.getExtremalGradient(
                    direction=direction))
        for k, v in self.getParamRanges().iteritems():
            offsets[k] = p1[k]
            gradients[k] = p2[k] - p1[k]
        return gradients, offsets

    def getExtremalGradient(self, direction):
        """ return dictionary that holds definition of a vector of length 1
            It's direction is calculated based on a MinimizationResults
            covariance matrix by looking for the largest or smallest (in
            absolute values) eigenvalue
        """
        if self._minres is None:
            raise StandardError("Must specify MinimizationResult!")
        grad = {}
        ## calculate the gradient vector
        grad_temp= formulas.getExtremalDirection(
                self._minres.getCovMatrix(),
                direction=direction)
        ## store it as user friendly dictionary
        for num, param in enumerate(self._minres.getKeys()):
            grad[param] = float(grad_temp[num])
        return grad

    def getPiercingPoints(self, grad, tries=10000, symmetric=True):
        """ Iteratively try to find those points where the LINESCAN line
            pierces the surropunding cube and return those points as dicts
            TODO: * make it symmetric!!!
        """
        logging.info("iteratively trying to find piercing points")
        center = self._minres.asDict(scaled=False)
        # length of body diagonal
        a = numpy.sqrt(sum([v[1] - v[0] for v in self._paramranges.values()]))
        # start iteration from the center in positive gradient direction
        temp = []
        for i in xrange(1, tries):
            newpoint = dict.fromkeys(self._paramranges)
            for k in self._paramranges.keys():
                newpoint[k] = i*grad[k]/(a*2*tries) + center[k]
            temp.append(newpoint)
            if not self.pointIsInsideRanges(newpoint, self._paramranges):
                break
        high = temp[-2]
        # start iteration from the center in negative gradient direction
        temp = []
        for i in xrange(1, tries):
            newpoint = dict.fromkeys(self._paramranges)
            for k in self._paramranges.keys():
                newpoint[k] =  center[k] - i*grad[k]/(a*2*tries)
            temp.append(newpoint)
            if not self.pointIsInsideRanges(newpoint, self._paramranges):
                break
        low = temp[-2]
        if symmetric:
            if self.getDistanceFromCenter(high, center) > self.getDistanceFromCenter(low, center):
                high = self.pointInversion(low, center)
            else:
                low = self.pointInversion(high, center)

        # save piercing points to file
        f=open(self._piercing_fname, 'w')
        f.write("# piercing points from scan along extremal direction\n")
        for k in sorted(low.keys()):
            f.write("%s   %f   %f\n"%(k, low[k], high[k]))
        f.close()
        logging.info("written piercing point params to %s "%self._piercing_fname)
        return low, high

    def getDistanceFromCenter(self, point, center):
        square_dist = 0.0
        for k in self._paramranges.keys():
            square_dist += (center[k] - point[k])**2
        return numpy.sqrt(square_dist)

    def pointInversion(self, point, center):
        temp = dict.fromkeys(self._paramranges)
        for k in self._paramranges.keys():
            temp[k] = 2.*center[k] - point[k]
        return temp


    def pointIsInsideRanges(self, point, ranges):
        """ return True if coordinates given by dict point are within allowed
            ranges of these specified by dict ranges
        """
        for k, v in ranges.iteritems():
            if v[0] <= point[k] and  v[1] >= point[k]:
                continue
            else:
                return False
        return True

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
        self._ranges = ranges
        if ranges is None:
            super(Hypercube, self).__init__({})
        else:
            super(Hypercube, self).__init__(ranges)

    def __str__(self):
        msg = "Hypercube in %i-dimensional parameter space:\n\n"%(
                len(self._ranges.keys()))
        for k in sorted(self._ranges.keys()):
            msg += "\t %s: %f ... %f\n"%(k, self._ranges[k][0],
                    self._ranges[k][1])
        return msg

    def getRanges(self):
        temp = {}
        for k,v in self._ranges.iteritems():
            temp[k] = v
        return temp

    @classmethod
    def getLengthBetweenPoints(self, p1, p2):
        """ return the length of the line between two points (dict typt)
        """
        a = numpy.array([p1[k] - p2[k] for k in p1.keys()])
        return numpy.sqrt(numpy.dot(a,a))

    @classmethod
    def getGradientFromTwoPoints(self, p1, p2):
        """ return gradient of the line between two points p1 and p2
        """
        gradient = {}
        for k in p1.keys():
            gradient[k] = p2[k] - p1[k]
        return gradient

    def getGradient(self):
        """ return gradient of the line bewtween points that define
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
    """
    TODO: overwrite write method
    """
    @classmethod
    def fromMinimizationResult(cls, ranges, minres):
        return cls(ranges, minres.asDict(scaled=True))

    @classmethod
    def fromFlatFile(cls, ranges, thefile):
        return cls(ranges, parameter.ppFromFile(thefile, ranges).asDict(scaled=True))


    def __init__(self, ranges=None, center=None, scaler=None):
        self._center = center
        if ranges is not None and center is not None:
            if not self.centerIsInsideRanges():
                raise StandardError("specified center lies outside the cube!")
        if scaler is None:
            logging.warning("creating scaler from cube definition")
            self._scaler=self.createScaler(ranges)
        else:
            self._scaler = scaler
        super(SymmetricHypercube, self).__init__(self.getLargestCube())

    def getCenter(self):
        return self._center

    def createScaler(self, ranges):
        return parameter.Scaler(ranges)

    def centerIsInsideRanges(self):
        """ check whether the scaled specified center is inside the hypercube
            and return True if so.
        """
        def aInside(a):
            if not (a >= 0. and a <= 1.):
                return False
            else:
                return True
        return numpy.array(map(aInside, self.getCenter().values())).all()

    def getClosestDistance(self):
        """ calculate the closest distance (in the scaled world) of the center
            to any of the parameter axes defined via ranges
        """
        center = self.getCenter().values()
        temp = (min(center), min(numpy.ones(len(center)) - center))
        return min(temp)

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
