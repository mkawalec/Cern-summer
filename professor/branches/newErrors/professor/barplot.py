#! /usr/bin/env python 
"""barplot.py

this script creates barplots out of ASCII-files using PAIDA

it is intended to display (1D) parameter optimization results in dependence
on the number of runs used for the creation of bin distributions

usage example for a result file 'results.txt':

    python barplot.py results.txt
    or
    python barplot.py results.txt True

the latter will generate an .eps-file
"""
import os, sys, random
from paida import IAnalysisFactory
from pylab import load

class BarPlot:
    def __init__(self, filename, runs = [4,20, 300]):
        self._runs = runs
        self._header, self._data, self._associate = self.parseFile(filename)
        self.analysisFactory = IAnalysisFactory.create()
        self.treeFactory = self.analysisFactory.createTreeFactory()
        self.tree = self.treeFactory.create()
        ### Creating histograms.
        self.histogramFactory = self.analysisFactory.createHistogramFactory(self.tree)

    def lSplit(self, line):
        """ this is to properly tokenize header lines """
        return line.split('#')[1].strip().split(':')

    def stringIt(self, alist):
        """ this is to properly write data lines into temporary file """
        string = ''
        for token in alist:
            string = string + token + '        '
        return string

    def parseFile(self, filename):
        """ parse a file, read header lines into dictionary, loads data into array """
        header = {}
        X = open(filename, 'r')
        temp = open('justatempfile', 'w') # this file is deleted a few lines later
        i = 1
        associate = {}
        for line in X:
            if line.startswith('#'):
                if self.lSplit(line)[0] == 'parameter':
                    header[self.lSplit(line)[1].split()[0]] = map(float, self.lSplit(line)[1].split()[1:])
                    associate[self.lSplit(line)[1].split()[0]] = i
                    i = i + 1
            elif line.startswith(' '):
                continue
            else:
                temp.write(self.stringIt(line.split()[1:])+'\n')
        temp.close()
        data  = load('justatempfile')
        os.system('rm justatempfile')
        X.close()
        return header, data, associate


    def getBoinks(self):
        xbins = []
        for i in self._data[:,0]:
            if not i in xbins:
                xbins.append(i)
        entriesX = {}
        for i in xbins:
            totalx = [j for j in self._data[:,0] if j == i]
            entriesX[str(i)] = len(totalx)
        return entriesX

    def getRanges(self, parameter):
        """ returns parameters needed for histogram creation """
        # X-ranges
        xmin = self._runs[0]
        xmax = self._runs[1]
        nx = xmax - xmin
        # Y-ranges
        ny = self._runs[-1]
        ymin = self._header[parameter][0]
        ymax = self._header[parameter][1]
        return nx, xmin, xmax, ny, ymin, ymax

    def buildPlot(self, parameter):
        """ this creates and fills histogram objects """
        r = self.getRanges(parameter)
        self.h2dF = self.histogramFactory.createHistogram2D(str(parameter), 'fitresults', *r)

        # filling histo with data
        Xentries = []
        weight = self.getBoinks()
        for entry in self._data:
            self.h2dF.fill(entry[0], entry[self._associate[parameter]])#, float(weight[str(entry[0])]))

        ##for xbin in xrange(self.h2dF._sizeX - 2):
        ##    Xentries.append(self.h2dF.binEntriesX(xbin))
        ##print Xentries
        #self.h2dF_t = self.histogramFactory.createHistogram2D(str(parameter), 'fitresults', *r)
        #self.c2d  = self.histogramFactory.createCloud2D('unlimited', 'Unlimited')
        ## filling histo with data
        #Xentries = []
        #for entry in self._data:
        #    self.h2dF_t.fill(entry[0], entry[self._associate[parameter]])
        #    # self.c2d.fill(entry[0], entry[self._associate[parameter]])
        #for xbin in xrange(self.h2dF_t._sizeX - 2):
        #    Xentries.append(self.h2dF_t.binEntriesX(xbin))
        #print Xentries

        #tempdict = {}
        #for i, boink in enumerate(self.getBoinks()):
        #    tempdict[str(boink)] = Xentries[i]
        ## reset histo and fill again but now normed
        ## self.h2dF.reset()
        #self.h2dF = self.histogramFactory.createHistogram2D(str(parameter), 'fitresults', *r)
        #for entry in self._data:
        #    self.h2dF.fill(entry[0], entry[self._associate[parameter]/tempdict[str(entry[0])]])

        self.plotterFactory = self.analysisFactory.createPlotterFactory()
        self.plotter = self.plotterFactory.create('fitresults for ' + parameter)
        self.plotter.createRegions(2, 1)

    def plotBarAndBox(self, parameter):
        """ this will create a bar and box plot """
        # self.buildPlot(parameter)
        for i, value in enumerate(['bar', 'box']):
            self.plotter.region(i).setTitle(value + ' format')
            self.plotter.region(i).style().setParameter('showTitle', 'true')
            self.plotter.region(i).style().dataStyle().setParameter('histogram2DFormat', value)
            self.plotterStyle = self.plotter.region(i).style()
            self.xAxisStyle = self.plotterStyle.xAxisStyle()
            self.xAxisStyle.setLabel('# of runs used for interpolation')
            self.yAxisStyle = self.plotterStyle.yAxisStyle()
            self.yAxisStyle.setLabel('parameter')
            self.xAxisStyle.setParameter('grid', 'true')
            self.plotter.region(i).plot(self.h2dF)


def main(filename, print2file=False):
   bp = BarPlot(filename, [4,20,300])
   for i in bp._header.keys():
       bp.buildPlot(i)
       # bp.plotScatter(i) # not working very well
       bp.plotBarAndBox(i)
       if print2file:
           temp = str(random.randint(1,9999))
           bp.plotter.writeToFile('out_' + i + temp + '.eps')
           print 'image saved as out_' + i + temp + '.eps'
   dummy = raw_input('Hit any key.')


if __name__=="__main__":
   if len(sys.argv) == 2:
       main(sys.argv[1])
   elif len(sys.argv) ==3:
       main(sys.argv[1], sys.argv[2])
   else:
       raise StandardError('too few/less arguments given!')

#filename = sys.argv[1]
#bp = BarPlot(filename, [4,20,300])
#for i in bp._header.keys():
#    bp.buildPlot(i)
#    # bp.plotScatter(i) # not working very well
#    bp.plotBarAndBox(i)
#    #if print2file:
#    #    temp = str(random.randint(1,9999))
#    #    bp.plotter.writeToFile('out_' + i + temp + '.eps')
#    #    print 'image saved as out_' + i + temp + '.eps'
#dummy = raw_input('Hit any key.')


