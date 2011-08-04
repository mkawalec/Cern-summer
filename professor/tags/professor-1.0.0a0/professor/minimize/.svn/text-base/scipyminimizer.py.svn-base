"""
Interface to the minimizer objects in the SciPy library.
"""

import numpy
import scipy.optimize as sciopt

from professor.tools import log as logging
from professor.minimize.baseminimizer import BaseMinimizer
from professor.minimize.result import MinimizationResult


class ScipyMinimizer(BaseMinimizer):

    def validateResult(self, *args):
        """Raise an exception to show that validation is not working."""
        raise RuntimeError("ScipyMinimizer does not support validating results!")


    def initMinimization(self):
        ## This isn't doing anything for the moment, might change in the future.
        super(ScipyMinimizer, self).initMinimization()
        self.__chi2func = self.tunedata.getChi2Function()


    def minimize(self):
        xopt, fopt, dirc, iter_, funcalls, warnflag = \
            sciopt.fmin_powell(self.__chi2func, self.getStartpoint(), full_output = 1)

        ## Work around SciPy bug: in 1D the xopt has shape () instead of (1,)
        if xopt.shape == ():
            logging.debug("Reshaping xopt: %s" % xopt)
            xopt = numpy.array([xopt])
            logging.debug("Reshaped xopt: %s" % xopt)

        mr = MinimizationResult.withScaler(fopt, self.tunedata.getNdof(),
                                           self.tunedata.scaler, xopt)
        if warnflag == 2:
            logging.warning("Minimization failed: Maximum number of"
                    " iterations reached! Proceeding anyway...")
        elif warnflag == 1:
            logging.warning("Minimization failed: Maximum number of function"
                    " evaluations reached! Proceeding anyway...")
        else:
            logging.info("Minimization succeeded: Found chi^2 value: %e" % fopt)
        return mr
