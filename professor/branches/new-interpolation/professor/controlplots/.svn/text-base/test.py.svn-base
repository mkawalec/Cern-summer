"""ttt.py

"""
import numpy
from os import *
from professor.histo import *
from professor.controlplots import *

# data collecting part, modify path as needed
h = getHistolist('test'
        , 'dummy') # path, name of observable
m = makePackage(h)

# envelope plot part - this already works
e = envelope.Envelope(h, mc=False)
#e.plotEnvelope(e.getTube()) # plots the envelope
#e.plotErrorbars(e.getAll(), e.getSmallestStep()) # adds errorbars
#e.plotPolygon(e.getAll(), e.getSmallestStep()) # plots polygons
#e.Show() # show previously plotted things, make legend etc...

# sensitivity part - needs plotting and normalization features
s = sensitivity.Sensitivity(m)

print 'calculated sensitivities\n bin|parameter|{Run:Sensitivity}'
alls = {}
for par in s._params:
    temp = []
    if s.par_hasChanged(par):
        for bin in s._histdata[s._p0run]['Bins'].keys():
            temp.append( (.5*(bin[1]-bin[0]), numpy.array(s.getSensitivity(bin, par))))
        alls[par] = numpy.array(temp)
print alls
            # print bin, par, s.getSensitivity(bin, par)
