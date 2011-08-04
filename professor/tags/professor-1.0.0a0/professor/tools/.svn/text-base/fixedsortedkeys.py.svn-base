from professor.tools.errors import FixedSortedKeysError

## TODO: Split into professor.tools
class FixedSortedKeys(object):
    """Stores given keys in a sorted list."""
    def __init__(self, indices):
        """
        @param indices: list with unique keys.
        @type indices: C{list}
        @raise TypeError: If indices is not a list.
        @raise ValueError: If indices are not unique.
        """
        if type(indices) != list:
            raise TypeError("argument indices must be a list!")

        if len(set(indices)) != len(indices):
            raise ValueError("indices must be unique!")
        self._keys = indices[:]
        self._keys.sort()

    def getIndex(self, key):
        """Return the index of given key."""
        return self.getKeys().index(key)

    def getKeys(self):
        """Return the stored keys."""
        return self._keys
    # something to make sub-classes more dict-like
    keys = getKeys
    iterkeys = getKeys

    def goodPartner(self, candidate):
        """Check if self and candidate have the same keys."""
        if not self.getKeys() == candidate.getKeys():
            raise FixedSortedKeysError("keys differ: %s != %s !" % (
                    self.getKeys(), candidate.getKeys()))
        return True

    def __str__(self):
        return "FixedSortedKeys:\n    %s\n"%(self._keys)

    def __len__(self):
        """Return the number of keys.

        For subclasses like ParameterPoint or BinDistribution it returns the
        number of parameters aka the dimension of the tuning.
        """
        return len(self.getKeys())

    dim = __len__
