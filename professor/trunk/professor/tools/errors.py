"""Module used to define error types raised by Professor code.
"""

class ProfessorError(Exception):
    pass


class ArgumentError(ProfessorError):
    pass


class DataProxyError(ProfessorError):
    pass


class MinimizerError(ProfessorError):
    pass


class ValidationFailed(ProfessorError):
    pass


class ResultError(ProfessorError):
    pass


class IOTestFailed(ProfessorError):
    pass


class WeightError(ProfessorError):
    pass


class FixedSortedKeysError(ProfessorError):
    pass


class ParameterError(FixedSortedKeysError):
    pass


class InterpolationError(ProfessorError):
    """Base class for all errors during interpolation."""
    pass


class InterpolationFailedError(InterpolationError):
    """Raise this if an interpolation has invalid coefficients/coeff errors.

    The constructor takes error message and bin id as arguments.
    """
    def __init__(self, message, binid):
        super(InterpolationError, self).__init__(message)
        self.binid = binid
