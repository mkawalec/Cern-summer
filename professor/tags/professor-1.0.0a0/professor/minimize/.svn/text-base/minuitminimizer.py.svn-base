"""
Normal interface to the Minuit minimizer via PyROOT.
"""

import ROOT

from professor.tools import log as logging
from baseminimizer import BaseMinimizer
from result import MinimizationResult


class ROOTMinuitMinimizer(BaseMinimizer):
    """Code copied from useitall.py"""
    def initMinimization(self):
        # check's if we need to rebuild the fitting function and the
        # histogram
        super(ROOTMinuitMinimizer, self).initMinimization()

        filtereddata = []
        for bp in self.getData().itervalues():
            if not bp.veto:
                filtereddata.append(bp)



        def fit_func_root(x, params):
            bin = int(x[0])
            binprops = filtereddata[bin]
            return binprops.sqrtweight * binprops.ipol.getValue(params)

        npars = self.getScaler().dim()
        nbins = len(filtereddata)

        self.__f = ROOT.TF1("prediction", fit_func_root, 0, nbins, npars)
        self.__h = ROOT.TH1F("data_reduced", "data_reduced", nbins, 0, nbins)
        for i, binprops in enumerate(filtereddata):
            self.__h.SetBinContent(i+1, binprops.sqrtweight*binprops.refbin.getYVal())
            self.__h.SetBinError(i+1, binprops.refbin.getYErr())

    def minimize(self):
        # set starting point parameters: this is useless
        # for i, p in enumerate(self.getStartpoint()):
            # self.__f.SetParameter(i, p)

        # fix parameters
        for i in xrange(self.__f.GetNpar()):
            pi = self.getFixedParameter(i)
            if pi is not None:
                logging.debug("Fixing parameter #%i to %e" % (i, pi))
                self.__f.FixParameter(i, pi)
            else:
                logging.debug("Releasing parameter #%i" % i)
                self.__f.ReleaseParameter(i)

        # Fit options:
        # N: Do not store the graphics function, do not draw.
        # M: More. Improve fit results.
        # E: Perform better Errors estimation using Minos technique.
        self.__h.Fit("prediction", "NME")

        minuit = ROOT.gMinuit

        scaler = self.getScaler()
        # plain list
        val = []
        # list of pairs
        err = []

        # we need this to retrieve the MINOS errors from MINUIT
        eplus = ROOT.Double()
        eminus = ROOT.Double()
        eparab = ROOT.Double()
        gcc = ROOT.Double()

        for i in xrange(scaler.dim()):
            ival = self.__f.GetParameter(i)
            ierr = self.__f.GetParError(i)

            minuit.mnerrs(i, eplus, eminus, eparab, gcc)

            val.append(ival)
            err.append((-float(eminus), float(eplus)))

            # compare errors from MIGRAD and MINOS
            logging.debug("#%i %e +- %e (MIGRAD)"%(i, ival, ierr))
            logging.debug("    MINOS    +- %e"%(eparab))
            logging.debug("    MINOS    + %e  - %e"%(eplus, eminus))
            logging.debug("    MINOS    gcc: %e"%(gcc))

        logging.debug("chi^2: %s  ndf: %s"%(self.__f.GetChisquare(),
                                            self.__f.GetNDF()))

        chi2 = self.__f.GetChisquare()

        return MinimizationResult.withScaler(chi2, scaler, val, errscaled=err)
