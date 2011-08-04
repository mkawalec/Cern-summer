from numpy import *
import pylab as pl
import sys, re

if len(sys.argv) < 2:
    sys.exit(1)
filename = sys.argv[1]
name = re.sub(r'\.dat$', '', filename)

data = zeros((12,38), dtype=float)
f = file(filename, "r")
for line in f:
    vals = line.split()
    xindex = int(round(12*(float(vals[1]) - 0.1)/(0.65 - 0.1 + 0.05)))
    yindex = int(round(38*(float(vals[0]) - 1.5)/(20.0 - 1.5 + 0.5)))
    #print vals[0], xindex, vals[1], yindex, int(yindex), int(round(yindex))
    data[xindex, yindex] = float(vals[2])
f.close()
#print data

## If we want a black background
if False:
    pl.rc('text', usetex=False, color="white")
    pl.rc('axes', edgecolor="white", labelcolor="white")
    pl.rc('savefig', facecolor="black")
    pl.rc('xtick', color="white")
    pl.rc('ytick', color="white")


pl.hold(True)    
pl.imshow(data, aspect=1.5*20.0/0.65, origin="lower", interpolation="nearest", extent=[1.5, 20.0, 0.1, 0.65])
pl.colorbar()
#pl.contourf(data, aspect=1.5*20.0/0.65, linewidths=2.0, origin="lower", extent=[1.5, 20.0, 0.1, 0.65])


#pl.title("Fit $\chi^2$ with Pythia shower params")
pl.ylabel("PARJ(81) / GeV")
pl.xlabel("PARJ(82) / GeV")


## Output
pl.jet()
pl.savefig(name + "-jet.eps")
pl.gray()
pl.savefig(name + "-grey.eps")
pl.hot()
pl.savefig(name + "-hot.eps")


## Other formats
#pl.savefig(name + ".png")
#pl.savefig(name + ".pdf")
#pl.savefig(name + ".svg")
#pl.show()
