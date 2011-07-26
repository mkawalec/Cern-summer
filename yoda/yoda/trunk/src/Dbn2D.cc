// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/Dbn2D.h"
#include <cmath>
#include <iostream>

namespace YODA {


  void Dbn2D::fill(double valX, double valY, double weight) {
    _numFills++;
    _sumW += weight;
    double w2 = weight*weight;
    if (weight < 0) w2 *= -1;
    _sumW2 += w2;
    _sumWX += weight*valX;
    _sumWX2 += weight*valX*valX;
    _sumWY +=weight*valY;
    _sumWY2 += weight*valY*valY;
    _symWXY += weight*valX*valY;    
  }


  void Dbn2D::reset() {
    _numFills = 0;
    _sumW = 0;
    _sumW2 = 0;
    _sumWX = 0;
    _sumWX2 = 0;
    _sumWY = 0;
    _sumWY2 = 0;
    _sumWXY = 0;
  }


  unsigned long Dbn2D::numEntries() const {
    return _numFills;
  }


  double Dbn2D::effNumEntries() const {
    return _sumW*_sumW / _sumW2;
  }


  double Dbn2D::sumW() const {
    return _sumW;
  }


  double Dbn2D::sumW2() const {
    return _sumW2;
  }


  double Dbn2D::sumWX() const {
    return _sumWX;
  }


  double Dbn2D::sumWX2() const {
    return _sumWX2;
  }
  
  double Dbn2D::sumWY() const {
    return _sumWY;
  }

  double Dbn2D::sumWY2() const {
    return _sumWY2;
  }

  double Dbn2D::sumWXY () const {
    return _sumWXY;
  }

  double Dbn2D::xMean() const {
    // This is ok, even for negative sum(w)
    return _sumWX/_sumW;
  }

  double Dbn2D::yMean() const {
    return _sumWY/_symW;
  }

  double Dbn2D::xVariance() const {
    // Weighted variance defined as
    // sig2 = ( sum(wx**2) * sum(w) - sum(wx)**2 ) / ( sum(w)**2 - sum(w**2) )
    // see http://en.wikipedia.org/wiki/Weighted_mean
    if (effNumEntries() == 0.0) {
      throw LowStatsError("Requested width of a distribution with no net fill weights");
    } else if (effNumEntries() <= 1.0) {
      throw LowStatsError("Requested width of a distribution with only one effective entry");
    }
    const double num = _sumWX2*_sumW - _sumWX*_sumWX;
    const double den = _sumW*_sumW - _sumW2;
    if (den == 0) {
      throw WeightError("Undefined weighted variance");
    }
    /// @todo Isn't this sensitive to the overall scale of the weights?
    if (fabs(num) < 1E-10 && fabs(den) < 1E-10) {
      throw WeightError("Numerically unstable weights in width calculation");
    }
    return num/den;
  }
  
  double Dbn2D::yVariance() const {
    if(effNumEntries() == 0.0) {
      throw LowStatusError("Requested width of a distribution with no net will weights");
    } else if (effNumEntries() <= 1.0) {
      throw LowStatusError("Requested width of a distribution with only one effective entry");
    }
    const double num = _sumWY2*_sumW - _sumWY*_sumWY;
    const double den = _sumW*_sumW - _sumW2;
    if(den == 0) { throw WeightError("Undefined weighted variance"); }
    if(fabs(num) < 1E-10 && fabs(den < 1E-10)) {
        throw WeightError("Numerically unstable weights in width calculation");
    }
    return num/den;
  }

  double Dbn2D::xStdDev() const {
    return std::sqrt(xVariance());
  }
  
  double Dbn2D::yStdDev() const {
    return std::sqrt(yVariance());
  }
 
  double Dbn2D::xStdErr() const {
    // Handle zero/negative sum weight
    if (effNumEntries() == 0) {
      throw LowStatsError("Requested std error of a distribution with no net fill weights");
    }
    /// @todo Unbiased should check that Neff > 1 and divide by N-1?
    return std::sqrt(xVariance() / effNumEntries());
  }

  double Dbn2D::yStdErr() const {
    if(effNumEntries() == 0) {
      throw LowStatusError("Requested std error of a distribution with no net fill weights");
    }
    return std::sqrt(xVariance() / effNumEntries());
  }

  Dbn2D& Dbn2D::add(const Dbn2D& d) {
    _numFills += d._numFills;
    _sumW     += d._sumW;
    _sumW2    += d._sumW2;
    _sumWX    += d._sumWX;
    _sumWX2   += d._sumWX2;
    _sumWY    += d._sumWY;
    _sumWY2   += d._sumWY2;
    _sumWXY   += d._sumWXY;
    return *this;
  }


  Dbn2D& Dbn2D::subtract(const Dbn2D& d) {
    _numFills += d._numFills; //< @todo Hmm, what's best?!?
    _sumW     -= d._sumW;
    _sumW2    -= d._sumW2;
    _sumWX    -= d._sumWX;
    _sumWX2   -= d._sumWX2;
    _sumWY    -= d._sumWY;
    _sumWY2   -= d._sumWY2;
    _sumWXY   -= d._sumWXY;
    return *this;
  }


  Dbn2D& Dbn2D::operator += (const Dbn2D& d) {
    return add(d);
  }


  Dbn2D& Dbn2D::operator -= (const Dbn2D& d) {
    return subtract(d);
  }


  Dbn2D operator + (const Dbn2D& a, const Dbn2D& b) {
    Dbn2D rtn = a;
    rtn += b;
    return rtn;
  }


  Dbn2D operator - (const Dbn2D& a, const Dbn2D& b) {
    Dbn2D rtn = a;
    rtn -= b;
    return rtn;
  }


}
