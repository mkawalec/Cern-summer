"""scipyminimizer.py

"""

import numpy
import scipy.optimize as sciopt

from baseminimizer import BaseMinimizer, _logger
from result import MinimizationResult

# idea for the scipy chi^2 function:
# it might not be necessary to reset the chi2 function every time when
# __currentdata changes. But I'm not sure.
#
class ScipyMinimizer(BaseMinimizer):
    def initMinimization(self):
        super(ScipyMinimizer, self).initMinimization()

        std = self.getData()
        filtereddata = []
        for bp in std.itervalues():
            if not bp.veto:
                filtereddata.append((bp.refbin.getYVal(),
                                     bp.refbin.getYErr(),
                                     bp.ipol))

        def chi2(p):
            r = .0
            for yval, yerr, ipol in filtereddata:
                r += ((yval - ipol.getValue(p))**2
                      /yerr**2)
            return r

        self.__chi2func = chi2

        _logger.debug("Built __chi2func.")

    def minimize(self):
        # return values:
        (xopt, fopt, dirc, iter_, funcalls, warnflag) = sciopt.fmin_powell(
                    self.__chi2func, self.getStartpoint(), full_output = 1)

        # work around scipy bug: in 1D the xopt has shape () instead of (1,)
        if xopt.shape == ():
            _logger.debug("reshaping xopt: %s"%(xopt))
            xopt = numpy.array([xopt])
            _logger.debug("reshaped xopt: %s"%(xopt))

        mr = MinimizationResult.withScaler(fopt, self.getScaler(), xopt)

        if warnflag == 2:
            _logger.warning("Minimization failed: Maximum number of"
                    " iterations reached! Proceeding anyway...")
        elif warnflag == 1:
            _logger.warning("Minimization failed: Maximum number of function"
                    " evalueations reached! Proceeding anyway...")
        else:
            _logger.info("Minimization succeded: Found chi^2 value:"
                    " %f"%(fopt))

        return mr
