"""
Some routines for drawing histograms.
"""

def plotRootHistogram(h, title='', xlabel='', ylabel='', logy=False, dogaussfit=False, filename=None):
    """Plot a ROOT-histogram 'h' and fit a gauss to it.

    This function depends on ROOT and on my plotting scripts which you can
    find at http://www.linta.de/~hoeth/d0/make_plot/
    I've put a copy of histplotter.py in trunk/professor/tools/ and a copy
    of make_plot.py in trunk/ .
    """
    import professor.tools.histplotter as histplotter
    if filename is None:
        filename = title
    hist = histplotter.Histogram(h.GetTitle(), h)
    hist.SetTitle('')
    plot = histplotter.Plot()
    plot.AddHistogram(hist)
    plot.SetLegend(True)
    plot.SetLegendXPos(0.5)
    plot.SetTitle(title.replace('_','\\_').replace('^','\\^{}').replace('$','\\$').replace('#','\\#').replace('%','\\%'))
    plot.SetXLabel(xlabel)
    plot.SetYLabel(ylabel)
    plot.SetLogY(logy)
    if dogaussfit:
        h.Fit("gaus","LQ")
        a = h.GetFunction("gaus").GetParameter(0)
        b = h.GetFunction("gaus").GetParameter(1)
        c = h.GetFunction("gaus").GetParameter(2)
        #ea = h.GetFunction("gaus").GetParError(0)
        eb = h.GetFunction("gaus").GetParError(1)
        ec = h.GetFunction("gaus").GetParError(2)
        func = histplotter.Function('gaus', 'return %s*exp(-0.5*((x-%s)/%s)**2)' % (a, b, c))
        func.SetTitle('mean=%3.2f${}\pm{}$%3.2f, sigma=%3.2f${}\pm{}$%3.2f' % (b, eb, c, ec))
        func.SetLineColor('red')
        plot.AddFunction(func)
    plot.Save('fig_%s.dat' % (filename.replace(' ', '_')))
