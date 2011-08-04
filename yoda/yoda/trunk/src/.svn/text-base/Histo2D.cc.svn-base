// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/Histo2D.h"
#include "YODA/Scatter2D.h"

#include <cmath>
#include <iostream>
using namespace std;

namespace YODA {


  typedef vector<HistoBin2D> Bins;


  //TODO: It should return/throw something if no bin exist.
  //So, what is the concept of under/over flow in 2D case?
  int Histo2D::fill(double x, double y, double weight) {
    // Fill the normal bins
    int index = findBinIndex(x, y);
    //cout << index << endl;
    if(index != -1) {
      HistoBin2D& b = bin(index);
      
      // Fill the underflow and overflow nicely
      _axis.totalDbn().fill(x, y, weight);
    
      b.fill(x, y, weight);
    }
    else if (x < _axis.lowEdgeX()) { _axis.underflow().fill(x, y, weight); }
    else if (x >= _axis.highEdgeX()) { _axis.overflow().fill(x, y, weight); }
    return index;
  }

  double Histo2D::sumW(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().sumW();
    double sumw = 0;
    foreach (const Bin& b, bins()) {
      sumw += b.sumW();
    }
    return sumw;
  }


  double Histo2D::sumW2(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().sumW2();
    double sumw2 = 0;
    foreach (const Bin& b, bins()) {
      sumw2 += b.sumW2();
    }
    return sumw2;
  }


  double Histo2D::xMean(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().xMean();
    double sumwx = 0;
    double sumw  = 0;
    for (size_t i = 0; i < bins().size(); i++) {
      sumwx += bins().at(i).sumWX();
      sumw  += bins().at(i).sumW();
    }
    return sumwx/sumw;
  }

  double Histo2D::yMean(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().yMean();
    double sumwy = 0;
    double sumw = 0;
    for (size_t i = 0; i < bins().size(); i++) {
        sumwy += bins().at(i).sumWY();
        sumw  += bins().at(i).sumW();
    }
    return sumwy/sumw;
  }


  double Histo2D::xVariance(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().xVariance();
    double sigma2 = 0;
    const double xMean = this->xMean();
    foreach (const Bin2D& b, bins()) {
      const double diff = b.focus().first - xMean;
      sigma2 += diff * diff * b.sumW();
    }
    return sigma2/sumW();
  }

  double Histo2D::yVariance(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().yVariance();
    double sigma2 = 0;
    const double yMean = this->yMean();
    foreach (const Bin2D& b, bins()) {
      const double diff = b.focus().first - yMean;
      sigma2 += diff * diff * b.sumW();
    }
    return sigma2/sumW();
  }

  ////////////////////////////////////////

  /// Copy constructor with optional new path
  Histo2D::Histo2D(const Histo2D& h, const std::string& path)
    : AnalysisObject("Histo2D", (path.size() == 0) ? h.path() : path, h, h.title())
  {
    _axis = h._axis;
  }


  ///////////////////////////////////////


  /// Divide two histograms
  Scatter3D operator / (const Histo2D& numer, const Histo2D& denom) {
    assert(numer.getHash() == denom.getHash());
    Scatter3D tmp;
    for (size_t i = 0; i < numer.numBinsTotal(); ++i) {
      const HistoBin2D& b1 = numer.bin(i);
      const HistoBin2D& b2 = denom.bin(i);
      assert(fuzzyEquals(b1.focus().first, b2.focus().first));
      assert(fuzzyEquals(b1.focus().second, b2.focus().second));
      
      const double x = b1.focus().first;
      const double y = b1.focus().second;

      assert(fuzzyEquals(b1.xMin(), b2.xMin()));
      assert(fuzzyEquals(b1.xMax(), b2.xMax()));

      assert(fuzzyEquals(b1.yMin(), b2.yMin()));
      assert(fuzzyEquals(b1.yMax(), b2.yMax()));

      const double exminus = x - b1.xMin();
      const double explus = b1.xMax() - x;

      const double eyminus = y - b1.yMin();
      const double eyplus = b1.yMax() - y;

      assert(exminus >= 0);
      assert(explus >= 0);
      assert(eyminus >= 0);
      assert(eyplus >= 0);
      
      const double z = b1.height() / b2.height();
      const double ez = z * sqrt( sqr(b1.heightErr()/b1.height()) + sqr(b2.heightErr()/b2.height()) );
      tmp.addPoint(x, exminus, explus, y, eyminus, eyplus, z, ez, ez);
    }
    assert(tmp.numPoints() == numer.numBinsTotal());
    return tmp;
  }

}
