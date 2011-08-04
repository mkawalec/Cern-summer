"""
Thin wrapper module for importing an interactive Python shell for use as a UI in
scripts. This module isn't (and probably shouldn't be!) available via professor.user.
"""

from professor.tools import log

def usePrettyTraceback():
    try:
        from IPython.Shell import IPShellEmbed
        ipshell = IPShellEmbed([])
    except:
        log.debug("ipython traceback not available.")
