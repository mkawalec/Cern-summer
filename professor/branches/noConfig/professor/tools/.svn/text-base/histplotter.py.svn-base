## 
## This program is copyright by Hendrik Hoeth <hoeth@linta.de>. It may be used
## for scientific and private purposes. Patches are welcome, but please don't
## redistribute any changed versions yourself.
## 
## $Date: 2007-08-22 06:37:38 +0200 (Wed, 22 Aug 2007) $
## $Revision: 312 $

## TODO:
##   - ErrorBands, ErrorBandColor


import ROOT
import array

class DrawableObject:
    def __init__(self,id):
        self.properties={}
        self.properties['id']=id
        self.properties['Comment']=[]
        self.properties['Title']=None
        self.properties['LineStyle']=None
        self.properties['LineColor']=None
        self.properties['LineWidth']=None
        self.properties['LineDash']=None
        self.properties['FillStyle']=None
        self.properties['FillColor']=None
        self.properties['HatchColor']=None
    def SaveDrawableObject(self,file):
        for i in self.properties['Comment']:
            file.write(i)
        if self.GetTitle()!=None:
            file.write('Title=%s\n' %(self.GetTitle()))
        if self.GetLineStyle()!=None:
            file.write('LineStyle=%s\n' %(self.GetLineStyle()))
        if self.GetLineColor()!=None:
            file.write('LineColor=%s\n' %(self.GetLineColor()))
        if self.GetLineWidth()!=None:
            file.write('LineWidth=%s\n' %(self.GetLineWidth()))
        if self.GetLineDash()!=None:
            file.write('LineDash=%s\n' %(self.GetLineDash()))
        if self.GetFillStyle()!=None:
            file.write('FillStyle=%s\n' %(self.GetFillStyle()))
        if self.GetFillColor()!=None:
            file.write('FillColor=%s\n' %(self.GetFillColor()))
        if self.GetHatchColor()!=None:
            file.write('HatchColor=%s\n' %(self.GetHatchColor()))
    def AddCommentLine(self,foo):
        self.properties['Comment'].append('# %s\n' %(foo))
    def SetTitle(self,foo):
        self.properties['Title']=str(foo)
    def SetLineStyle(self,foo):
        self.properties['LineStyle']=str(foo)
    def SetLineColor(self,foo):
        self.properties['LineColor']=str(foo)
    def SetLineWidth(self,foo):
        self.properties['LineWidth']=str(foo)
    def SetLineDash(self,foo):
        self.properties['LineDash']=str(foo)
    def SetFillStyle(self,foo):
        self.properties['FillStyle']=str(foo)
    def SetFillColor(self,foo):
        self.properties['FillColor']=str(foo)
    def SetHatchColor(self,foo):
        self.properties['HatchColor']=str(foo)
    def GetId(self):
        return self.properties['id']
    def GetTitle(self):
        return self.properties['Title']
    def GetLineStyle(self):
        return self.properties['LineStyle']
    def GetLineColor(self):
        return self.properties['LineColor']
    def GetLineWidth(self):
        return self.properties['LineWidth']
    def GetLineDash(self):
        return self.properties['LineDash']
    def GetFillStyle(self):
        return self.properties['FillStyle']
    def GetFillColor(self):
        return self.properties['FillColor']
    def GetHatchColor(self):
        return self.properties['HatchColor']


class Histogram(DrawableObject):
    def __init__(self,id,hist):
        DrawableObject.__init__(self,id)
        self.hist=hist
        self.properties['is2dim']=bool(self.hist.InheritsFrom('TH2'))
        self.properties['Title']=self.hist.GetTitle()
        self.properties['PolyMarker']=None
        self.properties['DotSize']=None
        self.properties['DotScale']=None
        self.properties['ErrorBars']=False
        self.properties['NormalizeToIntegral']=False
        self.properties['NormalizeToSum']=False
        self.properties['Scale']=1
        self.properties['Rebin']=1
    def Save(self,file):
        file.write('# BEGIN HISTOGRAM %s\n' %(self.GetId()))
        self.SaveDrawableObject(file)
        if self.GetPolyMarker()!=None:
            file.write('PolyMarker=%s\n' %(self.GetPolyMarker()))
        if self.GetDotSize()!=None:
            file.write('DotSize=%s\n' %(self.GetDotSize()))
        if self.GetDotScale()!=None:
            file.write('DotScale=%s\n' %(self.GetDotScale()))
        if self.GetErrorBars():
            file.write('ErrorBars=1\n')
        if self.GetNormalizeToIntegral():
            file.write('NormalizeToIntegral=1\n')
        if self.GetNormalizeToSum():
            file.write('NormalizeToSum=1\n')
        if self.GetScale()!=1:
            file.write('Scale=%s\n' %(self.GetScale()))
        if self.GetRebin()!=1:
            file.write('Rebin=%s\n' %(self.GetRebin()))
        #
        if self.GetIs2dim():
            # FIXME: not yet supported
            pass
        else:
            if self.GetIsGraph():
                x=array.array('d')
                y=array.array('d')
                ex=array.array('d')
                ey=array.array('d')
                if self.hist.Class().GetName()=='TGraphErrors':
                    x=self.hist.GetX()
                    y=self.hist.GetY()
                    ex=self.hist.GetEX()
                    ey=self.hist.GetEY()
                    for i in range(self.hist.GetN()):
                        file.write('%s\t%s\t%s\t%s\n' %(x[i]-ex[i],x[i]+ex[i],y[i],ey[i]))
                else:
                    x=self.hist.GetX()
                    y=self.hist.GetY()
                    for i in range(self.hist.GetN()):
                        file.write('%s\t%s\t%s\t%s\n' %(x[i],x[i],y[i],'0'))
            else:
                for i in range(1,self.hist.GetNbinsX()+1):
                    file.write('%s\t%s\t%s\t%s\n' %(self.hist.GetBinLowEdge(i), \
                                                    self.hist.GetBinLowEdge(i)+self.hist.GetBinWidth(i), \
                                                    self.hist.GetBinContent(i), \
                                                    self.hist.GetBinError(i)))
        file.write('# END HISTOGRAM\n\n')
    def SetPolyMarker(self,foo):
        self.properties['PolyMarker']=str(foo)
    def SetDotSize(self,foo):
        self.properties['DotSize']=str(foo)
    def SetDotScale(self,foo):
        self.properties['DotScale']=float(foo)
    def SetErrorBars(self,foo):
        self.properties['ErrorBars']=bool(foo)
    def SetNormalizeToIntegral(self,foo):
        self.properties['NormalizeToIntegral']=bool(foo)
    def SetNormalizeToSum(self,foo):
        self.properties['NormalizeToSum']=bool(foo)
    def SetScale(self,foo):
        self.properties['Scale']=float(foo)
    def SetRebin(self,foo):
        self.properties['Rebin']=int(foo)
    def GetIsGraph(self):
        return False
    def GetHist(self):
        return self.hist
    def GetIs2dim(self):
        return self.properties['is2dim']
    def GetPolyMarker(self):
        return self.properties['PolyMarker']
    def GetDotSize(self):
        return self.properties['DotSize']
    def GetDotScale(self):
        return self.properties['DotScale']
    def GetErrorBars(self):
        return self.properties['ErrorBars']
    def GetNormalizeToIntegral(self):
        return self.properties['NormalizeToIntegral']
    def GetNormalizeToSum(self):
        return self.properties['NormalizeToSum']
    def GetScale(self):
        return self.properties['Scale']
    def GetRebin(self):
        return self.properties['Rebin']

class Graph(Histogram):
    def __init__(self,id,hist):
        Histogram.__init__(self,id,hist)
        self.properties['is2dim']=False
        self.properties['PolyMarker']='*'
        self.properties['ErrorBars']=True
    def GetIsGraph(self):
        return True

class Function(DrawableObject):
    def __init__(self,id,code):
        DrawableObject.__init__(self,id)
        self.properties['Code']=str(code)
        self.properties['XMin']=-99999
        self.properties['XMax']=-99999
    def Save(self,file):
        file.write('# BEGIN FUNCTION %s\n' %(self.GetId()))
        self.SaveDrawableObject(file)
        if self.GetXMin()>-99999:
            file.write('XMin=%s\n' %(self.GetXMin()))
        if self.GetXMax()>-99999:
            file.write('XMax=%s\n' %(self.GetXMax()))
        if self.GetCode()!=None:
            file.write('Code=\n%s\n' %(self.GetCode()))
        file.write('# END FUNCTION\n\n')
        #
    def SetXMin(self,foo):
        self.properties['XMin']=float(foo)
    def SetXMax(self,foo):
        self.properties['XMax']=float(foo)
    def GetCode(self):
        return self.properties['Code']
    def GetXMin(self):
        return self.properties['XMin']
    def GetXMax(self):
        return self.properties['XMax']

class Special:
    def __init__(self,id):
        self.lines=[]
        self.properties={}
        self.properties['id']=id
        self.properties['Clip']=False
    def Save(self,file):
        file.write('# BEGIN SPECIAL %s\n' %(self.GetId()))
        if self.GetClip():
            file.write('\\psclip{\\psframe[linewidth=0, linestyle=none](0,0)(1,1)}\n')
        for i in self.lines:
            file.write(i)
        if self.GetClip():
            file.write('\\endpsclip\n')
        file.write('# END SPECIAL\n\n')
    def AddLine(self,foo):
        self.lines.append('%s\n' %(foo))
    def SetClip(self,foo):
        self.properties['Clip']=bool(foo)
    def GetId(self):
        return self.properties['id']
    def GetClip(self):
        return self.properties['Clip']


class Plot:
    def __init__(self):
        self.histos=[]
        self.functions=[]
        self.specials=[]
        self.properties={}
        self.properties['Comment']=[]
        self.properties['Title']=None
        self.properties['XLabel']=None
        self.properties['YLabel']=None
        self.properties['XLabelSep']=None
        self.properties['YLabelSep']=None
        self.properties['XMin']=-99999
        self.properties['XMax']=-99999
        self.properties['YMin']=-99999
        self.properties['YMax']=-99999
        self.properties['ZMin']=-99999
        self.properties['ZMax']=-99999
        self.properties['LogX']=False
        self.properties['LogY']=False
        self.properties['Legend']=False
        self.properties['CustomLegend']=None
        self.properties['LegendXPos']=-2
        self.properties['LegendYPos']=-2
        self.properties['LegendOnly']=None
        self.properties['DrawOnly']=None
        self.properties['Stack']=None
        self.properties['DrawSpecialFirst']=False
        self.properties['DrawFunctionFirst']=False
        self.properties['XMinorTickMarks']=-1
        self.properties['YMinorTickMarks']=-1
        self.properties['XMajorTickMarks']=-1
        self.properties['YMajorTickMarks']=-1
        self.properties['XCustomTicks']=None
        self.properties['YCustomTicks']=None
        self.properties['PlotSize']=None
        self.properties['LeftMargin']=None
        self.properties['RightMargin']=None
        self.properties['TopMargin']=None
        self.properties['BottomMargin']=None
    def Save(self,filename):
        file=open(filename, 'w')
        #
        file.write('# BEGIN PLOT\n')
        for i in self.properties['Comment']:
            file.write(i)
        if self.GetTitle()!=None:
            file.write('Title=%s\n' %(self.GetTitle()))
        if self.GetXLabel()!=None:
            file.write('XLabel=%s\n' %(self.GetXLabel()))
        if self.GetYLabel()!=None:
            file.write('YLabel=%s\n' %(self.GetYLabel()))
        if self.GetXLabelSep()!=None:
            file.write('XLabelSep=%s\n' %(self.GetXLabelSep()))
        if self.GetYLabelSep()!=None:
            file.write('YLabelSep=%s\n' %(self.GetYLabelSep()))
        if self.GetXMin()>-99999:
            file.write('XMin=%s\n' %(self.GetXMin()))
        if self.GetXMax()>-99999:
            file.write('XMax=%s\n' %(self.GetXMax()))
        if self.GetYMin()>-99999:
            file.write('YMin=%s\n' %(self.GetYMin()))
        if self.GetYMax()>-99999:
            file.write('YMax=%s\n' %(self.GetYMax()))
        if self.GetZMin()>-99999:
            file.write('ZMin=%s\n' %(self.GetZMin()))
        if self.GetZMax()>-99999:
            file.write('ZMax=%s\n' %(self.GetZMax()))
        if self.GetLogX():
            file.write('LogX=1\n')
        if self.GetLogY():
            file.write('LogY=1\n')
        if self.GetLegend():
            file.write('Legend=1\n')
        if self.GetCustomLegend()!=None:
            file.write('CustomLegend=%s\n' %(self.GetCustomLegend()))
        if self.GetLegendXPos()>-2:
            file.write('LegendXPos=%s\n' %(self.GetLegendXPos()))
        if self.GetLegendYPos()>-2:
            file.write('LegendYPos=%s\n' %(self.GetLegendYPos()))
        if self.GetLegendOnly()!=None:
            file.write('LegendOnly=%s\n' %(self.GetLegendOnly()))
        if self.GetDrawOnly()!=None:
            file.write('DrawOnly=%s\n' %(self.GetDrawOnly()))
        if self.GetStack()!=None:
            file.write('Stack=%s\n' %(self.GetStack()))
        if self.GetDrawSpecialFirst():
            file.write('DrawSpecialFirst=1\n')
        if self.GetDrawFunctionFirst():
            file.write('DrawFunctionFirst=1\n')
        if self.GetXMinorTickMarks()>-1:
            file.write('XMinorTickMarks=%s\n' %(self.GetXMinorTickMarks()))
        if self.GetYMinorTickMarks()>-1:
            file.write('YMinorTickMarks=%s\n' %(self.GetYMinorTickMarks()))
        if self.GetXMajorTickMarks()>-1:
            file.write('XMajorTickMarks=%s\n' %(self.GetXMajorTickMarks()))
        if self.GetYMajorTickMarks()>-1:
            file.write('YMajorTickMarks=%s\n' %(self.GetYMajorTickMarks()))
        if self.GetXCustomTicks()!=None:
            file.write('XCustomTicks=%s\n' %(self.GetXCustomTicks()))
        if self.GetYCustomTicks()!=None:
            file.write('YCustomTicks=%s\n' %(self.GetYCustomTicks()))
        if self.GetPlotSize()!=None:
            file.write('PlotSize=%s\n' %(self.GetPlotSize()))
        if self.GetLeftMargin()!=None:
            file.write('LeftMargin=%s\n' %(self.GetLeftMargin()))
        if self.GetRightMargin()!=None:
            file.write('RightMargin=%s\n' %(self.GetRightMargin()))
        if self.GetTopMargin()!=None:
            file.write('TopMargin=%s\n' %(self.GetTopMargin()))
        if self.GetBottomMargin()!=None:
            file.write('BottomMargin=%s\n' %(self.GetBottomMargin()))
        file.write('# END PLOT\n\n')
        #
        for special in self.specials:
            special.Save(file)
        for histo in self.histos:
            histo.Save(file)
        for function in self.functions:
            function.Save(file)
        file.close()
    def AddHistogram(self,foo):
        self.histos.append(foo)
    def AddGraph(self,foo):
        self.histos.append(foo)
    def AddFunction(self,foo):
        self.functions.append(foo)
    def AddSpecial(self,foo):
        self.specials.append(foo)
    def AddCommentLine(self,foo):
        self.properties['Comment'].append('# %s\n' %(foo))
    def SetTitle(self,foo):
        self.properties['Title']=str(foo)
    def SetXLabel(self,foo):
        self.properties['XLabel']=str(foo)
    def SetYLabel(self,foo):
        self.properties['YLabel']=str(foo)
    def SetXLabelSep(self,foo):
        self.properties['XLabelSep']=str(foo)
    def SetYLabelSep(self,foo):
        self.properties['YLabelSep']=str(foo)
    def SetXMin(self,foo):
        self.properties['XMin']=float(foo)
    def SetXMax(self,foo):
        self.properties['XMax']=float(foo)
    def SetYMin(self,foo):
        self.properties['YMin']=float(foo)
    def SetYMax(self,foo):
        self.properties['YMax']=float(foo)
    def SetZMin(self,foo):
        self.properties['ZMin']=float(foo)
    def SetZMax(self,foo):
        self.properties['ZMax']=float(foo)
    def SetLogX(self,foo):
        self.properties['LogX']=bool(foo)
    def SetLogY(self,foo):
        self.properties['LogY']=bool(foo)
    def SetLegend(self,foo):
        self.properties['Legend']=bool(foo)
    def SetCustomLegend(self,foo):
        self.properties['CustomLegend']=str(foo)
    def SetLegendXPos(self,foo):
        self.properties['LegendXPos']=float(foo)
    def SetLegendYPos(self,foo):
        self.properties['LegendYPos']=float(foo)
    def SetLegendOnly(self,foo):
        self.properties['LegendOnly']=str(foo)
    def SetDrawOnly(self,foo):
        self.properties['DrawOnly']=str(foo)
    def SetStack(self,foo):
        self.properties['Stack']=str(foo)
    def SetDrawSpecialFirst(self,foo):
        self.properties['DrawSpecialFirst']=bool(foo)
    def SetDrawFunctionFirst(self,foo):
        self.properties['DrawFunctionFirst']=bool(foo)
    def SetXMinorTickMarks(self,foo):
        self.properties['XMinorTickMarks']=int(foo)
    def SetYMinorTickMarks(self,foo):
        self.properties['YMinorTickMarks']=int(foo)
    def SetXMajorTickMarks(self,foo):
        self.properties['XMajorTickMarks']=int(foo)
    def SetYMajorTickMarks(self,foo):
        self.properties['YMajorTickMarks']=int(foo)
    def SetXCustomTicks(self,foo):
        self.properties['XCustomTicks']=str(foo)
    def SetYCustomTicks(self,foo):
        self.properties['YCustomTicks']=str(foo)
    def SetPlotSize(self,foo):
        self.properties['PlotSize']=str(foo)
    def SetLeftMargin(self,foo):
        self.properties['LeftMargin']=float(foo)
    def SetRightMargin(self,foo):
        self.properties['RightMargin']=float(foo)
    def SetTopMargin(self,foo):
        self.properties['TopMargin']=float(foo)
    def SetBottomMargin(self,foo):
        self.properties['BottomMargin']=float(foo)
    def GetTitle(self):
        return self.properties['Title']
    def GetXLabel(self):
        return self.properties['XLabel']
    def GetYLabel(self):
        return self.properties['YLabel']
    def GetXLabelSep(self):
        return self.properties['XLabelSep']
    def GetYLabelSep(self):
        return self.properties['YLabelSep']
    def GetXMin(self):
        return self.properties['XMin']
    def GetXMax(self):
        return self.properties['XMax']
    def GetYMin(self):
        return self.properties['YMin']
    def GetYMax(self):
        return self.properties['YMax']
    def GetZMin(self):
        return self.properties['ZMin']
    def GetZMax(self):
        return self.properties['ZMax']
    def GetLogX(self):
        return self.properties['LogX']
    def GetLogY(self):
        return self.properties['LogY']
    def GetLegend(self):
        return self.properties['Legend']
    def GetCustomLegend(self):
        return self.properties['CustomLegend']
    def GetLegendXPos(self):
        return self.properties['LegendXPos']
    def GetLegendYPos(self):
        return self.properties['LegendYPos']
    def GetLegendOnly(self):
        return self.properties['LegendOnly']
    def GetDrawOnly(self):
        return self.properties['DrawOnly']
    def GetStack(self):
        return self.properties['Stack']
    def GetDrawSpecialFirst(self):
        return self.properties['DrawSpecialFirst']
    def GetDrawFunctionFirst(self):
        return self.properties['DrawFunctionFirst']
    def GetXMinorTickMarks(self):
        return self.properties['XMinorTickMarks']
    def GetYMinorTickMarks(self):
        return self.properties['YMinorTickMarks']
    def GetXMajorTickMarks(self):
        return self.properties['XMajorTickMarks']
    def GetYMajorTickMarks(self):
        return self.properties['YMajorTickMarks']
    def GetXCustomTicks(self):
        return self.properties['XCustomTicks']
    def GetYCustomTicks(self):
        return self.properties['YCustomTicks']
    def GetPlotSize(self):
        return self.properties['PlotSize']
    def GetLeftMargin(self):
        return self.properties['LeftMargin']
    def GetRightMargin(self):
        return self.properties['RightMargin']
    def GetTopMargin(self):
        return self.properties['TopMargin']
    def GetBottomMargin(self):
        return self.properties['BottomMargin']



