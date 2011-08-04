import itertools

from professor.minimize.result import ResultList
# from professor.tools.errors import ResultError
# import professor.tools.log as logging
from professor.tools.stringtools import latexEscape


# TODO: put this somewhere else?
def updateFigure(reslist, fignum=None):
    """Create/update a matplotlib figure with all GoF vs. parameter plots.

    This is a convenience function for use inside a IPython session.
    """
    from matplotlib import pyplot
    plotter = ParameterScatterPlotter([reslist], ["numruns","startpoint"])
    numplots = len(plotter.parameternames)
    numcols = 2
    numrows = numplots/2
    if numplots%numcols != 0:
        numrows += 1

    # TODO: is this if ... else ... necessary?
    if fignum is None:
        f = pyplot.figure()
    else:
        f = pyplot.figure(fignum)
    f.clear()
    for i, n in enumerate(plotter.parameternames):
        sub = f.add_subplot(numrows, numcols, i+1)
        plotter.plotParamChi2MPL(sub, n, True)
        sub.set_xlabel(n)
    return f


# TODO: rename this to "KebabPlotter" ;)
class ParameterScatterPlotter(dict):
    """Class to create GoF vs. parameter estimate scatter plots."""
    def __init__(self, resultlists, dflags=None, labeledresults=()):
        """Plot the chi2-param values for all results in resultlists in sub.

        Parameters
        ----------
        resultlists : list of ResultList instances
            Lists with the results that will be plotted. Generally the items
            of `resultlists` can be any sequence-type that contains
            :class:`Result` objects.
        dflags : list of str, optional
            List with the  categories that will be plotted with different
            styles. the plot. Accepted categories are:

                * numruns
                * startpoint (startpoint method)
                * limits (limits used in minimisation)

            The results are grouped by color in the first given category.
        labeledresults : list of pairs, optional
            ("label", result) pairs to plot in addition to the results in
            `resultlists`, e.g. to mark previous tunings.
        """
        if dflags is None:
            dflags = []
        # build diffkey->plotdata dictionary
        for result in itertools.chain(*resultlists):
            key = ""
            for flag in dflags:
                if flag == "numruns":
                    key += "%i:" % (len(result.runs))
                elif flag == "startpoint":
                    key += "%s:" % (result.startpointmethod)
                elif flag == "limits":
                    key += "%s:" % (result.limitedparameters)
            if not self.has_key(key):
                label = ""
                for flag in dflags:
                    if flag == "numruns":
                        # label += "Runs:%i" % (len(result.runs))
                        label += "$N_\mathrm{runs} = %i$" % (len(result.runs))
                    elif flag == "startpoint":
                        label += " (%s)" % (result.startpointmethod)
                    elif flag == "limits":
                        if len(result.limitedparameters):
                            label += "(limited)"
                        else:
                            label += "(not limited)"
                self[key] = ({"label":label, "linestyle":''}, ResultList())
            self[key][1].append(result)
        # fill plotstyles
        # Cannot use StyleGen here because we loop through colours and
        # markers independently.
        # colcycle = itertools.cycle(['k', 'r', 'b', 'g'])
        colcycle = itertools.cycle(['r', 'k', 'b', 'g'])
        markcycle = itertools.cycle(['o', 'x', 'v', '+', '^', '*'])
        if len(self.keys()) > 1:
            # key => color
            colordict = {}
            # currentcolorkey = None
            # currentcolor = None
            # for key in sorted(self.keys(), key=lambda k: k.split(":")[0]):
            for key, val in self.sortedItems():
                colorkey = key.split(":")[0]
                try:
                    color = colordict[colorkey]
                except KeyError:
                    color = colcycle.next()
                    colordict[colorkey] = color

                # if colorkey != currentcolorkey:
                    # currentcolorkey = colorkey
                    # currentcolor = colcycle.next()
                marker = markcycle.next()
                self[key][0]["color"] = color
                self[key][0]["marker"] = marker
        else:
            self.values()[0][0]["color"] = 'k'
            self.values()[0][0]["marker"] = 'o'

        self.labeledresults = labeledresults

    def plotParamChi2MPL(self, sub, param, ndof, ranges=None):
        """Plot GoF vs. parameter values in a matplotlib Axes.

        Parameters
        ----------
        sub : matplotlib Axes instance
        param : str
            The parameter name to plot.
        ndof : bool
            Plot chi2/Ndof on the y axis instead of plain chi2.
        ranges : ParameterRange, optional
            The sampling boundaries.
        """
        minx = 1.0e15
        miny = 1.0e15
        maxx = -1.0e15
        maxy = -1.0e15
        # for (kwargs, results) in self.itervalues():
        for (kwargs, results) in reversed(self.sortedValues()):
            pindex = results[0].getIndex(param)
            chi2s = []
            params = []
            for res in results:
                if ndof:
                    chi2s.append(res.gof)
                else:
                    chi2s.append(res.gof*res.ndof)
                params.append(res.values[pindex])
            minx = min(minx, min(params))
            maxx = max(maxx, max(params))
            miny = min(miny, min(chi2s))
            maxy = max(maxy, max(chi2s))
            sub.plot(params, chi2s, **kwargs)

        if ranges is not None:
            low = ranges[param][0]
            high = ranges[param][1]
            minx = min(minx, low)
            maxx = max(maxx, high)
            sub.axvline(x=low, linestyle = ":", color = "g")
            sub.axvline(x=high, linestyle = ":", color = "g",
                        label = "Sampling boundaries")

        for label, result in self.labeledresults:
            annotateargs = {"xytext" : (20, 0),
                            "textcoords" : "offset points",
                            "arrowprops" : {"arrowstyle" : "->"}}
            x = result.values[param]
            if ndof:
                y = result.gof
            else:
                y = result.gof * result.ndof
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
            sub.annotate(label, (x, y), **annotateargs)

        # update x-, y-limits
        minx -= 0.1*(maxx-minx)
        maxx += 0.1*(maxx-minx)
        miny -= 0.1*(maxy-miny)
        maxy += 0.1*(maxy-miny)
        sub.set_xlim((minx, maxx))
        sub.set_ylim((miny, maxy))

        # set axes labels
        sub.set_xlabel(param)
        if ndof:
            sub.set_ylabel(r"$\chi^2/N_\mathrm{df}$")
        else:
            sub.set_ylabel(r"$\chi^2$")


        return (minx, maxx, miny, maxy)

    # map matplotlib styles to make-plots
    mplcolor2makeplots = {"r" : "red", "b":"blue", "k":"black"}
    mplmarker2makeplots = { "o" : "*", "x" : "x", "+":"+", "^":"hexagon",
                            "*" : "BoldAsterisk", "v":"triangle*"}

    def plotParamChi2MakePlots(self, param, ndof, samplebounds=None):
        """Plot GoF vs. parameter values suitable for make-plots.

        Parameters
        ----------
        param : str
            The parameter name to plot.
        ndof : bool
            Plot chi2/Ndof on the y axis instead of plain chi2.
        samplebounds : ParameterRange
            The sampling boundaries.

        Returns
        -------
        String suitable as file input for make-plots.
        """
        minx = 1.0e15
        miny = 1.0e15
        maxx = -1.0e15
        maxy = -1.0e15
        nl = "\n"

        plots = []
        idx = 1
        for (kwargs, results) in reversed(self.sortedValues()):
            marker = self.mplmarker2makeplots.get(kwargs["marker"], "*")
            color = self.mplcolor2makeplots.get(kwargs["color"], "gray")

            plotname = "scatter-%i" % (idx)
            idx += 1

            pindex = results[0].getIndex(param)
            chi2s = []
            params = []
            for res in results:
                if ndof:
                    chi2s.append(res.gof)
                else:
                    chi2s.append(res.gof*res.ndof)
                params.append(res.values[pindex])
            minx = min(minx, min(params))
            maxx = max(maxx, max(params))
            miny = min(miny, min(chi2s))
            maxy = max(maxy, max(chi2s))
            tmp = nl + "# BEGIN HISTOGRAM " + plotname + nl
            tmp += "Title=" + kwargs["label"] + nl
            tmp += "ErrorBars=0" + nl + "PolyMarker=" + marker + nl
            tmp += "LineStyle=none" + nl
            tmp += "LineColor=" + color + nl
            for gof, par in zip(chi2s, params):
                tmp += "%e\t%e\t%e\t0\n" % (par, par, gof)
            tmp += "# END HISTOGRAM" + nl
            plots.append((plotname, tmp))
        if samplebounds is not None:
            minx = min(minx, samplebounds[param][0])
            maxx = max(maxx, samplebounds[param][1])
        minx -= 0.1*(maxx-minx)
        maxx += 0.1*(maxx-minx)
        miny -= 0.1*(maxy-miny)
        maxy += 0.1*(maxy-miny)

        pname = r"$\mathtt{" + latexEscape(param) + "}$"
        s = "# BEGIN PLOT" + nl + "LogY=0" + nl
        s += "Title=Result scatter for " + pname + nl
        s += "XLabel=" + pname + nl
        s += r"YLabel=$\chi^2/N_\mathrm{df}$" + nl
        s += "XMin=" + str(minx) + nl
        s += "XMax=" + str(maxx) + nl
        s += "YMin=" + str(miny) + nl
        s += "YMax=" + str(maxy) + nl
        s += "Legend=1" + nl
        s += "LegendXPos=0.55" + nl
        s += "ConnectGaps=0" + nl
        s += "DrawOnly=" + " ".join([i[0] for i in plots])
        if samplebounds is not None:
            s += " boundaries boundarieslabel"
        s += nl + "# END PLOT" + nl
        for plotname, plot in plots:
            s += plot
        if samplebounds is not None:
            s += nl + "# BEGIN HISTOGRAM boundarieslabel" + nl
            s += "Title=Sampling boundaries" + nl
            s += "LineStyle=dashed" + nl
            s += "LineWidth=1.2pt" + nl
            s += "LineColor=green!60!black" + nl
            s += "%i\t%i\t%i\t%i\n" % (0,0,0,0)
            s += "# END HISTOGRAM" + nl
            s += nl + "# BEGIN SPECIAL boundaries" + nl
            s += r"\psline[linewidth=1.2pt,linestyle=dashed,"
            s +=          "linecolor=green!60!black]"
            s += "\physicscoor(%s,%s)\physicscoor(%s,%s)" % (
                        samplebounds[param][0], miny, samplebounds[param][0], maxy)
            s += nl
            s += "\psline[linewidth=1.2pt,linestyle=dashed,"
            s +=         "linecolor=green!60!black]"
            s += "\physicscoor(%s,%s)\physicscoor(%s,%s)" % (
                        samplebounds[param][1], miny, samplebounds[param][1], maxy)
            s += nl + "# END SPECIAL" + nl
        return s

    def sortedValues(self):
        """Return self.values() sorted by the length of the result list."""
        return sorted(self.itervalues(), key=lambda val: len(val[1]))
                # operator.itemgetter(1))

    def sortedItems(self):
        "Return (key, value) pairs sorted by the length of the result list."
        return sorted(self.iteritems(), key=lambda item: len(item[1][1]))

    def getParameterNames(self):
        result = self.values()[0][1][0]
        return result.names
    parameternames = property(getParameterNames)

    def getMaxRunsValue(self, param):
        """Return the common estimate for param of the maximal runs results.

        Raises a ValueError if the estimates or covariance matrix differ too much.
        """
        maxruns = 0
        maxresults = None
        for kwargs, rlist in self.values():
            if max(rlist.getRunCounts()) > maxruns:
                maxruns = max(rlist.getRunCounts())
                maxresults = rlist.getMaxRunsResults()
            elif max(rlist.getRunCounts()) == maxruns:
                maxresults.extend(rlist.getMaxRunsResults())
        if maxruns <= 0 or len(maxresults) == 0:
            raise ValueError("No max runs result found!")

        # check that results are comparable:
        #   relative diff < 0.05
        #   diff of covariance matrix < 1e-5
        normvalues = maxresults[0].values
        for rtest in maxresults[1:]:
            if (abs( (rtest.values - normvalues)/normvalues ) > 0.05).any():
                raise ValueError("Results differ relatively by more than 0.05!")
            #TODO: rewrite after covariances are added again.
            # try:
                # if (abs(rnorm.getCovMatrix()
                    # - rtest.getCovMatrix()) > 1e-5).any():
                    # raise ValueError("Covariance matrices differ by more"
                                     # " than 1.0e-5!")
            # except ResultError, err:
                # logging.warn("Could not compare covariance matrices:"
                             # " %s" % (err))

        return normvalues[param]
