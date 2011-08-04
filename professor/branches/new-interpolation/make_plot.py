#! /usr/bin/env python

## 
## This program is copyright by Hendrik Hoeth <hoeth@linta.de>. It may be used
## for scientific and private purposes. Patches are welcome, but please don't
## redistribute changed versions yourself.
## 
## $Date: 2008-04-18 11:48:03 +0200 (Fri, 18 Apr 2008) $
## $Revision: 334 $
## 


# TODO:
# - Angabe von manuellen tickmarks und ticklabeln schoener machen.
#   Im Moment ist die Syntax noch eine mit tab getrennte Liste von Wert und Beschriftung


import os
import tempfile
import sys
import getopt
import string
from math import *

class Inputdata:
    def __init__(self, filename):
        self.histos = {}
        self.special = {}
        self.functions = {}
        f = open(filename+'.dat')
        global is2dim
        is2dim=False
        for line in f:
            if (line.count('#',0,1)):
                if (line.count('BEGIN PLOT')):
                    self.read_input(f);
                if (line.count('BEGIN SPECIAL')):
                    self.special[line.split('BEGIN SPECIAL', 1)[1].strip()] = Special(f)
                if (line.count('BEGIN HISTOGRAM')):
                    self.histos[line.split('BEGIN HISTOGRAM', 1)[1].strip()] = Histogram(f)
                if (line.count('BEGIN FUNCTION')):
                    self.functions[line.split('BEGIN FUNCTION', 1)[1].strip()] = Function(f)

        global plotsizex
        global plotsizey
        if self.description.has_key('PlotSize') and self.description['PlotSize']!='':
            plotsizex,plotsizey=self.description['PlotSize'].split(',')
            plotsizex=float(plotsizex)
            plotsizey=float(plotsizey)
        else:
            plotsizex=10.
            plotsizey=6.

        global ratioplotsizey
        if self.description.has_key('RatioPlot') and self.description['RatioPlot']=='1':
            if self.description.has_key('RatioPlotYSize') and self.description['RatioPlotYSize']!='':
                ratioplotsizey=float(self.description['RatioPlotYSize'])
            else:
                ratioplotsizey=3.
        else:
            ratioplotsizey=0.

        global logx
        if self.description.has_key('LogX') and self.description['LogX']=='1':
            logx=True
        else:
            logx=False

        global logy
        if self.description.has_key('LogY') and self.description['LogY']=='1':
            logy=True
        else:
            logy=False

        if self.description.has_key('Stack'):
            foo=[]
            for i in self.description['Stack'].strip().split():
                if i in self.histos.keys():
                    foo.append(i)
            previous=''
            for i in foo:
                if previous!='':
                    self.histos[i].add(self.histos[previous])
                previous=i
        foo=[]
        if self.description.has_key('DrawOnly'):
            for i in self.description['DrawOnly'].strip().split():
                if i in self.histos.keys(): foo.append(i)
        else:
            foo=self.histos.keys()
        self.description['DrawOnly']=foo
    def read_input(self, f):
        self.description = {}
        for line in f:
            if (line.count('#',0,1)):
                if (line.count('END PLOT')):
                    break
            else:
                line = line.rstrip()
                if (line.count('=')):
                    linearray = line.split('=', 1)
                    self.description[linearray[0]] = linearray[1]

class Plot:
    def __init__(self, inputdata):
        pass
    def set_borders(self, inputdata):
        self.set_xmax(inputdata)
        self.set_xmin(inputdata)
        self.set_ymax(inputdata)
        self.set_ymin(inputdata)
        self.set_zmax(inputdata)
        self.set_zmin(inputdata)
    def set_xmin(self,inputdata):
        global xmin
        if inputdata.description.has_key('XMin'):
            xmin = float(inputdata.description['XMin'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getXMin())
            xmin=min(foo)
    def set_xmax(self,inputdata):
        global xmax
        if inputdata.description.has_key('XMax'):
            xmax = float(inputdata.description['XMax'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getXMax())
            xmax=max(foo)
    def set_ymin(self,inputdata):
        global ymin, ymax
        if inputdata.description.has_key('YMin'):
            ymin = float(inputdata.description['YMin'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getYMin(xmin, xmax))
            if is2dim:
                ymin=min(foo)
            else:
                if min(foo) > -1e-4:
                    ymin = 0
                else:
                    ymin = 1.1*min(foo)
                if logy: ymin = max(min(foo)/1.7, 2e-4*ymax)
                if ymin==ymax:
                    ymin-=1
                    ymax+=1
    def set_ymax(self,inputdata):
        global ymax
        if inputdata.description.has_key('YMax'):
            ymax = float(inputdata.description['YMax'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getYMax(xmin, xmax))
            if is2dim:
                ymax=max(foo)
            else:
                if logy:
                    ymax=1.7*max(foo)
                else:
                    ymax=1.1*max(foo)
    def set_zmin(self,inputdata):
        global zmin
        if inputdata.description.has_key('ZMin'):
            zmin = float(inputdata.description['ZMin'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getZMin())
            zmin=min(foo)
    def set_zmax(self,inputdata):
        global zmax
        if inputdata.description.has_key('ZMax'):
            zmax = float(inputdata.description['ZMax'])
        else:
            foo=[]
            for i in inputdata.description['DrawOnly']:
                foo.append(inputdata.histos[i].getZMax())
            zmax=min(foo)
    def draw(self):
        pass
    def write_header(self,inputdata):
        if inputdata.description.has_key('LeftMargin') and inputdata.description['LeftMargin']!='':
            leftmargin=float(inputdata.description['LeftMargin'])
        else:
            leftmargin=1.25
        if inputdata.description.has_key('RightMargin') and inputdata.description['RightMargin']!='':
            rightmargin=float(inputdata.description['RightMargin'])
        else:
            rightmargin=0.35
        if inputdata.description.has_key('TopMargin') and inputdata.description['TopMargin']!='':
            topmargin=float(inputdata.description['TopMargin'])
        else:
            topmargin=0.65
        if inputdata.description.has_key('BottomMargin') and inputdata.description['BottomMargin']!='':
            bottommargin=float(inputdata.description['BottomMargin'])
        else:
            bottommargin=0.95
        papersizex=plotsizex+0.1+leftmargin+rightmargin
        papersizey=plotsizey+ratioplotsizey+0.1+topmargin+bottommargin
        texfile.write('\\documentclass{article}\n')
        if GLOBALOPTIONS['minion']:
            texfile.write('\\usepackage{minion}\n')
        elif GLOBALOPTIONS['mathpazoosf']:
            texfile.write('\\usepackage[osf,sc]{mathpazo}\n')
        else:
            texfile.write('\\usepackage{mathpazo}\n')
        texfile.write('\\usepackage{pst-all}\n')
        texfile.write('\\usepackage{amsmath}\n')
        texfile.write('\\usepackage{relsize}\n')
        texfile.write('\\usepackage[dvips,\n')
        texfile.write('  left=%4.3fcm, right=0cm,\n' %(leftmargin-0.55,))
        texfile.write('  top=%4.3fcm,  bottom=0cm,\n' %(topmargin+0.05,))
        texfile.write('  paperwidth=%scm,paperheight=%scm\n' %(papersizex,papersizey))
        texfile.write(']{geometry}\n')
        texfile.write('\\begin{document}\n')
        texfile.write('\\pagestyle{empty}\n')
        texfile.write('\\SpecialCoor\n')
        texfile.write('\\psset{xunit=%scm,yunit=%scm}\n' %(plotsizex,plotsizey))
        texfile.write('\\begin{pspicture}(0,0)(1,1)\n')
        if is2dim:
            texfile.write('\\definecolorseries{gradientcolors}{hsb}{grad}[rgb]{0,0,1}{-.700,0,0}\n')
            texfile.write('\\resetcolorseries[130]{gradientcolors}\n')
    def write_footer(self):
        texfile.write('\\end{pspicture}\n')
        texfile.write('\\end{document}\n')

class MainPlot(Plot):
    def __init__(self, inputdata):
        self.set_borders(inputdata)
        global coors
        coors = Coordinates()
        self.write_header(inputdata)
        self.draw(inputdata)
    def draw(self,inputdata):
        if inputdata.description.has_key('DrawSpecialFirst') and inputdata.description['DrawSpecialFirst']=='1':
            for i in inputdata.special.keys():
                inputdata.special[i].draw()
            if inputdata.description.has_key('DrawFunctionFirst') and inputdata.description['DrawFunctionFirst']=='1':
                for i in inputdata.functions.keys():
                    inputdata.functions[i].draw()
                for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].draw()
            else:
                for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].draw()
                for i in inputdata.functions.keys():
                    inputdata.functions[i].draw()
        else:
            if inputdata.description.has_key('DrawFunctionFirst') and inputdata.description['DrawFunctionFirst']=='1':
                for i in inputdata.functions.keys():
                    inputdata.functions[i].draw()
                for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].draw()
            else:
                for i in inputdata.description['DrawOnly']:
                    inputdata.histos[i].draw()
                for i in inputdata.functions.keys():
                    inputdata.functions[i].draw()
            for i in inputdata.special.keys():
                inputdata.special[i].draw()
        if inputdata.description.has_key('Legend') and inputdata.description['Legend']=='1':
            legend = Legend(inputdata.description,inputdata.histos,inputdata.functions)
            legend.draw()
        frame = Frame()
        frame.draw()

        if inputdata.description.has_key('XMajorTickMarks') and inputdata.description['XMajorTickMarks']!='':
            xcustommajortickmarks=int(inputdata.description['XMajorTickMarks'])
        else:
            xcustommajortickmarks=-1
        if inputdata.description.has_key('XMinorTickMarks') and inputdata.description['XMinorTickMarks']!='':
            xcustomminortickmarks=int(inputdata.description['XMinorTickMarks'])
        else:
            xcustomminortickmarks=-1
        xcustomticks=[]
        if inputdata.description.has_key('XCustomTicks') and inputdata.description['XCustomTicks']!='':
            FOO=inputdata.description['XCustomTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    xcustomticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        xticks = XTicks()
        if inputdata.description.has_key('RatioPlot') and inputdata.description['RatioPlot']=='1':
            drawlabels=False
        else:
            drawlabels=True
        xticks.draw(custommajortickmarks=xcustommajortickmarks,\
                    customminortickmarks=xcustomminortickmarks,\
                    customticks=xcustomticks,drawlabels=drawlabels)

        if inputdata.description.has_key('YMajorTickMarks') and inputdata.description['YMajorTickMarks']!='':
            ycustommajortickmarks=int(inputdata.description['YMajorTickMarks'])
        else:
            ycustommajortickmarks=-1
        if inputdata.description.has_key('YMinorTickMarks') and inputdata.description['YMinorTickMarks']!='':
            ycustomminortickmarks=int(inputdata.description['YMinorTickMarks'])
        else:
            ycustomminortickmarks=-1
        ycustomticks=[]
        if inputdata.description.has_key('YCustomTicks') and inputdata.description['YCustomTicks']!='':
            FOO=inputdata.description['YCustomTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    ycustomticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        yticks = YTicks()
        yticks.draw(custommajortickmarks=ycustommajortickmarks,\
                    customminortickmarks=ycustomminortickmarks,\
                    customticks=ycustomticks)

        labels = Labels(inputdata.description)
        if inputdata.description.has_key('RatioPlot') and inputdata.description['RatioPlot']=='1':
            labels.draw(['Title','YLabel'])
        else:
            labels.draw(['Title','XLabel','YLabel'])

class RatioPlot(Plot):
    def __init__(self, inputdata):
        if inputdata.description.has_key('RatioPlot') and inputdata.description['RatioPlot']=='1':
            self.refdata=inputdata.description['RatioPlotReference']
            global plotsizey
            plotsizey=ratioplotsizey
            global logy
            logy=False
            if inputdata.description.has_key('RatioPlotYMin'):
                inputdata.description['YMin']=inputdata.description['RatioPlotYMin']
            if inputdata.description.has_key('RatioPlotYMax'):
                inputdata.description['YMax']=inputdata.description['RatioPlotYMax']
            if not inputdata.description.has_key('RatioPlotErrorBandColor'):
                inputdata.description['RatioPlotErrorBandColor']='yellow'
            inputdata.histos[self.refdata].description['ErrorBandColor']=inputdata.description['RatioPlotErrorBandColor']
            inputdata.histos[self.refdata].description['ErrorBands']='1'
            inputdata.histos[self.refdata].description['ErrorBars']='0'
            inputdata.histos[self.refdata].description['LineStyle']='solid'
            inputdata.histos[self.refdata].description['LineColor']='black'
            inputdata.histos[self.refdata].description['LineWidth']='0.3pt'
            inputdata.histos[self.refdata].description['PolyMarker']=''
            self.calculate_ratios(inputdata)
            self.set_borders(inputdata)
            global coors
            coors = Coordinates()
            texfile.write('\n%\n% RatioPlot\n%\n')
            texfile.write('\\psset{yunit=%scm}\n' %(plotsizey))
            texfile.write('\\rput(0,-1){%\n')
            self.draw(inputdata)
            texfile.write('}\n')
        self.write_footer()

    def calculate_ratios(self,inputdata):
        foo=inputdata.description['DrawOnly'].pop(inputdata.description['DrawOnly'].index(self.refdata))
        inputdata.description['DrawOnly'].insert(0,foo)
        for i in inputdata.description['DrawOnly']:
            if i!=self.refdata:
                inputdata.histos[i].divide(inputdata.histos[self.refdata])
        inputdata.histos[self.refdata].divide(inputdata.histos[self.refdata])

    def draw(self,inputdata):
        for i in inputdata.description['DrawOnly']:
            inputdata.histos[i].draw()

        frame = Frame()
        frame.draw()

        if inputdata.description.has_key('XMajorTickMarks') and inputdata.description['XMajorTickMarks']!='':
            xcustommajortickmarks=int(inputdata.description['XMajorTickMarks'])
        else:
            xcustommajortickmarks=-1
        if inputdata.description.has_key('XMinorTickMarks') and inputdata.description['XMinorTickMarks']!='':
            xcustomminortickmarks=int(inputdata.description['XMinorTickMarks'])
        else:
            xcustomminortickmarks=-1
        xcustomticks=[]
        if inputdata.description.has_key('XCustomTicks') and inputdata.description['XCustomTicks']!='':
            FOO=inputdata.description['XCustomTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    xcustomticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        xticks = XTicks()
        xticks.draw(custommajortickmarks=xcustommajortickmarks,\
                    customminortickmarks=xcustomminortickmarks,\
                    customticks=xcustomticks)

        if inputdata.description.has_key('YMajorTickMarks') and inputdata.description['YMajorTickMarks']!='':
            ycustommajortickmarks=int(inputdata.description['YMajorTickMarks'])
        else:
            ycustommajortickmarks=-1
        if inputdata.description.has_key('YMinorTickMarks') and inputdata.description['YMinorTickMarks']!='':
            ycustomminortickmarks=int(inputdata.description['YMinorTickMarks'])
        else:
            ycustomminortickmarks=-1
        ycustomticks=[]
        if inputdata.description.has_key('YCustomTicks') and inputdata.description['YCustomTicks']!='':
            FOO=inputdata.description['YCustomTicks'].strip().split('\t')
            if not len(FOO)%2:
                for i in range(0,len(FOO),2):
                    ycustomticks.append({'Value': float(FOO[i]), 'Label': FOO[i+1]})
        yticks = YTicks()
        yticks.draw(custommajortickmarks=ycustommajortickmarks,\
                    customminortickmarks=ycustomminortickmarks,\
                    customticks=ycustomticks)

        labels = Labels(inputdata.description)
        labels.draw(['XLabel','RatioPlotYLabel'])

class Legend:
    def __init__(self, description, histos, functions):
        self.histos = histos
        self.functions = functions
        self.description = description
    def draw(self):
        texfile.write('\n%\n% Legend\n%\n')
        texfile.write('\\rput[tr]('+self.getLegendXPos()+','+self.getLegendYPos()+'){%\n')
        ypos = -0.05*6/plotsizey
        foo=[]
        if self.description.has_key('LegendOnly'):
            for i in self.description['LegendOnly'].strip().split():
                if i in self.histos.keys() or i in self.functions.keys():
                    foo.append(i)
        else:
            foo=self.description['DrawOnly']+self.functions.keys()

        for i in foo:
            if self.histos.has_key(i):
                drawobject=self.histos[i]
            elif self.functions.has_key(i):
                drawobject=self.functions[i]
            else:
                continue
            title = drawobject.getTitle()
            if title == '':
                continue
            else:
                texfile.write('\\rput[Bl](-0.35,' + str(ypos) + '){' + title + '}\n')
                texfile.write('\\rput[Bl](-0.35,%s){%s\n' %(ypos,'%'))
                if drawobject.getErrorBands():
                    texfile.write('\\psframe[linecolor=%s,fillstyle=solid,fillcolor=%s]' %(drawobject.getErrorBandColor(),drawobject.getErrorBandColor()))
                    texfile.write('(-0.10, 0.033)(-0.02, 0.001)\n')
                texfile.write('\\psline[linestyle=' + drawobject.getLineStyle() \
                            + ', linecolor=' + drawobject.getLineColor() \
                            + ', linewidth=' + drawobject.getLineWidth())
                if drawobject.getLineDash()!='':
                    texfile.write(', dash=' + drawobject.getLineDash())
                if drawobject.getFillStyle()!='none':
                    texfile.write(', fillstyle=' + drawobject.getFillStyle() \
                            + ', fillcolor='  + drawobject.getFillColor() \
                            + ', hatchcolor=' + drawobject.getHatchColor() \
                            + '](-0.10, 0.030)(-0.02, 0.030)(-0.02, 0.004)(-0.10, 0.004)(-0.10, 0.030)\n')
                else:
                    texfile.write('](-0.10, 0.016)(-0.02, 0.016)\n')
                if drawobject.getPolyMarker() != '':
                    texfile.write('  \\psdot[dotstyle=' + drawobject.getPolyMarker() \
                            + ', dotsize='    + drawobject.getDotSize()   \
                            + ', dotscale='   + drawobject.getDotScale()  \
                            + ', linecolor='  + drawobject.getLineColor() \
                            + ', linewidth='  + drawobject.getLineWidth() \
                            + ', linestyle='  + drawobject.getLineStyle() \
                            + ', fillstyle='  + drawobject.getFillStyle() \
                            + ', fillcolor='  + drawobject.getFillColor() \
                            + ', hatchcolor=' + drawobject.getHatchColor())
                    if drawobject.getFillStyle()!='none':
                        texfile.write('](-0.06, 0.028)\n')
                    else:
                        texfile.write('](-0.06, 0.016)\n')
                texfile.write('}\n')
                ypos -= 0.075*6/plotsizey
        if self.description.has_key('CustomLegend'):
            for i in self.description['CustomLegend'].strip().split('\\\\'):
                texfile.write('\\rput[Bl](-0.35,' + str(ypos) + '){' + i + '}\n')
                ypos -= 0.075*6/plotsizey
        texfile.write('}\n')
    def getLegendXPos(self):
        if self.description.has_key('LegendXPos'):
            return self.description['LegendXPos']
        else:
            return '0.98'
    def getLegendYPos(self):
        if self.description.has_key('LegendYPos'):
            return self.description['LegendYPos']
        else:
            return '0.98'
            


class Labels:
    def __init__(self, description):
        self.description = description
    def draw(self, axis=[]):
        texfile.write('\n%\n% Labels\n%\n')
        if self.description.has_key('Title') and (axis.count('Title') or axis==[]):
            texfile.write('\\rput(0,1){\\rput[lB](0, 1.7\\labelsep){\\normalsize '+self.description['Title']+'}}\n')
        if self.description.has_key('XLabel') and (axis.count('XLabel') or axis==[]):
            xlabelsep=4.7
            if self.description.has_key('XLabelSep'):
                xlabelsep=float(self.description['XLabelSep'])
            texfile.write('\\rput(1,0){\\rput[rB](0,-%4.3f\\labelsep){\\normalsize '%(xlabelsep) +self.description['XLabel']+'}}\n')
        if self.description.has_key('YLabel') and (axis.count('YLabel') or axis==[]):
            ylabelsep=5.3
            if self.description.has_key('YLabelSep'):
                ylabelsep=float(self.description['YLabelSep'])
            texfile.write('\\rput(0,1){\\rput[rB]{90}(-%4.3f\\labelsep,0){\\normalsize '%(ylabelsep) +self.description['YLabel']+'}}\n')
        if self.description.has_key('RatioPlotYLabel') and (axis.count('RatioPlotYLabel') or axis==[]):
            ylabelsep=5.3
            if self.description.has_key('YLabelSep'):
                ylabelsep=float(self.description['YLabelSep'])
            texfile.write('\\rput(0,1){\\rput[rB]{90}(-%4.3f\\labelsep,0){\\normalsize '%(ylabelsep) +self.description['RatioPlotYLabel']+'}}\n')

class Special:
    def __init__(self, f):
        self.read_input(f)
    def read_input(self, f):
        self.description = {}
        self.data = []
        for line in f:
            if (line.count('#',0,1)):
                if (line.count('END SPECIAL')):
                    break
            else:
                self.data.append(line)
    def draw(self):
        texfile.write('\n%\n% Special\n%\n')
        for i in range(len(self.data)):
            if self.data[i].count('\\physicscoor'):
                line = self.data[i].split('\\physicscoor')
                self.data[i] = line[0]
                for j in range(1,len(line)):
                    coor = line[j].split(')')[0].lstrip(' (').split(',')
                    self.data[i] +=   '(' + coors.strphys2frameX(float(coor[0])) \
                                    + ',' + coors.strphys2frameY(float(coor[1])) \
                                    + ')' + line[j].split(')',1)[1]
            texfile.write(self.data[i]+'\n')

class DrawableObject:
    def __init__(self, f):
        pass
    def getTitle(self):
        if self.description.has_key('Title'):
            return self.description['Title']
        else:
            return ''
    def getLineStyle(self):
        if self.description.has_key('LineStyle'):
            return self.description['LineStyle']
        else:
            return 'solid'
    def getLineDash(self):
        if self.description.has_key('LineDash'):
            return self.description['LineDash']
        else:
            return ''
    def getLineWidth(self):
        if self.description.has_key('LineWidth'):
            return self.description['LineWidth']
        else:
            return '0.8pt'
    def getLineColor(self):
        if self.description.has_key('LineColor'):
            return self.description['LineColor']
        else:
            return 'black'
    def getFillColor(self):
        if self.description.has_key('FillColor'):
            return self.description['FillColor']
        else:
            return 'white'
    def getHatchColor(self):
        if self.description.has_key('HatchColor'):
            return self.description['HatchColor']
        else:
            return 'black'
    def getFillStyle(self):
        if self.description.has_key('FillStyle'):
            return self.description['FillStyle']
        else:
            return 'none'
    def getPolyMarker(self):
        if self.description.has_key('PolyMarker'):
            return self.description['PolyMarker']
        else:
            return ''
    def getDotSize(self):
        if self.description.has_key('DotSize'):
            return self.description['DotSize']
        else:
            return '2pt 2'
    def getDotScale(self):
        if self.description.has_key('DotScale'):
            return self.description['DotScale']
        else:
            return '1'
    def getErrorBars(self):
        if self.description.has_key('ErrorBars'):
            return bool(int(self.description['ErrorBars']))
        else:
            return False
    def getErrorBands(self):
        if self.description.has_key('ErrorBands'):
            return bool(int(self.description['ErrorBands']))
        else:
            return False
    def getErrorBandColor(self):
        if self.description.has_key('ErrorBandColor'):
            return self.description['ErrorBandColor']
        else:
            return 'yellow'
    def startclip(self):
        texfile.write('\\psclip{\\psframe[linewidth=0, linestyle=none](0,0)(1,1)}\n')
    def stopclip(self):
        texfile.write('\\endpsclip\n')
    def startpsset(self):
        texfile.write('\\psset{linecolor='+self.getLineColor()+'}\n')
        texfile.write('\\psset{linewidth='+self.getLineWidth()+'}\n')
        texfile.write('\\psset{linestyle='+self.getLineStyle()+'}\n')
        texfile.write('\\psset{fillstyle='+self.getFillStyle()+'}\n')
        texfile.write('\\psset{fillcolor='+self.getFillColor()+'}\n')
        texfile.write('\\psset{hatchcolor='+self.getHatchColor()+'}\n')
        if self.getLineDash()!='':
            texfile.write('\\psset{dash='+self.getLineDash()+'}\n')
    def stoppsset(self):
        texfile.write('\\psset{linecolor=black}\n')
        texfile.write('\\psset{linewidth=0.8pt}\n')
        texfile.write('\\psset{linestyle=solid}\n')
        texfile.write('\\psset{fillstyle=none}\n')
        texfile.write('\\psset{fillcolor=white}\n')
        texfile.write('\\psset{hatchcolor=black}\n')

class Function(DrawableObject):
    def __init__(self, f):
        self.read_input(f)
    def read_input(self, f):
        self.description = {}
        self.code='def plotfunction(x):\n'
        iscode=False
        for line in f:
            if (line.count('#',0,1)):
                if (line.count('END FUNCTION')):
                    break
            else:
                if iscode:
                    self.code+='    '+line
                elif (line.count('=')):
                    line = line.rstrip()
                    linearray = line.split('=', 1)
                    if linearray[0]=='Code':
                        iscode=True
                    else:
                        self.description[linearray[0]] = linearray[1]
        if not iscode:
            print '++++++++++ ERROR: No code in function'
    def draw(self):
        self.startclip()
        self.startpsset()
        if self.description.has_key('XMin') and self.description['XMin']!='':
            min=float(self.description['XMin'])
        else:
            min=xmin
        if self.description.has_key('XMax') and self.description['XMax']!='':
            max=float(self.description['XMax'])
        else:
            max=xmax
        dx=(max-min)/500.
        x=min-dx
        texfile.write('\\pscurve')
        while x<(max+2*dx):
            foo=compile(self.code, '<string>', 'exec')
            exec(foo)
            y=plotfunction(x)
            texfile.write('(%s,%s)\n' % (coors.strphys2frameX(x), coors.strphys2frameY(y)))
            x+=dx
        self.stoppsset()
        self.stopclip()

class Histogram(DrawableObject):
    def __init__(self, f):
        self.read_input(f)
    def read_input(self, f):
        self.description = {}
        self.data = []
        for line in f:
            if (line.count('#',0,1)):
                if (line.count('END HISTOGRAM')):
                    break
            else:
                line = line.rstrip()
                if (line.count('=')):
                    linearray = line.split('=', 1)
                    self.description[linearray[0]] = linearray[1]
                else:
                    linearray = line.split('\t')
                    if len(linearray)==4:
                        self.data.append({'LowEdge': float(linearray[0]),
                                          'UpEdge':  float(linearray[1]),
                                          'Content': float(linearray[2]),
                                          'Error':   [float(linearray[3]),float(linearray[3])]})
                    elif len(linearray)==5:
                        self.data.append({'LowEdge': float(linearray[0]),
                                          'UpEdge':  float(linearray[1]),
                                          'Content': float(linearray[2]),
                                          'Error':   [float(linearray[3]),float(linearray[4])]})
                    else:
                        global is2dim
                        is2dim=True
                        self.data.append({'LowEdge': [float(linearray[0]), float(linearray[2])],
                                          'UpEdge':  [float(linearray[1]), float(linearray[3])],
                                          'Content': float(linearray[4]),
                                          'Error':   float(linearray[5])})
        if (self.description.has_key('NormalizeToIntegral') and self.description['NormalizeToIntegral']=='1') or \
           (self.description.has_key('NormalizeToSum') and self.description['NormalizeToSum']=='1'):
            if (self.description.has_key('NormalizeToIntegral') and self.description['NormalizeToIntegral']=='1') and \
               (self.description.has_key('NormalizeToSum') and self.description['NormalizeToSum']=='1'):
                print 'Can\'t normalize to Integral and to Sum at the same time. Will normalize to the Sum.'
            foo = 0
            for i in range(len(self.data)):
                if self.description.has_key('NormalizeToSum') and self.description['NormalizeToSum']=='1':
                    foo += self.data[i]['Content']
                else:
                    foo += self.data[i]['Content']*(self.data[i]['UpEdge']-self.data[i]['LowEdge'])
            for i in range(len(self.data)):
                self.data[i]['Content']  /= foo
                self.data[i]['Error'][0] /= foo
                self.data[i]['Error'][1] /= foo
        if self.description.has_key('Scale') and self.description['Scale']!='':
            for i in range(len(self.data)):
                self.data[i]['Content']  *= float(self.description['Scale'])
                self.data[i]['Error'][0] *= float(self.description['Scale'])
                self.data[i]['Error'][1] *= float(self.description['Scale'])
        if self.description.has_key('Rebin') and self.description['Rebin']!='':
            rebin=int(self.description['Rebin'])
            newdata=[]
            if rebin>=2:
                for i in range(0,(len(self.data)/rebin)*rebin,rebin):
                    foo=0.
                    barl=0.
                    baru=0.
                    for j in range(rebin):
                        foo +=self.data[i+j]['Content']
                        barl+=self.data[i+j]['Error'][0]**2
                        baru+=self.data[i+j]['Error'][1]**2
                    newdata.append({'LowEdge': self.data[i]['LowEdge'],
                                    'UpEdge':  self.data[i+rebin-1]['UpEdge'],
                                    'Content': foo/float(rebin),
                                    'Error':   [sqrt(barl)/float(rebin),sqrt(baru)/float(rebin)]})
                self.data=newdata
    def add(self,name):
        if len(self.data)!=len(name.data):
            print '+++ Error in Histogram.add(): Binning of histograms differs'
        for i in range(len(self.data)):
            if self.data[i]['LowEdge']==name.data[i]['LowEdge'] and \
               self.data[i]['UpEdge']==name.data[i]['UpEdge']:
                self.data[i]['Content'] += name.data[i]['Content']
                self.data[i]['Error'][0] = sqrt(self.data[i]['Error'][0]**2 + name.data[i]['Error'][0]**2)
                self.data[i]['Error'][1] = sqrt(self.data[i]['Error'][1]**2 + name.data[i]['Error'][1]**2)
            else:
                print '+++ Error in Histogram.add(): Binning of histograms differs'
    def divide(self,name):
        if len(self.data)!=len(name.data):
            print '+++ Error in Histogram.divide(): Binning of histograms differs'
        for i in range(len(self.data)):
            if self.data[i]['LowEdge']==name.data[i]['LowEdge'] and \
               self.data[i]['UpEdge']==name.data[i]['UpEdge']:
                # FIXME: Is this kind of error calculation correct?
                try:
                    self.data[i]['Error'][0] /= name.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Error'][0]=0.
                try:
                    self.data[i]['Error'][1] /= name.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Error'][1]=0.
                try:
                    self.data[i]['Content'] /= name.data[i]['Content']
                except ZeroDivisionError:
                    self.data[i]['Content']=1.
#                self.data[i]['Error'][0] = sqrt(self.data[i]['Error'][0]**2 + name.data[i]['Error'][0]**2)
#                self.data[i]['Error'][1] = sqrt(self.data[i]['Error'][1]**2 + name.data[i]['Error'][1]**2)
            else:
                print '+++ Error in Histogram.divide(): Binning of histograms differs'
    def draw(self):
        self.startclip()
        self.startpsset()
        #
        if is2dim:
            for i in range(len(self.data)):
                texfile.write('\\psframe')
                color=int(129*(self.data[i]['Content']-zmin)/(zmax-zmin))
                if self.data[i]['Content']>zmax:
                    color=129
                if self.data[i]['Content']<zmin:
                    color=0
                texfile.write('[linewidth=0pt, fillstyle=solid, fillcolor={gradientcolors!!['+str(color)+']}]')
                texfile.write('(' + coors.strphys2frameX(self.data[i]['LowEdge'][0]) + ', ' \
                                  + coors.strphys2frameY(self.data[i]['LowEdge'][1]) + ')(' \
                                  + coors.strphys2frameX(self.data[i]['UpEdge'][0])  + ', ' \
                                  + coors.strphys2frameY(self.data[i]['UpEdge'][1])  + ')\n')
        else:
            if self.getErrorBars():
                for i in range(len(self.data)):
                    if self.data[i]['Content']==0. and self.data[i]['Error']==[0.,0.]: continue
                    texfile.write('\psline')
                    texfile.write('(' + coors.strphys2frameX(self.data[i]['LowEdge']) + ', ' \
                                      + coors.strphys2frameY(self.data[i]['Content']) + ')(' \
                                      + coors.strphys2frameX(self.data[i]['UpEdge'])  + ', ' \
                                      + coors.strphys2frameY(self.data[i]['Content']) + ')\n')
                    texfile.write('\psline')
                    bincenter = coors.strphys2frameX(.5*(self.data[i]['LowEdge']+self.data[i]['UpEdge']))
                    texfile.write('(' + bincenter + ', ' \
                                      + coors.strphys2frameY(self.data[i]['Content']-self.data[i]['Error'][0]) + ')(' \
                                      + bincenter + ', ' \
                                      + coors.strphys2frameY(self.data[i]['Content']+self.data[i]['Error'][1]) + ')\n')
            else:
                if self.getErrorBands():
                    for i in range(len(self.data)):
                        texfile.write('\\psframe[dimen=outer,linecolor=%s,fillstyle=solid,fillcolor=%s]' %(self.getErrorBandColor(),self.getErrorBandColor()))
                        texfile.write('(' + coors.strphys2frameX(self.data[i]['LowEdge']) + ', ' \
                                          + coors.strphys2frameY(self.data[i]['Content']-self.data[i]['Error'][0]) + ')(' \
                                          + coors.strphys2frameX(self.data[i]['UpEdge'])  + ', ' \
                                          + coors.strphys2frameY(self.data[i]['Content']+self.data[i]['Error'][1]) + ')\n')
                texfile.write('\psline(-0.1,-0.1)\n')
                for i in range(len(self.data)):
                    texfile.write('(' + coors.strphys2frameX(self.data[i]['LowEdge']) + ', ' \
                                      + coors.strphys2frameY(self.data[i]['Content']) + ')(' \
                                      + coors.strphys2frameX(self.data[i]['UpEdge'])  + ', ' \
                                      + coors.strphys2frameY(self.data[i]['Content']) + ')\n')
                texfile.write('(1.1,-0.1)')
        #
        if self.getPolyMarker() != '':
            for i in range(len(self.data)):
                if self.data[i]['Content']==0. and self.data[i]['Error']==[0.,0.]: continue
                texfile.write('\\psdot[dotstyle=%s,dotsize=%s,dotscale=%s](' %(self.getPolyMarker(),self.getDotSize(),self.getDotScale()) \
                              + coors.strphys2frameX(.5*(self.data[i]['LowEdge']+self.data[i]['UpEdge'])) + ', ' \
                              + coors.strphys2frameY(self.data[i]['Content']) + ')\n')
        self.stoppsset()
        self.stopclip()
    def getXMin(self):
        if is2dim:
            return self.data[0]['LowEdge'][0]
        else:
            return self.data[0]['LowEdge']
    def getXMax(self):
        if is2dim:
            return self.data[-1]['UpEdge'][0]
        else:
            return self.data[-1]['UpEdge']
    def getYMin(self, xmin, xmax):
        if is2dim:
            return self.data[0]['LowEdge'][1]
        else:
            yvalues = []
            for i in range(len(self.data)):
                if ((self.data[i]['UpEdge'] > xmin or self.data[i]['LowEdge'] >= xmin) and \
                    (self.data[i]['LowEdge'] < xmax or self.data[i]['UpEdge'] <= xmax)):
                    foo = 0
                    if self.getErrorBars() or self.getErrorBands():
                        foo = self.data[i]['Content']-self.data[i]['Error'][0]
                    else:
                        foo = self.data[i]['Content']
                    if logy:
                        if foo>0: yvalues.append(foo)
                    else:
                        yvalues.append(foo)
            if len(yvalues) > 0:
                return min(yvalues)
            else:
                return self.data[0]['Content']
    def getYMax(self, xmin, xmax):
        if is2dim:
            return self.data[-1]['UpEdge'][1]
        else:
            yvalues = []
            for i in range(len(self.data)):
                if ((self.data[i]['UpEdge'] > xmin or self.data[i]['LowEdge'] >= xmin) and \
                    (self.data[i]['LowEdge'] < xmax or self.data[i]['UpEdge'] <= xmax)):
                    if self.getErrorBars() or self.getErrorBands():
                        yvalues.append(self.data[i]['Content']+self.data[i]['Error'][1])
                    else:
                        yvalues.append(self.data[i]['Content'])
            if len(yvalues) > 0:
                return max(yvalues)
            else:
                return self.data[0]['Content']
    def getZMin(self):
        if not is2dim:
            return 0
        zvalues = []
        for i in range(len(self.data)):
            if (self.data[i]['UpEdge'][0] > xmin and self.data[i]['LowEdge'][0] < xmax) and \
               (self.data[i]['UpEdge'][1] > ymin and self.data[i]['LowEdge'][1] < ymax):
                zvalues.append(self.data[i]['Content'])
        return min(zvalues)
    def getZMax(self):
        if not is2dim:
            return 0
        zvalues = []
        for i in range(len(self.data)):
            if (self.data[i]['UpEdge'][0] > xmin and self.data[i]['LowEdge'][0] < xmax) and \
               (self.data[i]['UpEdge'][1] > ymin and self.data[i]['LowEdge'][1] < ymax):
                zvalues.append(self.data[i]['Content'])
        return max(zvalues)

class Frame:
    def __init__(self):
        self.framelinewidth     = '0.3pt'
    def draw(self):
        texfile.write('\n%\n% Frame\n%\n')
        texfile.write('\\psframe[linewidth='+self.framelinewidth+',dimen=middle](0,0)(1,1)\n')

class Ticks:
    def __init__(self):
        self.majorticklinewidth = '0.3pt'
        self.minorticklinewidth = '0.3pt'
        self.majorticklength    = '9pt'
        self.minorticklength    = '4pt'
    def draw_ticks(self, min, max, plotlog=False, customticks=[], customminortickmarks=-1, custommajortickmarks=-1,drawlabels=True):
        if plotlog:
            x=int(log10(min))
            while (x<log10(max)+1):
                if 10**x>=min:
                    ticklabel=10**x
                    if ticklabel>min and ticklabel<max:
                        self.draw_majorticklabel(ticklabel)
                        self.draw_majortick(ticklabel)
                    if ticklabel==min or ticklabel==max:
                        self.draw_majorticklabel(ticklabel)
                    for i in range(2,10):
                        ticklabel=i*10**(x-1)
                        if ticklabel>min and ticklabel<max:
                            self.draw_minortick(ticklabel)
                x+=1
        elif customticks!=[]:
            for i in range(len(customticks)):
                value=customticks[i]['Value']
                label=customticks[i]['Label']
                if value>=min and value<=max:
                    self.draw_majortick(value)
                    self.draw_majorticklabel(value, label=label)
        else:
            xrange = max-min
            digits = int(log10(xrange))+1
            if (xrange < 1):
                digits -= 1
            foo = int(xrange/(10**(digits-1)))
            if (foo/9. > 0.5):
                tickmarks = 10
            elif (foo/9. > 0.2):
                tickmarks = 5
            elif (foo/9. > 0.1):
                tickmarks = 2

            if (custommajortickmarks>-1):
                if custommajortickmarks not in [1, 2, 5, 10]:
                    print '+++ Error in Ticks.draw_ticks(): MajorTickMarks must be in [1, 2, 5, 10]'
                else:
                    #if custommajortickmarks==1: custommajortickmarks=10
                    tickmarks = custommajortickmarks

            if (tickmarks == 2):
                minortickmarks = 3
            else:
                minortickmarks = 4
            if (customminortickmarks>-1):
                minortickmarks = customminortickmarks
            #
            x = 0
            while (x > min*10**digits):
                x -= tickmarks*100**(digits-1)
            while (x <= max*10**digits):
                if (x >= min*10**digits-tickmarks*100**(digits-1)):
                    ticklabel = 1.*x/10**digits
                    if (int(ticklabel) == ticklabel):
                        ticklabel = int(ticklabel)
                    if (float(ticklabel-min)/xrange >= -1e-5):
                        if (fabs(ticklabel-min)/xrange > 1e-5 and fabs(ticklabel-max)/xrange > 1e-5):
                            self.draw_majortick(ticklabel)
                        if drawlabels:
                            self.draw_majorticklabel(ticklabel)

                    xminor = x
                    for i in range(minortickmarks):
                        xminor += 1.*tickmarks*100**(digits-1)/(minortickmarks+1)
                        ticklabel = 1.*xminor/10**digits
                        if (ticklabel > min and ticklabel < max):
                            if (fabs(ticklabel-min)/xrange > 1e-5 and fabs(ticklabel-max)/xrange > 1e-5):
                                self.draw_minortick(ticklabel)
                x += tickmarks*100**(digits-1)
    def draw(self):
        pass
    def draw_minortick(self, ticklabel):
        pass
    def draw_majortick(self, ticklabel):
        pass
    def draw_majorticklabel(self, ticklabel):
        pass
    def get_ticklabel(self, value, plotlog=False):
        label=''
        if plotlog:
            bar = int(log10(value))
            if bar<0:
                sign='-'
            else:
                sign='\\,'
            if bar==0:
                label = '1'
            else:
                label = '10$^{'+sign+'\\text{'+str(abs(int(log10(value))))+'}}$'
        else:
            if fabs(value) < 1e-8: value=0
            label=str(value)
        return label

class XTicks(Ticks):
    def draw(self, customticks=[], custommajortickmarks=-1, customminortickmarks=-1,drawlabels=True):
        texfile.write('\n%\n% X-Ticks\n%\n')
        texfile.write('\\def\\majortickmarkx{\\psline[linewidth='+self.majorticklinewidth+'](0,0)(0,'+self.majorticklength+')}%\n')
        texfile.write('\\def\\minortickmarkx{\\psline[linewidth='+self.minorticklinewidth+'](0,0)(0,'+self.minorticklength+')}%\n')
        self.draw_ticks(xmin, xmax,\
                        plotlog=logx,\
                        customticks=customticks,\
                        custommajortickmarks=custommajortickmarks,\
                        customminortickmarks=customminortickmarks,drawlabels=drawlabels)
    def draw_minortick(self, ticklabel):
        texfile.write('\\rput('+coors.strphys2frameX(ticklabel)+', 0){\\minortickmarkx}\n')
    def draw_majortick(self, ticklabel):
        texfile.write('\\rput('+coors.strphys2frameX(ticklabel)+', 0){\\majortickmarkx}\n')
    def draw_majorticklabel(self, value, label=''):
        if label=='':
            label=self.get_ticklabel(value,logx)
        texfile.write('\\rput('+coors.strphys2frameX(value)+', 0){\\rput[B](0,-2.3\\labelsep){'+label+'}}\n')

class YTicks(Ticks):
    def draw(self, customticks=[], custommajortickmarks=-1, customminortickmarks=-1):
        texfile.write('\n%\n% Y-Ticks\n%\n')
        texfile.write('\\def\\majortickmarky{\\psline[linewidth='+self.majorticklinewidth+'](0,0)('+self.majorticklength+',0)}%\n')
        texfile.write('\\def\\minortickmarky{\\psline[linewidth='+self.minorticklinewidth+'](0,0)('+self.minorticklength+',0)}%\n')
        self.draw_ticks(ymin, ymax,\
                        plotlog=logy,\
                        customticks=customticks,\
                        custommajortickmarks=custommajortickmarks,\
                        customminortickmarks=customminortickmarks)
    def draw_minortick(self, ticklabel):
        texfile.write('\\rput(0, '+coors.strphys2frameY(ticklabel)+'){\\minortickmarky}\n')
    def draw_majortick(self, ticklabel):
        texfile.write('\\rput(0, '+coors.strphys2frameY(ticklabel)+'){\\majortickmarky}\n')
    def draw_majorticklabel(self, value, label=''):
        if label=='':
            label=self.get_ticklabel(value,logy)
        texfile.write('\\uput[180]{0}(0, '+coors.strphys2frameY(value)+'){'+label+'}\n')

class Coordinates:
    def __init__(self):
        pass
    def phys2frameX(self, x):
        if logx:
            if x>0:
                result = 1.*(log10(x)-log10(xmin))/(log10(xmax)-log10(xmin))
            else:
                return -10
        else:
            result = 1.*(x-xmin)/(xmax-xmin)
        if (fabs(result) < 1e-4):
            return 0
        else:
            return min(max(result,-10),10)
    def phys2frameY(self, y):
        if logy:
            if y>0:
                result = 1.*(log10(y)-log10(ymin))/(log10(ymax)-log10(ymin))
            else:
                return -10
        else:
            result = 1.*(y-ymin)/(ymax-ymin)
        if (fabs(result) < 1e-4):
            return 0
        else:
            return min(max(result,-10),10)
    def strphys2frameX(self, x):
        return str(self.phys2frameX(x))
    def strphys2frameY(self, y):
        return str(self.phys2frameY(y))


####################
def usage():
    print """Usage: make_plot.py [options] file [file2 ...]

Options:
  --help, -h     Show this help.
  --verbose, -v  Be verbose.
  --minion       Use Adobe Minion Pro. Note: You need to set TEXMFHOME before.
  --pdf          Create PDF output instead of PostScript. This usually
                 results in a smaller file size.
  --nocleanup    Keep temporary directory and print its filename.
"""

GLOBALOPTIONS={}
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hv', ['help','verbose','minion','pdf','nocleanup'])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    if len(args)==0:
        usage()
        sys.exit(2)
    GLOBALOPTIONS['verbose']=False
    GLOBALOPTIONS['minion']=False
    GLOBALOPTIONS['pdf']=False
    GLOBALOPTIONS['nocleanup']=False
    GLOBALOPTIONS['mathpazoosf']=not(os.system('kpsewhich ot1pplx.fd > /dev/null'))
    for o, a in opts:
        if o in ['--help', '-h']:
            usage()
            sys.exit()
        if o in ('--verbose', '-v'):
            GLOBALOPTIONS['verbose']=True
        if o=='--pdf':
            GLOBALOPTIONS['pdf']=True
        if o=='--nocleanup':
            GLOBALOPTIONS['nocleanup']=True
        if o=='--minion':
            if os.system('kpsewhich minion.sty > /dev/null')!=0:
                print 'Warning: Using "--minion" requires minion.sty to be installed. Ignoring it.'
            else:
                GLOBALOPTIONS['minion']=True

    for datfile in args:
        filename=datfile.replace('.dat','')

        # create a temporary directory
        oldwdir=os.getcwd()
        tempdir=tempfile.mkdtemp('.make_plot')
        os.chdir(tempdir)
        os.symlink('%s/%s' %(oldwdir, datfile), datfile)

        # do it
        inputdata = Inputdata(filename)
        global texfile
        texfile = open(filename+'.tex', 'w')
        MainPlot(inputdata)
        RatioPlot(inputdata)
        texfile.close()

        # compile the .tex file
        if GLOBALOPTIONS['verbose']:
            os.system('latex '+filename)
            dvips_verbose=''
        else:
            os.system('latex '+filename+' > /dev/null')
            dvips_verbose='-q'
        if GLOBALOPTIONS['minion']:
            dvips_minion='-Pminion'
        else:
            dvips_minion=''
        if GLOBALOPTIONS['pdf']:
            dvips_pdf='-f | ps2pdf - > %s.pdf' %(filename)
        else:
            dvips_pdf=''
        os.system('dvips %s %s %s %s' %(dvips_verbose,dvips_minion,filename,dvips_pdf))

        # clean up
        if GLOBALOPTIONS['pdf']:
            os.system('cp %s.pdf %s/' %(filename, oldwdir))
        else:
            os.system('cp %s.ps %s/' %(filename, oldwdir))
        os.chdir(oldwdir)
        if GLOBALOPTIONS['nocleanup']:
            print 'keeping temp-files in %s' %(tempdir)
        else:
            for i in os.listdir(tempdir):
                os.unlink('%s/%s' %(tempdir, i))
            os.rmdir(tempdir)

if __name__ == '__main__':
    main()
