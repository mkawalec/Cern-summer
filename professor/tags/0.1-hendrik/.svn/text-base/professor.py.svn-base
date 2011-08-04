#! /usr/bin/python

# 
# Author: Hendrik Hoeth <hendrik.hoeth@cern.ch>
# 
# professor is a MC tuning tool, based on the ideas described in "Tuning and
# Test of Fragmentation Models Based on Identified Particles and Precision
# Event Shape Data" (Z. Phys., C 73 (1996) 11-60) and earlier implemented and
# used by the Delphi collaboration.
# 
# The method and the original program was developed at the University of
# Wuppertal. Unfortunately the original Fortran code has grown in a historic
# way, depends on naglib for the singular value decomposition, uses hbook and
# zebra for all the I/O and doesn't run on current linux distributions anymore.
# So I decided to rewrite the program in python and use the HepML format for
# reading and writing distributions.
# 
# professor.py depends on
# 
# - Numeric  (pygsl and SciPy depend on Numeric)
# - libgsl and pygsl  (for the singular value decomposition)
# - SciPy  (for the chi^2 minimization)
# - PyXML  (for reading the data files)
# 


# 1. Read the data and the generated MC distributions
# 2. Fit the X_MC (p_1, ..., p_n) function to get the coeff. for each bin
# 3. minimise the chi^2
# 
# We need at least N = 1/2 * (n (n+3) + 2) parameter sets for the fit.

from pygsl.linalg import *
from pygsl._numobj import *
from scipy.optimize import fmin

class Distributions:
    def __init__(self):
        self.parameters()
        self.read()

    def read(self):
        """
        Instead of reading real data we just generate some toy numbers.
        This needs to be fixed.
        """
        data = []
        for i in range(len(self.params)):
            row = []
            for x in range(4):
                row.append(self.params[i][0] * x + self.params[i][1] * x**2)
            data.append(row)
        self.data = array(data, Float)

    def output(self):
        print self.data

    def parameters(self):
        None

class Data(Distributions):
    def parameters(self):
        self.params = array([[ 1. , 2.]], Float)

class MC(Distributions):
    def parameters(self):
        self.params = array([
                [0.9  , 2.1  ],
                [0.94 , 1.95 ],
                [1.0  , 1.9  ],
                [1.0  , 2.03 ],
                [1.05 , 2.05 ],
                [1.02 , 2.04 ],
                [1.1  , 2.0  ]], Float)



class Prediction:
    def __init__(self, data, mc):
        """
        In the class "Prediction" the Monte Carlo response is modelled
        as a quadratic function of the parameters which are to be tuned.
        The Monte Carlo response for each bin is described as
        X_mc (p_1, ..., p_n) = A_0 + \sum_1^n B_i p_i + \sum_1^n C_i p_i^2
                                   + \sum_1^(n-1) \sum_(i+1)^n D_ij p_i p_j
        p_1, ..., p_n are the parameters. The coefficients A_0, B_i, C_i, D_ij
        are calculated using a singular value decomposition in calc_coeff().
        get_prediction() uses these coefficients to predict the MC response
        for any parameter setting.
        """
        if (len(data.data[0,:]) != len(mc.data[0,:])):
            print "Data and MC have different number of bins!"
        self.nsets = len(mc.params[:,0])
        self.nparam = len(mc.params[0,:])

        self.calc_pmatrix()
        self.calc_coeff()

    def calc_pmatrixrow(self, params):
        """
        calc_pmatrixrow() takes a set of parameters and returns a vector
        which contains:
        [1 p_1 ... p_n p_1^2 ... p_n^2 p_1*p_2 p_1*p_3 ... p_(n-1)*p_n]
        """
        # 1  (for A_0)
        a = [1.]
        # p_i  (for B_i)
        for i in range(self.nparam):
            a.append(params[i])
        # p_i^2  (for C_i)
        for i in range(self.nparam):
            a.append(params[i]**2)
        # p_i * p_j  (for D_ij)
        for i in range(self.nparam - 1):
            for j in range(i+1, self.nparam):
                a.append(params[i]*params[j])
        return a

    def calc_pmatrix(self):
        """
        Loop over all sets of parameters used for generating the MC. For each
        set take calc_pmatrixrow and put it as a row into self.pmatrix. This
        matrix will then be used as 
        """
        pmatrix = []
        for set in range(self.nsets):
            a = self.calc_pmatrixrow(mc.params[set,:])
            pmatrix.append(a)

        self.pmatrix = array(pmatrix, Float)
        #print self.pmatrix

    def calc_coeff(self):
        """
        Solve pmatrix*coeff=b for each bin
        coeff is the vector of coefficients (A_0, B_i, C_i, D_ij)
        b is the MC response for the bin
        """
        self.coeff = []
        for bin in range(len(mc.data[0,:])):
            b = array(mc.data[:,bin], Float)
            #print b
            (u,v,s) = SV_decomp(self.pmatrix)
            coeff = SV_solve(u, v, s, b)
            self.coeff.append(coeff)
        self.coeff = array(self.coeff, Float)

    def get_prediction(self, bin, params):
        """
        get_prediction() uses the coefficients A_0, B_i, C_i and D_ij to
        predict the MC response for any parameter setting.
        """
        return sum (self.calc_pmatrixrow(params) * self.coeff[bin])


class Tune:
    def __init__(self, data, prediction):
        """
        The class "Tune" takes data and the MC prediction and
        optimizes the parameters to fit the data the best possible way.
        """
        print "Starting the optimization"

    def calc_chi2(self, params):
        """
        calc_chi2() calculates the chi^2 of the Monte Carlo
        prediction wrt the data. This is minimized in optimize().
        """
        # FIXME: We ignore the errors !!!!!!
        sigma = 1.
        chi2 = 0.
        for bin in range(len(data.data[0,:])):
            Xmc = prediction.get_prediction(bin, params)
            Xdata = data.data[0, bin]
            chi2 += (Xmc - Xdata)**2
        return chi2

    def optimize(self):
        """
        optimize() minimizes the chi^2 to find the parameter set
        that describes the data best. The used function fmin() is
        part of the SciPy packages and implements a simplex algorithm.
        As start value x0 for the fit we use the center of the
        tuning interval.
        """
        x0 = []
        for i in range(len(mc.params[0,:])):
            x0.append(1.*sum(mc.params[:,i])/len(mc.params[:,i]))
        xopt = fmin(self.calc_chi2, x0)
        print xopt


mc = MC()
data = Data()
#mc.output()
#data.output()

prediction = Prediction(data, mc)

tune = Tune(data, prediction)
tune.optimize()


