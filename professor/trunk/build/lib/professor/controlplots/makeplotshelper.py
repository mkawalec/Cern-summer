"""
makeplotshelper.py

    * Helper functions for creating input files for make-plots

"""

from professor.tools.decorators import deprecated

@deprecated(r"""use '"\t".join(["%e" % x for x in data]) + "\n"' instead""")
def get2DHisto(data):
    """ Data has to be a six-tuple with the following ordering:
        (lowerxbinedge, upperxbinedge, lowerybinedge, upperybinedge, value)
        The error will be ignored when plotting and is therefore set to 0
    """
    histo = ""
    for dp in data:
        histo+="%s\t%s\t%s\t%s\t%s\t0.0\n"%(dp[0], dp[1], dp[2], dp[3], dp[4])
    return histo
