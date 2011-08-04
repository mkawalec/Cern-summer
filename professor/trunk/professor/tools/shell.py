"""
Thin wrapper module for importing an interactive Python shell for use as a UI in
scripts. This module isn't (and probably shouldn't be!) available via professor.user.
"""

from professor.tools import log

# TODO: Perhaps this is a bit of an overkill for mainly having just a nicer
# trace back. Instead we can split this and use IPython.ultraTB.(...) for
# trace backs.
def usePrettyTraceback():
    """Use IPython's pretty trace back.

    If you want to use the IPython shell later, you can use::

        ipshell = usePrettyTraceback()
        [...]
        ipshell()

    If the IPython import failed the returned ipshell is a no-op and just
    logs an error message.

    Returns
    -------
    ipshell
        IPython shell for later use.
    """
    try:
        from IPython.Shell import IPShellEmbed
        ipshell = IPShellEmbed([])
        return ipshell
    except:
        log.debug("ipython traceback not available.")
        def ipshell(*args, **kwargs):
            log.error("IPython shell not available!")
        return ipshell


def setProcessName(name):
    """Set the process name."""
    try:
        import ctypes
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        libc.prctl(15, name, 0, 0, 0)
    except Exception:
        log.debug("Failed to set process name")
