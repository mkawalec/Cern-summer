#!/usr/bin/python
"""sensitivityplotter.py
calculates (dMC/MC)/(p0 - p) for all bins and parametervalues between 0 and 1
in the scaled world and plotting the result as a colormap

Left hand plot always uses the interpolation center as p0, the right hand plot
uses center * numpy.zeros(dim) as p0

Mini Manual:

usage: python nonsens2.py PATH

here, PATH is the (not mandatory) path to a directory that contains
subdirectories mc and ref
if PATH is omitted, a FileDialog is opened and you have to navigate
to an appropriate directory


I  ==Envelope Plots==

1.) Choose one or more observables
2.) Check or uncheck plotting options and hit the Envelope-button.


II ==Sensitivity Plots==

=Neccessary=

1.) Choose one or more Observables from upper Listbox
2.) Enter threshold: only bins whose relative errors are <= this value will be
    used for the calculation. In a plot, these bins will be drawn with the
    color that corresponds to the colorvalue 0 (default: yellow).
3.) choose from the Radiobuttons, whether the max relative error shall be taken
    from the RefHisto or from all MCHistos (the latter is default).
4.) Choose value for the right hand plot (has to be between 0 and 1) that all
    other parametervalues are set to during the calculation of the sensitivity
    of an observable to each single parameter (has no effect on projected
    sensitivity).
5.) Choose, whether you want to have a centered or a projected Sensitivity
    calculated and hit the Sensitivity-button.

=Other=

5.) You may or may not want to use the same colorscaling for all plots, if you
    want so, check on 'use same colorbar for ...'
6.) If you are not happy with the default Colormap RdYlBu, you can choose
    another colormap of 58 in total from the lower listbox
7.) The Button 'Close All' closes all created plots
8.) If you want to investigate another directory, hit 'File'->'Open' and
    navigate to (make sure, it contains subdirectories mc and ref!)
"""

import pylab, os, sys, numpy, matplotlib, matplotlib.cm
import Tkinter as tk
import FileDialog as fd
from professor import rivetreader as rr
from professor.controlplots import sensitivity as st
from professor.controlplots import envelope as ev

class App:
    def __init__(self, master, DIR=False):
        # main window
        self._master = tk.Frame(master)
        # tk.Label(self._master, text='Please choose Observable(s):').pack()
        # directory settings
        self._startDIR = os.path.expandvars('$PWD')
        # all other frames
        self._select_obs = tk.Frame(self._master)
        self._select_obs.pack()
        tk.Label(self._select_obs, text='Please choose Observable(s):').pack()
        self._select_scaling = tk.Frame(self._master)
        self._select_cmap = tk.Frame(self._master)
        self._select_intcenter = tk.Frame(self._master)
        self._select_center = tk.Frame(self._master)
        self._select_threshold = tk.Frame(self._master)
        self._select_method = tk.Frame(self._master)
        self._buttons = tk.Frame(self._master)
        self._cbar = tk.Frame(self._master)
        self._frame_envel = tk.Frame(self._master, relief=tk.GROOVE)
        #
        tk.Label(self._frame_envel, text='Select Envelope Plotting Options:').pack()
        self._envel = tk.BooleanVar()
        self._envel.set(True)
        self._refdat = tk.BooleanVar()
        self._refdat.set(True)
        self._mcpolys = tk.BooleanVar()
        self._mcpolys.set(False)
        tk.Checkbutton(self._frame_envel, text='Envelope',
                variable=self._envel,onvalue=True, offvalue=False).pack(side=tk.LEFT)
        tk.Checkbutton(self._frame_envel, text='ReferenceData',
                variable=self._refdat,onvalue=True, offvalue=False).pack(side=tk.LEFT)
        tk.Checkbutton(self._frame_envel, text='MC-Entries as Polygons',
                variable=self._mcpolys,onvalue=True, offvalue=False).pack(side=tk.LEFT)
        #
        self._one4all = tk.StringVar()
        self._one4all.set('all')
        tk.Checkbutton(self._cbar, text='use same colorbar for all plots',
                variable=self._one4all, onvalue='all', offvalue='single').pack()
        # logarithmic scales
        self._logx = tk.BooleanVar()
        self._logy = tk.BooleanVar()
        # not packed, since feature doesnt work yet
        #tk.Checkbutton(self._select_scaling, text="log x", variable=self._logx,
        #        onvalue=True, offvalue=False).pack()
        #tk.Checkbutton(self._select_scaling, text="log y", variable=self._logy,
        #        onvalue=True, offvalue=False).pack()

        # swich between interactive mode and saving image to file
        self._printshow = tk.StringVar()
        self._printshow.set('show')
        tk.Radiobutton(self._buttons, text='Show Image(s)', variable=self._printshow, value='show').pack(side=tk.BOTTOM)
        tk.Radiobutton(self._buttons, text='Save Image(s) to file', variable=self._printshow, value='print').pack(side=tk.BOTTOM)

        # method selection
        self._method = tk.StringVar(self._select_method)
        self._method.set('centered')
        tk.Label(self._select_method, text='Choose calculation method')
        tk.Radiobutton(self._select_method, text='centered Sensitivity', variable=self._method, value='centered').pack(side=tk.LEFT)
        tk.Radiobutton(self._select_method, text='projected Sensitivity (slow)', variable=self._method, value='projected').pack(side=tk.LEFT)
        # colormap selection
        self._default_cmap = 'RdYlBu'
        tk.Label(self._select_cmap, text='Select Colormap, default is %s:'%self._default_cmap).pack()
        self._cmapsel = self.createListBoxFromList(self._select_cmap, matplotlib.cm.cmapnames, selectmode=tk.SINGLE)
        #interpolation center selection
        self._intcenter = tk.DoubleVar(self._select_intcenter)
        self._intcenter.set(.5)
        self._intentry = tk.Entry(self._select_intcenter, width=6, textvariable=self._intcenter)
        tk.Label(self._select_intcenter, text='Choose interpolation center:').pack()
        self._intentry.pack()
        # center selection
        self._center = tk.DoubleVar(self._select_center)
        self._center.set(.5)
        self._entry = tk.Entry(self._select_center, width=6, textvariable=self._center)
        tk.Label(self._select_center, text='Choose right hand plot center:').pack()
        self._entry.pack()
        # threshold selection
        self._thresh = tk.DoubleVar(self._select_threshold)
        self._thresh.set(5.)
        self._entry_th = tk.Entry(self._select_threshold, width=8, textvariable=self._thresh)
        tk.Label(self._select_threshold, text='Set Upper Tolerance Limit for relative errors (in %)').pack()
        self._entry_th.pack()
        self._mode = tk.StringVar(self._select_threshold)
        self._mode.set('mc')
        tk.Radiobutton(self._select_threshold, text='use MC', variable=self._mode, value='mc').pack(side=tk.LEFT)#anchor=tk.W)
        tk.Radiobutton(self._select_threshold, text='use Ref', variable=self._mode, value='ref').pack(side=tk.LEFT)#anchor=tk.W)
        self._buttons.pack(side=tk.BOTTOM)
        self._select_cmap.pack(side=tk.BOTTOM)
        tk.Frame(self._master, height=2, bg='black').pack(side=tk.BOTTOM, fill=tk.BOTH) # seperating line
        self._select_method.pack(side=tk.BOTTOM)
        tk.Frame(self._master, height=1, bg='grey').pack(side=tk.BOTTOM, fill=tk.BOTH) # seperating line
        self._cbar.pack(side=tk.BOTTOM)
        tk.Frame(self._master, height=1, bg='grey').pack(side=tk.BOTTOM, fill=tk.BOTH) # seperating line
        self._select_center.pack(side=tk.BOTTOM)
        tk.Frame(self._master, height=1, bg='grey').pack(side=tk.BOTTOM, fill=tk.BOTH) # seperating line
        self._select_intcenter.pack(side=tk.BOTTOM)
        tk.Frame(self._master, height=1, bg='grey').pack(side=tk.BOTTOM, fill=tk.BOTH) # seperating line
        self._select_threshold.pack(side=tk.BOTTOM)
        # self._select_scaling.pack(side=tk.BOTTOM)
        tk.Frame(self._master, height=2, bg='black').pack(side=tk.BOTTOM, fill=tk.BOTH) # seperating line
        self._frame_envel.pack(side=tk.BOTTOM)
        tk.Frame(self._master, height=1, bg='grey').pack(side=tk.BOTTOM, fill=tk.BOTH) # seperating line
        self._master.pack()
        # buttons
        tk.Button(self._buttons, text="QUIT", fg="red", command=self.quit).pack(side=tk.LEFT)
        tk.Button(self._buttons, text="Sensitivity", fg='blue', command=self.ok_sens).pack(side=tk.RIGHT)#LEFT)
        tk.Button(self._buttons, text="Envelope", fg='blue', command=self.ok_env).pack(side=tk.RIGHT)#LEFT)
        tk.Button(self._buttons, text='Close all', command=self.close).pack(side=tk.RIGHT)
        # refresh obs-box and prepare sensitivity
        self.checkDir(DIR)
        self.update()

    def checkDir(self, DIR):
        """ only to be called on init, checks whether given path DIR is valid
            or opens file-dialog if DIR is false
        """
        if DIR is False:
            self.setDir()
        elif os.path.isdir(DIR):
            self._DIR = DIR
        else:
            raise StandardError('not a directory!')

    def update(self):
        """ refresh obs-list and prepare sensitivities """
        self._select_obs.forget()
        self._select_obs = tk.Frame(self._master)
        tk.Label(self._select_obs, text='Please choose Observable(s):').pack()
        self._td = rr.getTuningData(self._DIR+'/ref', self._DIR+'/mc')
        self._S = self.getSensitivity(self._DIR)
        self._obssel = self.createListBoxFromList(self._select_obs, self._S._observables)
        self._select_obs.pack()#side=tk.TOP)

    def setDir(self):
        """ opens FileDialog and returns selection if it is a directory
        """
        d = fd.FileDialog(self._master)
        DIR = d.go(self._startDIR)
        if os.path.isdir(DIR):
            self._DIR = DIR
            self.update()
        else:
            raise StandardError('not a directory!')

    def getDir(self):
        """ return currently used directory """
        return self._DIR

    def getSensitivity(self, DIR):
        """ create TuningData-object from histos found in DIR and use it to
            get Sensitivity-object
        """
        # td = rr.getTuningData(DIR+'/ref', DIR+'/mc')#change this line as needed
        return st.Sensitivity(self._td)

    def quit(self):
        """ quit the program """
        self.close()
        self._master.quit()

    def close(self):
        """ close all figures """
        pylab.close('all')

    def ok_sens(self):
        """ select colormap and plot all selected observables """
        if len(self._cmapsel.curselection()) == 0: # set default cmap
            CMAP = self._default_cmap
        else:
            temp = matplotlib.cm.cmapnames
            temp.sort()
            CMAP = [temp[int(i)] for i in self._cmapsel.curselection()][0]

        temp = self._S._observables
        temp.sort()
        SELECTION = [temp[int(i)] for i in self._obssel.curselection()] # selected observables

        if self.confirm():
            pylab.ioff()
            for obs in SELECTION:
                #self._S.plotOverview(obs, newcenter=self._center.get(),
                #        cmap=matplotlib.cm.get_cmap(CMAP),
                #        errorlimit=self._thresh.get(), mode=self._mode.get(),
                #        method=self._method.get(),
                #        cscale=self._one4all.get(),
                #        intcenter=self._intcenter.get(),
                #        logscale=(self._logx.get(),self._logy.get()), printshow=self._printshow.get())
                self._S.plotOverview2(obs, intcenter=self._intcenter.get(),
                        cmap=matplotlib.cm.get_cmap(CMAP),
                        errorlimit=self._thresh.get(), mode=self._mode.get(),
                        method=self._method.get(), cscale=self._one4all.get(),
                        printshow=self._printshow.get())
            if self._printshow.get() == 'show':
                pylab.show()
        else:
            print 'Center value must be < 1 and > 0 !'

    def ok_env(self):
        """ plot Envelope """
        temp = self._td.getMCHistoNames()
        temp.sort()
        SELECTION = [temp[int(i)] for i in self._obssel.curselection()] # selected observables
        pylab.ioff()
        for obs in SELECTION:
            ev.Envelope(self._td, obs, plotwhat=(
                self._envel.get(), self._refdat.get(), self._mcpolys.get()),
                show=True)
        pylab.show()

    def createListBoxFromList(self, frame, alist, selectmode=tk.EXTENDED):
        """ creates a Listbox-object with vertical scrollbar and fills it with
            the elements contained in alist
        """
        temp = alist
        temp.sort()
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        lb = tk.Listbox(frame, width= 40, selectmode=selectmode, yscrollcommand=scrollbar.set, exportselection=0)
        for item in temp:
            lb.insert(tk.END, item)
        scrollbar.config(command=lb.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        return lb

    def confirm(self):
       if self._center.get() >=0. and self._center.get() <=1.:
           return True
       else:
           return False

# helper functions
def addMenu(master, menubar, label, entries):
    """ uses a list of tuples to create pulldown menus, that are added to
        the master menubar
    """
    cascade = tk.Menu(master, tearoff=0)
    for i in entries:
        if type(i) == tuple:
            cascade.add_command(label=i[0], command=i[1])
        elif i == 'sep':
            cascade.add_separator()

    menubar.add_cascade(label=label, menu=cascade)

def quit(master):
    pylab.close('all')
    master.quit()

def help():
    print __doc__

def about(string):
    print string

# check whether a path has been handed over as commandline argument
if len(sys.argv) < 2:
    DIR = False
else:
    DIR = sys.argv[1]

# gui
root = tk.Tk()
title = 'Control Plotter 0.22'
root.title(title)
a = App(root, DIR)
menubar = tk.Menu(root)
addMenu(root, menubar, 'File', [('Open', lambda: a.setDir()),'sep',
    ('Quit', lambda: quit(root))])
addMenu(root, menubar, '?', [('Help', lambda: help()),'sep',
    ('About', lambda: about(title))])
root.config(menu=menubar)
tk.mainloop()
