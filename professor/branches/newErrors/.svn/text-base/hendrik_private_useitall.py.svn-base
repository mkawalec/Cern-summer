"""useitall.py

example script to show the usage of the different parts.

I don't use from ... import ... statements so everywhere in this file it is
clear where the original code is located.

Hopefully heavy documented :)
"""

# import non-professor modules
import scipy.optimize, numpy

# import our central config/logging module
import professor.tools.config

# import parameter handling tools
import professor.tools.parameter


# import rivetreader so we can load data files
import professor.rivetreader


# get central config object and load configuration from the given file
conf = professor.tools.config.Config('example.conf')

# we use the module name `example' to store our configuration
# now we init our module with some default values in case the given
# configuration file doesn't contain any values.
# This does not overwrite any settings set before, e.g. during parsing
# example.conf!
logger = conf.initModule('example',
        {
        # a space separated list with filenames for logfiles:
        # `-' or `stderr' result in logging put to stderr
        # here we log to stderr an the file example.log
        'logfiles' : 'example.log',
        #'loglevel' : 'debug',
        # the directory where xml files reside
        'mcdir' :  './data/mc',
        'refdir' : './data/ref'
        })

# store some configuration values
mcdir = conf.getOption('example', 'mcdir')
refdir = conf.getOption('example', 'refdir')


logger.info('loading XML files from %s and %s'%(mcdir, refdir))
tundat = professor.rivetreader.getTuningData(refdir, mcdir)

#########################
##
## do some plotting here
##
#########################
#
#h={}
#import ROOT
#import array
#from professor.tools.rootplot import plotRootHistogram
#for histname, histtitle in [
#        ("/DELPHI_1996_S3430090/ds1-x1-y1", "In-plane p_T in GeV w.r.t. thrust axes (charged)"),
#        ("/DELPHI_1996_S3430090/ds1-x1-y2", "In-plane p_T in GeV w.r.t. thrust axes (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds10-x1-y1", "Mean in-plane p_T in GeV w.r.t. thrust axes vs. x_p (charged)"),
#        ("/DELPHI_1996_S3430090/ds11-x1-y1", "1-thrust, 1-T (charged)"),
#        ("/DELPHI_1996_S3430090/ds11-x1-y2", "1-thrust, 1-T (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds12-x1-y1", "Thrust major, M (charged)"),
#        ("/DELPHI_1996_S3430090/ds12-x1-y2", "Thrust major, M (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds13-x1-y1", "Thrust minor, m (charged)"),
#        ("/DELPHI_1996_S3430090/ds13-x1-y2", "Thrust minor, m (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds14-x1-y1", "Oblateness = M - m (charged)"),
#        ("/DELPHI_1996_S3430090/ds14-x1-y2", "Oblateness = M - m (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds15-x1-y1", "Sphericity, S (charged)"),
#        ("/DELPHI_1996_S3430090/ds15-x1-y2", "Sphericity, S (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds16-x1-y1", "Aplanarity, A (charged)"),
#        ("/DELPHI_1996_S3430090/ds16-x1-y2", "Aplanarity, A (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds17-x1-y1", "Planarity, P (charged)"),
#        ("/DELPHI_1996_S3430090/ds17-x1-y2", "Planarity, P (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds18-x1-y1", "C parameter (charged)"),
#        ("/DELPHI_1996_S3430090/ds18-x1-y2", "C parameter (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds19-x1-y1", "D parameter (charged)"),
#        ("/DELPHI_1996_S3430090/ds19-x1-y2", "D parameter (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds2-x1-y1", "Out-of-plane p_T in GeV w.r.t. thrust axes (charged)"),
#        ("/DELPHI_1996_S3430090/ds2-x1-y2", "Out-of-plane p_T in GeV w.r.t. thrust axes (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds20-x1-y1", "Heavy hemisphere masses, M_h^2/E_vis^2 (charged)"),
#        ("/DELPHI_1996_S3430090/ds20-x1-y2", "Heavy hemisphere masses, M_h^2/E_vis^2 (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds21-x1-y1", "Light hemisphere masses, M_l^2/E_vis^2 (charged)"),
#        ("/DELPHI_1996_S3430090/ds21-x1-y2", "Light hemisphere masses, M_l^2/E_vis^2 (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds22-x1-y1", "Difference in hemisphere masses, M_d^2/E_vis^2 (charged)"),
#        ("/DELPHI_1996_S3430090/ds22-x1-y2", "Difference in hemisphere masses, M_d^2/E_vis^2 (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds23-x1-y1", "Wide hemisphere broadening, B_max (charged)"),
#        ("/DELPHI_1996_S3430090/ds23-x1-y2", "Wide hemisphere broadening, B_max (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds24-x1-y1", "Narrow hemisphere broadening, B_min (charged)"),
#        ("/DELPHI_1996_S3430090/ds24-x1-y2", "Narrow hemisphere broadening, B_min (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds25-x1-y1", "Total hemisphere broadening, B_sum (charged)"),
#        ("/DELPHI_1996_S3430090/ds25-x1-y2", "Total hemisphere broadening, B_sum (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds26-x1-y1", "Difference in hemisphere broadening, B_diff (charged)"),
#        ("/DELPHI_1996_S3430090/ds26-x1-y2", "Difference in hemisphere broadening, B_diff (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds27-x1-y1", "Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)"),
#        ("/DELPHI_1996_S3430090/ds27-x1-y2", "Differential 2-jet rate with Durham algorithm, D_2^Durham (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds28-x1-y1", "Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)"),
#        ("/DELPHI_1996_S3430090/ds28-x1-y2", "Differential 2-jet rate with Jade algorithm, D_2^Jade (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds29-x1-y1", "Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)"),
#        ("/DELPHI_1996_S3430090/ds29-x1-y2", "Differential 3-jet rate with Durham algorithm, D_3^Durham (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds3-x1-y1", "In-plane p_T in GeV w.r.t. sphericity axes (charged)"),
#        ("/DELPHI_1996_S3430090/ds3-x1-y2", "In-plane p_T in GeV w.r.t. sphericity axes (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds30-x1-y1", "Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)"),
#        ("/DELPHI_1996_S3430090/ds30-x1-y2", "Differential 3-jet rate with Jade algorithm, D_3^Jade (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds31-x1-y1", "Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)"),
#        ("/DELPHI_1996_S3430090/ds31-x1-y2", "Differential 4-jet rate with Durham algorithm, D_4^Durham (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds32-x1-y1", "Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)"),
#        ("/DELPHI_1996_S3430090/ds32-x1-y2", "Differential 4-jet rate with Jade algorithm, D_4^Jade (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds33-x1-y1", "Energy-energy correlation, EEC (charged)"),
#        ("/DELPHI_1996_S3430090/ds34-x1-y1", "Asymmetry of the energy-energy correlation, AEEC (charged)"),
#        ("/DELPHI_1996_S3430090/ds4-x1-y1", "Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)"),
#        ("/DELPHI_1996_S3430090/ds4-x1-y2", "Out-of-plane p_T in GeV w.r.t. sphericity axes (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds5-x1-y1", "Rapidity w.r.t. thrust axes, y_T (charged)"),
#        ("/DELPHI_1996_S3430090/ds5-x1-y2", "Rapidity w.r.t. thrust axes, y_T (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds6-x1-y1", "Rapidity w.r.t. sphericity axes, y_S (charged)"),
#        ("/DELPHI_1996_S3430090/ds6-x1-y2", "Rapidity w.r.t. sphericity axes, y_S (charged and neutral)"),
#        ("/DELPHI_1996_S3430090/ds7-x1-y1", "Scaled momentum, x_p = |p|/|p_beam| (charged)"),
#        ("/DELPHI_1996_S3430090/ds8-x1-y1", "Log of scaled momentum, log(1/x_p) (charged)"),
#        ("/DELPHI_1996_S3430090/ds9-x1-y1", "Mean out-of-plane p_T in GeV w.r.t. thrust axes vs. x_p (charged)"),
#        ("/Example/Aplanarity", "Aplanarity"),
#        ("/Example/HadrTotalChMult", "Total hadronic charged multiplicity"),
#        ("/Example/HadrTotalMult", "Total hadronic multiplicity"),
#        ("/Example/Major", "Thrust major"),
#        ("/Example/Sphericity", "Sphericity"),
#        ("/Example/Thrust", "Thrust"),
#        ("/DELPHI_1996_S3430090/d35-x01-y01", "Total charged multiplicity"),
#        ("/Example/TotalMult", "Total multiplicity"),
#        ]:
#    hist=tundat.getRefHisto(histname)
#    bins=hist.getBins()
#    x=array.array('d')
#    for bin in bins:
#        xlow, xhigh = bin.getXRange()
#        x.append(xlow)
#    x.append(xhigh)
#    h[histname]=ROOT.TH1F('%s' %histname, '%s' %histname, len(bins), x)
#    for i, bin in enumerate(bins):
#        h[histname].SetBinContent(i+1, bin.getYVal())
#        h[histname].SetBinError(i+1, bin.getYErr())
#    plotRootHistogram(h[histname], title=histtitle, filename=histname.replace('/',''), logy=True)
#
#
#######################

logger.debug('checking tuning data')
# this might raise an exception
tundat.isValid()

if True:
    def fit_func_root(x, params):
        """fit_func_root() defines the prediction function in a way ROOT can
        use for the optimisation. Basically I return a constant value over the
        whole bin width.
        """
        bin=int(x[0])
        refbin, interp = data_reduced[bin]
        return interp.getValueFromScaled(params)
    def optimize_root():
        """optimize_root() uses the ROOT TH1:Fit() for optimisation.
        I define a TH1F histogram with a bin width of 1 and fill all data
        bins into this histogram. Then I fit the function defined in
        fit_func_root() to this histogram.

        NB: I don't set the start values for the fit yet, so minuit does
        everything on its own.
        """
        import ROOT
        npars=tundat.numberOfParams()
        nbins=len(data_reduced)
        # define fit function f:
        f=ROOT.TF1('prediction', fit_func_root, 0, nbins, npars)
        # define data histogram h:
        h=ROOT.TH1F('data_reduced', 'data_reduced', nbins, 0, nbins)
        # fill the histogram:
        for i, (refbin, interp) in enumerate(data_reduced):
            h.SetBinContent(i+1, refbin.getYVal())
            h.SetBinError(i+1, refbin.getYErr())
        # do the fit:
        #h.Fit('prediction', 'NMEV')
        h.Fit('prediction', 'N')
        print 'chi2     = %f' %(f.GetChisquare())
        print 'ndf      = %f' %(f.GetNDF())
        print 'chi2/ndf = %f' %(f.GetChisquare()/f.GetNDF())

        # print the result. FIXME: The error unscaling is ugly.
        guessval_root = []
        guesserr_root = []
        for i in range(npars):
            #print "Parameter %d: %f +- %f " %(i, f.GetParameter(i), f.GetParError(i))
            guessval_root.append(f.GetParameter(i))
            guesserr_root.append(f.GetParameter(i)+f.GetParError(i))
        finalguessval_root = professor.tools.parameter.ppFromList(guessval_root, scaler, scaled=True)
        finalguesserr_root = professor.tools.parameter.ppFromList(guesserr_root, scaler, scaled=True)
        print "Unscaled minimization results using ROOT:"
        unscaled_val = []
        unscaled_err = []
        for i in range(npars):
            unscaled_val.append(finalguessval_root.getUnscaled()[i])
            unscaled_err.append(finalguesserr_root.getUnscaled()[i] - finalguessval_root.getUnscaled()[i])
            print '%s  %f +- %f' %(finalguessval_root.getKeys()[i], unscaled_val[i], unscaled_err[i])
        return (unscaled_val, unscaled_err)

USE_OBS = []

# 1
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 2
USE_OBS.append([
           #"/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           "/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 3
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           "/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 4
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           "/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           "/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           "/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           #"/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           #"/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           #"/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 5
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           #"/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 6
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           #"/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 7
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           #"/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 8
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           #"/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 9
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           #"/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           #"/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 10
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           #"/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 11
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           "/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 12
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           "/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 13
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           "/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           "/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           "/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           "/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           "/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           "/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           "/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           "/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           "/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 14
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           "/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           "/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])

# 15
USE_OBS.append([
           "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
           "/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
           #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
           #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
           "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
           "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
           "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
           #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
           "/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
           "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
           "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
           "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
           "/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
           "/DELPHI_1996_S3430090/d35-x01-y01",                # Total charged multiplicity
           "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
           "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
           #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
           #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
           #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
           "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
          ])


for use_obs in USE_OBS:
#for use_obs in [USE_OBS[8]]:
    data = tundat.buildBinDistList(use_runnums = None, use_obs=use_obs)
    #data = tundat.buildBinDistList(use_runnums = None, use_obs=None)
    #data = tundat.buildBinDistList(use_runnums = None, use_obs=["/Test/Thrust", "/Test/TotalChMult"])
    data_reduced = []
    for refbin, interp in data:
        if (refbin.getYVal()!=0 and refbin.getYErr()!=0):
            data_reduced.append((refbin, interp))
    scaler = tundat.getScaler(use_runnums = None)
    unscaled_val, unscaled_err = optimize_root()

#import ROOT
#h_pull = {}
#for i in range(tundat.numberOfParams()):
#    h_pull[i] = ROOT.TH1F('pull parameter %d' %i, 'pull parameter %d' %i, 51, -5, 5)
#
#
#for excluderun in range(len(tundat.getRunNums())):
#    foo = tundat.getRunNums()
#    foo.pop(excluderun)
#
#    #data = tundat.buildBinDistList(use_runnums = foo, use_obs=["/Test/Thrust", "/Test/TotalChMult"])
#    #data = tundat.buildBinDistList(use_runnums = None, use_obs=["/Test/Thrust", "/Test/TotalChMult"])
#    data = tundat.buildBinDistList(use_runnums = None, use_obs=None)
#
#    # Reduce the data set to bins which are non-zero.
#    # Do this just once, we'll need it all over the place:
#    data_reduced = []
#    for refbin, interp in data:
#        if (refbin.getYVal()!=0 and refbin.getYErr()!=0):
#            data_reduced.append((refbin, interp))
#
#    scaler = tundat.getScaler(use_runnums = foo)
#    foo, bar = optimize_root()
#    for i in range(tundat.numberOfParams()):
#        h_pull[i].Fill((foo[i]-unscaled_val[i])/bar[i])
#
#import professor.tools.rootplot
#
#for i in range(tundat.numberOfParams()):
#    professor.tools.rootplot.plotRootHistogram(h_pull[i], title='Pull of %s, using %d out of %d runs' %(scaler.getKeys()[i], len(tundat.getRunNums())-1, len(tundat.getRunNums())), filename='pull_par_%d' %i, xlabel='pull')
#
#
## 1. create the chi2 function we want to minimize:
#logger.debug('building chi2 funtion')
#def chi2(p):
#    r = 0.
#    for refbin, interp in data_reduced:
#        r += ( (refbin.getYVal() - interp.getValueFromNormed(p)) / refbin.getYErr() )**2
#    return r
#
## Use the scipy-minimizer:
#logger.info('starting the minimization using fmin_powell')
## set the starting point to the center of unit cube
#p0 = .5 * numpy.ones(tundat.numberOfParams())
#guess = scipy.optimize.fmin_powell(chi2, p0)
#
## work around scipy bug: in 1D the guess has shape () instead of (1,)
#if guess.shape == ():
#    guess.reshape(1)
#
#logger.debug('unscaled result: %s'%(guess))
#
## Turn the guess into a ParameterPoint instance using a factory funtion.
#finalguess = professor.tools.parameter.ppFromList(guess, scaler, scaled=True)
#
## Do some final output
#logger.info('minimization result: %s'%(finalguess))
#print "Minimization results in:"
#print 'parameter names: ' + '\t'.join(finalguess.getKeys())
#print 'unscaled values: ' + '\t'.join(['%f'%(p) for p in finalguess.getUnscaled()])
#print 'scaled values:   ' + '\t'.join(['%f'%(p) for p in finalguess.getScaled()])
#
## uncomment this if you want to start a IPython shell at the end
## to examine the created objects
##
## from IPython.Shell import IPShellEmbed
## ipshell = IPShellEmbed()
## ipshell()
