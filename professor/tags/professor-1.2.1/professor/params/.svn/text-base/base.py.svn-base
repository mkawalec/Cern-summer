import re
from operator import indexOf
import numpy

from professor.tools import sorting


class ParameterBase(numpy.ndarray):
    """Base class for name-value kind of containers.

    Factory functions for easy instance creation are:
        * :meth:`mkFromDict`
        * :meth:`mkFromFile`

    The constructor takes two arguments:

        names : array_like
            The parameter names.
        values : array_like
            The parameter values.

    """
    scanparamtag = "PROF_SCAN_PARAM"
    # Note: This code is mostly copied from the subclassing.py.gz
    # documentation.
    def __new__(cls, names, values, scanparam=None):
        """Create a new instance from lists of names and associated values.

        Parameters
        ----------
        names : array_like
            The parameter names.
        values : array_like
            The parameter values.

        Raises
        ------
        ValueError
            If `names` and `values` have incompatible length.
        """
        # print "=== Creating new %s" % (cls)
        # print names
        # print values
        names = numpy.asarray(names)
        values = numpy.asarray(values)
        if names.shape[0] != values.shape[0]:
            raise ValueError("Different number of parameter names and values!")
        # print "==="
        # print "+++"
        # print names
        # print values
        # print values.shape
        # print "+++"

        # Sort `values` by the order of parameters in `names`.
        idx = numpy.argsort(names)
        # print idx
        # print "==="
        # print names[idx]
        # print values[idx]
        # print values[idx].shape
        # print "==="
        # print names
        # print values
        names = names[idx]
        values = values[idx]
        values = numpy.asarray(values).view(type=cls)
        # print "+++"
        # print values
        # print type(values)
        # print "+++"

        values._parameter_names = tuple(names)
        values._dim = len(names)
        values.scanparam = scanparam
        return values


    def __array_finalize__(self, obj):
        # print "Finalizing ParameterBase"
        self._parameter_names = getattr(obj, "_parameter_names", None)
        self._dim = getattr(obj, "_dim", None)
        self.scanparam = getattr(obj, "scanparam", None)


    @classmethod
    def mkFromFile(cls, path):
        """Load parameters from a file.

        Parameters
        ----------
        path : str
            The path of the file.
        """
        f = open(path)
        names, values, scanparam = cls._parselines(f)
        f.close()
        return cls(names, values, scanparam)


    @classmethod
    def _parselines(cls, lines):
        """Parse a sequence/iterator of lines.

        Parameters
        ----------
        lines : iterator of strings, e.g. a ``file`` object.
            The strings to parse.
        Returns
        -------
        rnames : list of strings
            The parameter names
        rvals : list of list of floats, list of floats
            (Nested) list of parameter values.
        scanparam : float, None
            The value of the 'PROF_SCAN_PARAM' tag used e.g. in line scans.
            If no such tag is found, ``None`` is returned.
        """
        rnames = []
        rvals = []
        scanparam = None
        numpar = 0
        # Keep the origline for useful error messages.
        for origline in lines:
            l = re.sub(r'(^.*?)#.*', r'\1', origline) # strip comments
            l = l.replace("=", " ")
            l = l.strip()
            if len(l) == 0:
                continue
            tokens = l.split()
            name = tokens[0]
            vals = map(float, tokens[1:])
            if numpar == 0:
                numpar = len(vals)
            if numpar != len(vals):
                raise ValueError("Number of parameter values differ from"
                                 " previous lines at line"
                                 " '%s'" % (origline[:-1]))

            # convert single values to floats
            if len(vals) == 1:
                vals = vals[0]

            # treat PROF_SCAN_PARAM special
            if name != cls.scanparamtag:
                rnames.append(name)
                rvals.append(vals)
            else:
                scanparam = vals
        return rnames, rvals, scanparam


    @classmethod
    def mkFromDict(cls, d):
        """Create an instance from a dictionary.

        Parameters
        ----------
        d : dict
            For 1D parameter data, e.g. parameter points
            `d` must have the form::

                d = {"PAR1" : val1, "PAR2" : val2 }

            for other data types, e.g. parameter errors and ranges::

                d = {"PAR1" : [val1, val2],
                     "PAR2" : [val3, val4] }

            In principle nesting is allowed, resulting in 3+ dimensional
            arrays.
        """
        names = []
        values = []
        scanparam = None
        for n, v in d.items():
            if n != "PROF_SCAN_PARAM":
                names.append(n)
                values.append(v)
            else:
                scanparam = v
        return cls(names, values, scanparam)


    # Overwrite this if you need to.
    def format(self, cmp_=sorting.cmpByInt, sep="  "):
        """Format parameter names and values.

        The default format is::

            Par1  val1  val2  ...
            Par2  ...

        Numbers are formatted using `%e`.

        Parameters
        ----------
        cmp_ : function, optional
            Comparison function used to sort parameter names with the
            builtin `sorted` function. By default
            :func:`professor.tools.sorting.cmpByInt` is used to sort
            parameter names by a contained number. Use `None` to preserve
            the order of :attr:`~self.names`
        sep : str, optional
            String used to separate parameter names and values.
            [default: two spaces]
        """
        w = max(map(len, self.names))
        s = ""
        for n in sorted(self.names, cmp=cmp_):
            i = self.getIndex(n)
            s += n.ljust(w) + sep
            s += sep.join(["%e" % (x) for x in self[i]])
            s += "\n"
        if self.scanparam is not None:
            s += "PROF_SCAN_PARAM%s%e\n" % (sep, self.scanparam)
        return s[:-1]


    def __str__(self):
        return self.format(cmp_=None)


    def writeParamFile(self, path, cmp_=sorting.cmpByInt):
        """Write the return value of :meth:`format` to a file."""
        f = open(path, "w")
        f.write(self.format(cmp_=cmp_) + "\n")
        f.close()


    @property
    def names(self):
        """The parameter names.

        Warnings
        --------
        The names are stored in an `numpy.ndarray` as instances of `numpy.string_`.
        """
        return self._parameter_names


    def keys(self):
        """Get the parameter names.

        Implemented for dict-like behaviour::

            >>> d = dict()
            >>> params = ParameterBase(["a", "z"], [1.3, 9e4])
            >>> d.update(params)
            >>> d
            {'a' : 1.3, 'z' : 90000.0}
        """
        return self.names


    @property
    def dim(self):
        return self._dim


    def getIndex(self, name):
        """Return the index of parameter `name`."""
        return indexOf(self.names, name)


    # Note: We have to overwrite both __getitem__ and __getslice__, although
    # __getslice__ is marked as deprecated in the Python documentation!
    def __getitem__(self, idx):
        """x.__getitem__(idx) <==> x[idx]

        Using parameter names as single index is supported. Slicing with
        parameter names is not supported.

        Returns
        -------
        ret
            If `idx` is a slice object the returned object has the same type
            as this. In all other cases, a simple `np.ndarray` or item type
            is returned.
        """
        if isinstance(idx, str):
            idx = self.getIndex(idx)
        elif type(idx) == slice:
            names = self.names[idx]
            values = numpy.asarray(self)[idx]
            return type(self)(names, values)

        return numpy.asarray(self)[idx]


    def __getslice__(self, a, b):
        return self.__getitem__(slice(a,b))


    def __setitem__(self, idx, val):
        """x.__setitem__(idx, val) <==> x[idx] = val

        Using parameter names as single index is supported. Slicing with
        parameter names is not supported.
        """
        if isinstance(idx, str):
            idx = self.getIndex(idx)
        numpy.ndarray.__setitem__(self, idx, val)


    def asDict(self):
        """Convert the data to dict.

        The keys are the parameter names the values the stored numerical
        data.

        The resulting dictionary is suitable to create a new instance with
        :meth:`~ParameterBase.mkFromDict`.
        """
        return dict(zip(self.names, self))


    # Implement the pickle protocol
    # see: http://mail.scipy.org/pipermail/numpy-discussion/attachments/20070415/ebf0a380/attachment.py
    def __reduce__(self):
        obj_state = list(numpy.ndarray.__reduce__(self))
        sub_state = (self._parameter_names, self._dim, self.scanparam)
        obj_state[2] = (obj_state[2], sub_state)
        return tuple(obj_state)


    def __setstate__(self, state):
        nd_state, own_state = state
        numpy.ndarray.__setstate__(self, nd_state)
        names, dim, scanparam = own_state

        self._parameter_names = names
        self._dim = dim
        self.scanparam = scanparam



class ParameterPoint(ParameterBase):
    def __new__(cls, names, values, scanparam=None):
        obj = ParameterBase.__new__(cls, names, values, scanparam)
        if len(obj.shape) != 1:
            raise ValueError("Parameter point must be of shape (dim,)!")
        return obj

    # TODO: Check that functions as default args work.
    def format(self, cmp_=sorting.cmpByInt, sep="  "):
        """Format parameter names and values

        The format is::
            Par1  val1
            Par2  val2
            ...

        Numbers are formatted using `%e`.

        Parameters
        ----------
        cmp_ : function, optional
            Comparison function used to sort parameter names with the
            builtin `sorted` function. By default
            :func:`professor.tools.sorting.cmpByInt` is used to sort
            parameter names by a contained number.
        sep : str, optional
            String used to separate parameter names and values.
            [default: two spaces]
        """
        d = self.asDict()
        w = max(map(len, d.keys()))
        s = ""
        for k in sorted(d.keys(), cmp=cmp_):
            s += "%s%s%e\n" % (k, sep, d[k])
        if self.scanparam is not None:
            s += "PROF_SCAN_PARAM  %e\n" % (self.scanparam)
        return s[:-1]

    @classmethod
    def mkFromString(cls, s):
        """Create an instance from a string.

        Typical use-case is parsing of command line option.

        Parameters
        ----------
        s : str
            A string with parameter names and values of the form
            `"Name1=Val1,Name2=Val2"`.
        """
        names = []
        values = []
        for partok in s.split(","):
            n, v = partok.split("=")
            v = float(v)
            names.append(n)
            values.append(v)
        return cls(names, values)



class ParameterErrors(ParameterBase):
    def __new__(cls, names, values, scanparam=None):
        if scanparam is not None:
            raise ValueError("ParameterErrors does not accept argument scanparam!")
        obj = ParameterBase.__new__(cls, names, values)
        if len(obj.shape) != 2 or obj.shape[1] != 2:
            raise ValueError("Parameter errors must be of shape (dim, 2)!")

        return obj

    def __getitem__(self, idx):
        """
        Specialised to allow ["Param", "low"/"high"] indexing.
        """
        if (type(idx) == tuple and len(idx) == 2 and
                isinstance(idx[0], str) and isinstance(idx[1], str)):
            t0 = self.getIndex(idx[0])
            if idx[1] == "low":
                t1 = 0
            elif idx[1] == "high":
                t1 = 1
            else:
                raise ValueError("Second index must be 'low' or 'high' for"
                                 " indexing by string!")
            idx = (t0, t1)
        return super(ParameterErrors, self).__getitem__(idx)



class ParameterMatrix(ParameterBase):
    """Class for parameter-parameter matrix data, e.g. correlations.

    An instance can be easily created from a dictionary with
    :meth:`~ParameterMatrix.mkFromDict`.

    The item look-up is modified to allow to specifiy the matrix cell by two
    paramater names::

        >>> d = { ("PAR1", "PAR1") : 11 ,
        ... ("PAR1", "PAR2") : 12 ,
        ... ("PAR2", "PAR1") : 21 ,
        ... ("PAR2", "PAR2") : 22 }
        >>> matrix = ParameterMatrix.mkFromDict(d)
        >>> matrix["PAR1", "PAR2"]
        12.0
        >>> matrix["PAR1", "PAR2"] = 120
        >>> matrix["PAR1", "PAR2"]
        120.0
    """
    def __new__(cls, names, values, scanparam=None):
        if scanparam is not None:
            raise ValueError("ParameterMatrix does not accept argument scanparam!")
        obj = ParameterBase.__new__(cls, names, values)
        if obj.shape != (obj._dim, obj._dim):
            raise ValueError("Parameter matrix must be of shape (dim, dim)!")

        return obj

    @classmethod
    def mkFromDict(cls, d):
        """
        Parameters
        ----------
        d : dict
            A mapping of tuples of parameter names on matrix values, e.g.::

                d = { ("PAR1", "PAR1") : val_11 ,
                      ("PAR1", "PAR2") : val_12 ,
                      ("PAR2", "PAR1") : val_21 ,
                      ("PAR2", "PAR2") : val_22 }
        """
        # get all parameter names, with python magic, yeehah ;)
        # see: http://paddy3118.blogspot.com/2007/02/unzip-un-needed-in-python.html
        n1, n2 = zip(*d.keys())
        n1 = sorted(set(n1))
        n2 = sorted(set(n2))
        # make sure that the same names were used as first and second
        # indices
        if n1 != n2:
            raise ValueError("List of parameter names in keys of `d` differ!")
        names = n1
        values = numpy.nan * numpy.empty((len(names), len(names)))
        for i, name_i in enumerate(names):
            for j, name_j in enumerate(names):
                values[i,j] = d[name_i, name_j]
        return cls(names, values)

    def asDict(self):
        d = {}
        for i in self.names:
            for j in self.names:
                # __getitem__ can handle (name1, name2) look-ups
                d[i, j] = self[i,j]
        return d

    def __getitem__(self, idx):
        """
        Specialised to allow ["Param1", "Param2"] indexing.
        """
        if (type(idx) == tuple and len(idx) == 2 and
                isinstance(idx[0], str) and isinstance(idx[1], str)):
            t0 = self.getIndex(idx[0])
            t1 = self.getIndex(idx[1])
            idx = (t0, t1)
        # TODO: treat slicing specially
        # elif type(idx) == slice:

        return super(ParameterMatrix, self).__getitem__(idx)

    def __setitem__(self, idx, val):
        """
        Specialised to allow ["Param1", "Param2"] indexing.
        """
        if (type(idx) == tuple and len(idx) == 2 and
                isinstance(idx[0], str) and isinstance(idx[1], str)):
            t0 = self.getIndex(idx[0])
            t1 = self.getIndex(idx[1])
            idx = (t0, t1)

        return super(ParameterMatrix, self).__setitem__(idx, val)



class ParameterRange(ParameterBase):
    """Container for parameter ranges.

    Range definitions are stored as low and high bounds for each parameter.
    I.e. a range is given by two parameter points.

    Possible use cases are:
        * Ranges of anchor points that are used for an interpolation.
        * Ranges for random point sampling.
        * Ranges for line-scan point sampling. The line is given by the
          diagonal stretching between the two corner points of the parameter
          range.

    Warnings
    --------
    The :attr:`low` and :attr:`high` properties contain the corners of the parameter
    range. They will not always fulfill :math:`low < high`. This is especially
    the case with line scans.


    Examples
    --------
    Create a parameter range and sample randomly from it. Parameter "Par1" is
    in [0.0, 1.0], "Par2" in [3.5, 3.6]::

        >>> range_ = ParameterRange(["Par1", "Par2"], [[0.0, 1.0], [3.5, 3.6]])
        >>> # Get a 2D random point in [0.0, 1.0].
        >>> rndpoint = np.random.rand(2)
        >>> # Convert it to the cube defined by range_
        >>> range_.getRelativePoint(rndpoint)

    Create a parameter range and sample along the diagonal, as one would do
    for a line scan::

        >>> range_ = ParameterRange(["Par1", "Par2"], [[0.0, 1.0], [3.5, 3.6]])
        >>> for rel in np.linspace(0.0, 1.0, 10, endpoint=True):
        >>>     print range_.getRelativePoint(rel)
        # some out put

    or get the same points in one numpy.ndarray::

        >>> relative = np.linspace(0.0, 1.0, 10, endpoint=True)
        >>> range_.getRelativePoint(relative[:,np.newaxis], plainarray=True)
        array([[ 0.        ,  3.5       ],
               [ 0.11111111,  3.51111111],
               [ 0.22222222,  3.52222222],
               [ 0.33333333,  3.53333333],
               [ 0.44444444,  3.54444444],
               [ 0.55555556,  3.55555556],
               [ 0.66666667,  3.56666667],
               [ 0.77777778,  3.57777778],
               [ 0.88888889,  3.58888889],
               [ 1.        ,  3.6       ]])
    """
    def __new__(cls, names, values, scanparam=None):
        if scanparam is not None:
            raise ValueError("ParameterRange does not accept argument scanparam!")
        obj = ParameterBase.__new__(cls, names, values)
        if len(obj.shape) != 2 or obj.shape[1] != 2:
            raise ValueError("Parameter range must be of shape (dim, 2)!")

        return obj


    @classmethod
    def mkFromPoints(cls, points):
        """Create a parameter range spanned by a list of points.

        The range is then defined by the min/max values in each direction.

        Parameters
        ----------
        points : list of :class:`ParameterPoint` instances
        """
        pmin = points[0]
        pmax = points[0]
        for p in points:
            pmin = numpy.minimum(p, pmin)
            pmax = numpy.maximum(p, pmax)
        return cls(pmin.names, zip(pmin, pmax))


    @classmethod
    def mkFromString(cls, s):
        """Create an instance from a string.

        Typical use-case is parsing of command line option.

        Parameters
        ----------
        s : str
            A string with parameter names and values of the form
            `"Name1=Low1=High1,Name2=Low2=High2"`.
        """
        names = []
        values = []
        for partok in s.split(","):
            n, low, high = partok.split("=")
            low = float(low)
            high = float(high)
            names.append(n)
            values.append((low, high))
        return cls(names, values)


    @property
    def center(self):
        """Calculate the center of the spanned hyper cube.

        Returns
        -------
        center : ParameterPoint
        """
        return self.getRelativePoint(0.5)


    def getRelativePoint(self, x, plainarray=False):
        """Transform normalised `x` to ranges.

        `x` is expected to have normalised values. Values of `x[i] = 0.0`
        and `x[i] = 1.0 correspond to the first and second corner of the
        parameter range, respectively.

        This can be useful to construct random points from this parameter range::

            >>> range_.getRelativePoint(np.random.rand(pr.dim))

        Parameters
        ----------
        x : array_like
        plainarray : bool, optional
            If `True` do not cast the returned value back to a
            :class:`ParameterPoint`. Useful if `x` has shape (1, numpoints).
            The returned array has then shape (dim, numpoints).
            The defalt is to return a :class:`ParameterPoint` instance.

        Returns
        -------
        new : ParameterPoint, ndarray
            A ndarray is returned if `plainarray` is `True`.
        """
        new = self.low + (self.high - self.low)*x
        if plainarray:
            return numpy.asarray(new)
        if type(new) != ParameterPoint:
            new = ParameterPoint(self.names, new)
        return new


    def getNormalisedPoint(self, x, plainarray=False):
        """Transform `x` to normalised coordinates in ranges.

        If `x` is inside the ranges the returned values will be between 0
        and 1. This is the inverse function of :meth:`getRelativePoint`.

        Parameters
        ----------
        x : array_like
        plainarray : bool
            Do not cast the returned value back to a ParameterPoint.
            Useful if `x` has shape (1, numpoints). The returned array has
            then shape (dim, numpoints).

        Returns
        -------
        new : ParameterPoint, ndarray
            A ndarray is returned if `plainarray` is set.
        """
        new = (x - self.low)/(self.high - self.low)
        if not plainarray and type(new) != ParameterPoint:
            new = ParameterPoint(self.names, new)
        return new


    @property
    def diagonal(self):
        """Calculate the diagonal of the spanned hyper cube.

        Returns
        -------
        diag : ParameterPoint
        """
        diag = self[:,1] - self[:,0]
        return ParameterPoint(self.names, diag)


    @property
    def low(self):
        return ParameterPoint(self.names, self[:,0])


    @property
    def high(self):
        return ParameterPoint(self.names, self[:,1])


    def isInside(self, point):
        """Return True if point is inside the ranges."""
        l = self.min(axis=1)
        h = self.max(axis=1)
        return (l <= point).all() and (point <= h).all()



if __name__ == "__main__":
    p1 = "/home/eike/projects/professor/forNAF/sherpa-pt-wide3.params"
    p2 = "/home/eike/projects/professor/forNAF/2010-05-21-flav9/000/used_params"
    try:
        pr = ParameterRange.mkFromFile(p1)
        print "range:", pr
        print "names:", pr.names
    except Exception, err:
        print "!!ERR:", err
    print

    try:
        pp1 = ParameterPoint.mkFromFile(p1)
        print "point1:", pp1
        print "names:", pp1.names
    except Exception, err:
        print "!!ERR(expected):", type(err), err
    print

    try:
        pp2 = ParameterPoint.mkFromFile(p2)
        print "point2:", pp2
        print "names:", pp2.names
    except Exception, err:
        print "!!ERR:", err
