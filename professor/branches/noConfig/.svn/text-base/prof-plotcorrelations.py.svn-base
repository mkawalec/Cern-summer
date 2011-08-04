#!/usr/bin/env python

import os, pylab, matplotlib, numpy, logging, time
from professor.tools import latextools
from professor.tools import stringtools as st
from professor.minimize import result
try:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed([])
except:
    print "Ipython shell not available."

params = {
        'backend':'pdf',
        #'axes.labelsize': 20,
        #'text.fontsize': 20,
        #'legend.fontsize': 20,
        #'axes.titlesize': 20,
        #'xtick.labelsize': 20,
        #'ytick.labelsize': 20,
        #'text.usetex': True, # TODO: understand why scripts crashes if set to True
        'text.latex.preamble' :  ['\usepackage{amsmath}'],
        'figure.dpi': 150,
        #'lines.markersize':7.5,
        #'figure.subplot.left' : 0.12,
        #'figure.subplot.right' : 0.995,
        #'figure.subplot.bottom' : 0.1,
        #'figure.subplot.top' : 0.979,
        #'lines.markersize':5
        }

pylab.rcParams.update(params)

usage = """%prog - generate param-param correlation plots and tables

USAGE:
  %prog [options] <results>
  where results may either be a directory or a certain results file.
  The filetype to look for may be specified via "-f" (default: "xml")

  The user may also specify an output directory via "-o"
  (default: "correlations"). The colormaps will be stored in a subdir
  ("colormaps") while the tex file and a pdf file created from it
  will be written to the subdir "tex".

  To help making filenames unique one may also force the output file name
  to include a timestamp (use "-t" for that).

TODO:
  * less colorbar ticks
  * make colorbar labels be typeset in latex
  * find suitable b/w colormap???
  * generic plottitle on demand using e.g. figtext
"""

from optparse import OptionParser
parser = OptionParser(usage=usage)
parser.add_option("-o", "--outdir", dest="OUTDIR",
                  default="correlations", help="write data files into this directory")
parser.add_option("-f", "--filetype", dest="FILETYPE",
                  default='xml', help="specify file ending of result files")
parser.add_option("-t", "--timestamp", action="store_true", dest="TIMESTAMP",
                  default=True, help="add a timestamp prefix to the output directory name")
parser.add_option("-Q", "--quiet", help="Suppress normal messages", dest="LOGLEVEL",
                  action="store_const", default=logging.INFO, const=logging.WARNING)
parser.add_option("-V", "--verbose", help="Add extra debug messages", dest="LOGLEVEL",
                  action="store_const", default=logging.INFO, const=logging.DEBUG)
opts, args = parser.parse_args()
logging.basicConfig(level=opts.LOGLEVEL, format="%(message)s")

# check if outdir exists and create it otherwise
TEXOUT  = opts.OUTDIR + "/tex"
PLOTOUT = opts.OUTDIR + "/colormaps"

if not os.path.isdir(opts.OUTDIR):
    os.mkdir(opts.OUTDIR)
if not os.path.isdir(TEXOUT):
    os.mkdir(TEXOUT)
if not os.path.isdir(PLOTOUT):
    os.mkdir(PLOTOUT)

def getResultfiles():
    if len(args) == 1:
        if os.path.isdir(args[0]):
            resultfiles = crawlDir(args[0])
        else:
            resultfiles = [args[0]]
    elif len(args) > 1:
        resultfiles = [i for i in args]
    else:
        logging.info("Reading resultfiles from PWD.")
        resultfiles = crawlDir('.')
    return resultfiles

def getStamp():
    if opts.TIMESTAMP:
        return time.strftime("%Y_%m_%d_")
    else:
        return ""

def crawlDir(directory):
    return [file for file in os.listdir(directory) if file.endswith(opts.FILETYPE)]

def wrapinTex(s):
    if "$" in s:
        return s
    else:
        return "$\\mathrm{%s}$"%((s.replace(" ","\\:")).replace("_","\\_")).replace("->","\\rightarrow ")

for file in getResultfiles():
    print 'processing file %s'%file
    res = result.ResultList.fromXML(file)
    s = res.getCorrelations(True, True)
    if not s is None: # a asafety, checking if correlations were stored at all
        a = list(st.sortParamNameList(res.getParamNames()))
        a_wrap = map(wrapinTex, a)
        a_rev = list(reversed(a))
        a_rev_wrap = map(wrapinTex, a_rev)
        x = numpy.arange(len(a)+1)
        y = numpy.arange(len(a)+1)
        X,Y = numpy.meshgrid(x,y)
        corr = numpy.zeros((len(a),len(a)))
        corr_err = numpy.zeros((len(a),len(a)))
        for n, n_item in enumerate(a):
            #for m, m_item in enumerate(reversed(a)):
            for m, m_item in enumerate(a_rev):
                try:
                    corr[m][n] = s[(n_item, m_item)][0]
                    corr_err[m][n] = s[(n_item, m_item)][1]
                except KeyError:
                    corr[m][n] = 0.
                    corr_err[m][n] = 0.
        fig = pylab.figure(facecolor='w')
        fig.set_figwidth(10)
        fig.set_figheight(7)
        fig.subplots_adjust(left=0.25, right=0.9, bottom=0.4, top=0.9, wspace=0.4)
        # l.h.s. plot
        sp1 = fig.add_subplot(1,2,1)
        # draw colormap
        coll1 = sp1.pcolor(X,Y,corr, vmin=-1., vmax=1.,cmap=matplotlib.cm.RdBu)
        # add 'color legends'
        cb=fig.colorbar(coll1)
        #cb.ax.set_yticks([0,.5,1])

        cb.set_label('$C_\\mathit{ij}$', rotation=0)
        # x/y-ticks handling
        #ipshell()
        sp1.set_xticks(numpy.linspace(.5,len(a)-.5, len(a)))
        sp1.set_yticks(numpy.linspace(.5,len(a)-.5, len(a)))
        #sp1.set_yticklabels(a_rev)
        # titles

        # r.h.s. plot
        sp2 = fig.add_subplot(1,2,2)
        coll2 = sp2.pcolor(X,Y,corr_err, vmin=0., vmax=1.,cmap=matplotlib.cm.gray_r)
        cb2 = fig.colorbar(coll2)
        #cb2.ax.set_yticks([0,.5,1])
        cb2.set_label('$\\Delta C_\\mathit{ij}$', rotation=0)

        sp2.set_xticks(numpy.linspace(.5,len(a)-.5, len(a)))
        sp2.set_yticks(numpy.linspace(.5,len(a)-.5, len(a)))
        #sp2.set_xticklabels(a, rotation=270)
        # remove yticks
        sp2.set_yticklabels([' '])
        try:
            sp1.set_xticklabels(a_wrap, rotation=270)
            sp2.set_xticklabels(a_wrap, rotation=270)
            sp1.set_yticklabels(a_rev_wrap, rotation=0)
        except:
            print "LATEX failed..."
            sp1.set_xticklabels(a, rotation=270)
            sp2.set_xticklabels(a, rotation=270)
            sp1.set_yticklabels(a_rev, rotation=0)

        # save fig
        plotname = PLOTOUT+'/'+'correlations_' + getStamp() + file.split('.xml')[0] + '.pdf'
        texname = TEXOUT+'/' + file.split('.xml')[0] + '.tex'

        fig.savefig(plotname)

        #creating a file for saving tex code
        f=open(texname,'w')
        b=res.getParamNames()
        # the return value of getCorrelationTable is a list of latex strings
        for line in latextools.getCorrelationTable(s,b,True, True):
            f.write((line.replace('_','\\:')).replace('->','$\\rightarrow$'))
            f.write('\n')
        f.close()
        ## run pdflatex to create pdf file of table
        #filename = file.split('.xml')[0]
        cmdline = 'pdflatex -output-directory %s %s &> /dev/null'%(TEXOUT, texname)
        try:
            os.system(cmdline)
        except:
            logging.error("failed! pdflatex may not be installed")
        ## clean up latex mess
        for i in ['.log', '.aux' ]:
            os.system('rm -f %s%s'%(texname.split(".")[0], i))
    else:
        print 'file %s does not contain any information on correlations'%file

logging.info("Done. Written all output to: %s"%opts.OUTDIR)
