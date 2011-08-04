from professor.tools.errors import FixedSortedKeysError


class NEWFixedSortedKeys(object):
    """
    Simple container for a list of constant, sorted index identifiers,
    typically parameter names.

    The interface consists of a `keys` and a `dim` attribute and two methods:
    * `getIndex()` to search for the index of a key
    * `goodPartner()` to check that another object is compatible with this
      one.
    """
    def _init_keys(self, keys):
        self._keys = tuple(sorted(keys))
        self._dim = len(keys)

    @property
    def keys(self):
        return self._keys


    @property
    def dim(self):
        return self._dim
    size = dim


    def getIndex(self, key):
        return indexOf(self.keys, key)


    def goodPartner(self, candidate):
        if self.keys != candidate.keys:
            raise FixedSortedKeysError("Key names differ: %s != %s !" %
                                       (self.keys, candidate.keys))
        return True



class FixedSortedKeys(object):
    """
    Stores given keys in a sorted list.
    """

    def __init__(self, indices):
        """
        @param indices: list with unique keys.
        @type indices: C{list}
        @raise TypeError: If indices is not a list.
        @raise ValueError: If indices are not unique.
        """
        if type(indices) != list:
            raise TypeError("Argument indices must be a list!")
        if len(set(indices)) != len(indices):
            raise ValueError("Indices must be unique!")
        self._keys = indices[:]
        self._keys.sort()



    def getIndex(self, key):
        """Return the index of given key."""
        return self.getKeys().index(key)
    index = getIndex


    def getKeys(self):
        """Return the stored keys (sorted, of course)."""
        return self._keys
    keys = property(getKeys)


    ## Make sub-classes a bit more dict-like
    iterkeys = getKeys


    @property
    def size(self):
        """Return number of stored keys."""
        return len(self._keys)


    def goodPartner(self, candidate):
        """Check if self and candidate have the same keys."""
        if not self.getKeys() == candidate.getKeys():
            raise FixedSortedKeysError("Keys differ: %s != %s !" %
                                       (self.keys, candidate.keys))
        return True


    def __str__(self):
        return "FixedSortedKeys:\n    %s\n" % self.keys


    def __len__(self):
        """
        Return the number of keys.

        For subclasses like ParameterPoint or BinDistribution it returns the
        number of parameters aka the dimension of the tuning.
        """
        return len(self.getKeys())

    dim = __len__
