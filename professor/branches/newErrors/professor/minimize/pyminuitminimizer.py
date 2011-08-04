"""pyminimizer.py

"""

import logging
import numpy


from baseminimizer import BaseMinimizer, MinError
from result import MinimizationResult

# Be tolerant if we don't have PyMinuit and try PyMinuit2 instead.
# The PyMinuit documentation promises that the class interfaces are the
# same.
try:
    from minuit2 import Minuit2 as Minuit
    from minuit2 import MinuitError
    logging.info("Using PyMinuit2 as interface")
except ImportError, e:
    from minuit import Minuit
    from minuit import MinuitError
    logging.info("Using PyMinuit as interface")

# Unless we want to edit the pyMinuit source-code, we have to live with some 
# kind of a hack for the chi2-definition. Since pyMinuit initializes using
# func.co_argcount, so the variables of the function need to be hardcoded.
# pyMinuit doesn't accept arrays or list, it counts the number of parameters
# as 1 all the time. Also, def chi2(*args): fails because the co_argcount
# is 0 here. A first approach was to define a chi2 for a number of dimension
# like chi2(x) chi2(x,y) and so on and use an if-statement.
# So at least the definition is now dynamic: I produce a string first and
# have it executed afterwards :-(

class PyMinuitMinimizer(BaseMinimizer):
    printminuit = 0
    useminos = False
    def initMinimization(self):
        # The following call isn't doing anything for the moment, might
        # change in the future.
        super(PyMinuitMinimizer, self).initMinimization()

        chi2func = self.tunedata.getChi2Function()
        dim = self.tunedata.numParams()

        if dim > 100:
            err = "Mapping of Professor parameter names to Minuit names fails with more than 100 parameters!"
            raise RunTimeError(err)

        # Unless we're using more than 100 parameters the parameter names in
        # the wrapper function will be in alphabetically order and we can
        # map them easily to PARJ... names.
        # 
        # Parameters are named after _M_inuit _P_arameter.
        mpnames = ["MP%02i"%(i) for i in xrange(dim)]
        funcargs = ", ".join(mpnames)

        funcdef = "def hackChi2Wrapper("
        funcdef += funcargs
        funcdef += "): "
        funcdef += "return chi2func(["
        funcdef += funcargs
        funcdef += "])"

        exec funcdef in locals()
        logging.debug("Built chi2 wrapper from:\n  '%s'"%(funcdef))
        self.__minuit = Minuit(hackChi2Wrapper, strategy=2)

        # turn on Minuit's printing if log level is below 20(INFO), i.e.
        # DEBUG
        if self.printminuit != 0:
            self.__minuit.printMode = self.printminuit

        # fix parameters and set startpoint
        for i, mpname in enumerate(mpnames):
            self.__minuit.values[mpname] = self.getStartpoint()[i]
            if self.getFixedParameter(i) is not None:
                self.__minuit.fixed[mpname] = True
                self.__minuit.values[mpname] = self.getFixedParameter(i)
            if self.getParameterLimits(i) is not None:
                self.__minuit.limits[mpname] = self.getParameterLimits(i)

        # self.__chi2func = hackChi2Wrapper
        # self.__chi2func.ndof = chi2func.ndof


    def minimize(self):
        # list of floats
        pvals = []
        # list of pairs of floats:
        # [ (low err, high err), ...]
        perrs = []

        # initialize Minuit
        #self.__minuit.strategy = 2

        # Call the minimizer,
        try:
            self.__minuit.migrad()
        except MinuitError, e:
            logging.error("Error during MIGRAD() call: %s" % (e))
            raise MinError(str(e))

        if self.useminos:
            # call minos to estimate errors
            try:
                self.__minuit.minos()
            except MinuitError, e:
                logging.error("Error during MINOS() call: %s" % (e))
                raise MinError(str(e))

            logging.debug("Results with MINOS:")
            for minuitname in sorted(self.__minuit.parameters):
                pv = self.__minuit.values[minuitname]
                dp_low = -self.__minuit.merrors[(minuitname, -1.0)]
                dp_high = self.__minuit.merrors[(minuitname, 1.0)]

                pvals.append(pv)
                perrs.append((dp_low, dp_high))
                logging.debug("  %s = %g -%g +%g"%(minuitname, pv,
                                                   dp_low, dp_high))
        else:
            logging.debug("Results with MIGRAD:")
            for minuitname in sorted(self.__minuit.parameters):
                pv = self.__minuit.values[minuitname]
                dp = self.__minuit.errors[minuitname]

                pvals.append(pv)
                perrs.append((dp, dp))

                logging.debug("  %s = %g -+%g"%(minuitname, pv, dp))

        #sca = self.tunedata.scaler
        #dim = self.tunedata.numParams()
        #scaled = numpy.NaN * numpy.zeros(dim)
        #for minuitname in sorted(self.__minuit.parameters):
            #scaled[i] = 
        #for pname, pval in self.__minuit.limits.iteritems():
        #unscaled = sca.descale(scaled)

        #print " those were the parameter limits used:\n", self.__minuit.limits

        mr = MinimizationResult.withScaler(self.__minuit.fval,
                                           self.tunedata.scaler, pvals,
                                           errscaled=perrs,
                                           covariance=self.__minuit.covariance)
        mr.ndof = self.tunedata.getNdof()

        return mr
