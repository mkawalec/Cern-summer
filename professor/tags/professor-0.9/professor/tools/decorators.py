"""decorators.py

Library with useful method/function decorators:

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

    >>> def newname(*args, **kwargs):
    >>>     pass
    >>>
    >>> @deprecated(newname)
    >>> def oldname(*args, **kwargs):
    >>>     pass
    >>> oldname(foo, bar)
    >>> # some warning log

or:

    >>> def newname(*args, **kwargs):
    >>>     pass
    >>> oldname = deprecated(newname)()
    >>> oldname(foo, bar)
    >>> # some warning log
"""

import logging
import types


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

def deprecated(new):
    # handle, that static/class methods are not callable but you have to
    # use the *.__get__ method
    if type(new) == staticmethod:
        new = new.__get__(object)
        wrapchange = staticmethod
    elif type(new) == classmethod:
        new = new.__get__(object).im_func
        wrapchange = classmethod
    else:
        wrapchange = lambda f: f

    def decorator(old):
        # This function is called by the old name.
        # Wraps around new and generates a log warning.
        def wrapper(*args, **kwargs):
            logging.warning("Using deprecated method '%s'. Use '%s'"
                             # " instead!"%(old, new))
                             " instead!"%(old.func_name, new.func_name))
            return new(*args, **kwargs)

        # copy doc string
        wrapper.__doc__ = "Deprecated function '%s' use '%s' instead!"%(
                          # old, new)
                          old.func_name, new.func_name)
        if new.__doc__ is not None:
            wrapper.__doc__ += '\n' + new.__doc__

        return wrapchange(wrapper)

    return decorator
