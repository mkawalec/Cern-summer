"""Library with useful method/function decorators:

virtualmethod
=============
A little tool to make interface definition and inheritance easier. Allows
completely virtual methods like in C++:

C{  virtual void func(...) = 0;  }

Usage example:

    >>> class Super:
    ...    @virtualmethod
    ...    def virt(arg1, arg2):
    ...        pass
    ...
    >>>
    >>> class Sub(Super):
    ...     def virt(arg1, arg2):
    ...         pass
    ...
    >>> mum = Super()
    >>> daughter = Sub()
    >>> mum.virt(1, 2)
    [...]
    VirtualMethodError: virtual method "virt" called!

deprecated
==========
Use this if you want to log a deprecation method with warning priority
everytime a function is called.

Usage:

    >>> def new(*args, **kwargs):
    >>>     pass
    >>>
    >>> @deprecated(new)
    >>> def old(*args, **kwargs):
    >>>     pass
    >>> old(foo, bar)
    >>> # some warning log

or:
    >>> @deprecated("newfunction")
    >>> def oldname(*args, **kwargs):
    >>>     pass
    >>> old(foo, bar)
    >>> # some warning log

"""


from professor.tools import log as logging


class VirtualMethodError(Exception):
    pass


def virtualmethod(f):
    """Descriptor function for virtual methods.

    Returns a function always raising a L{VirtualMethodError} when called.
    """
    def r(*args, **kwargs):
        # classmethod- and staticmethod-objects don't have a func_name
        # property!
        if hasattr(f, 'func_name'):
            raise VirtualMethodError('virtual method "%s" called!'%(
                f.func_name))
        else:
            raise VirtualMethodError('virtual method "%s" called!'%(f))
    return r


def deprecated(arg=None):
    """Throw a warning everytime an old function is called.

    If the deprecated decorator gets a string argument it treats it as the
    name of the new function that replaces the deprecated one.

    Parameters
    ----------
        arg : str,callable
            The new function name, if it's a string.
            Usage:
                >>> @deprecated("new function name")
                ... def f(foo, bar):
                [...]

            The old function, if it's not a string.
            Usage:
                >>> @deprecated
                ... def f(foo, bar):
                [...]

    TODO: The code might be clearer if the decorator was a callable class
          rather than a function with many nested sub-functions.
    """
    if arg is None:
        arg = "new function"

    if type(arg) == str:
        # This decorator is the function that is actually called with the
        # old function as argument.
        def decorator(old):
            # This function is called by the old name.
            # Wraps around new and generates a log warning.
            def wrapped(*args, **kwargs):
                logging.warning("Using deprecated callable '%s'. Use '%s' instead!" % (old.func_name, arg))
                return old(*args, **kwargs)
            return wrapped
        return decorator
    else:
        def wrapped(*args, **kwargs):
            logging.warning("Using deprecated callable '%s'. Use 'new function'"
                             " instead!" % (arg.func_name))
            return arg(*args, **kwargs)
        return wrapped
