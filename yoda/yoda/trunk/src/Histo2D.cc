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

  //So, what is the concept of under/over flow in 2D case?
  void Histo2D::fill(double x, double y, double weight) {
    // Fill the underflow and overflow nicely
    _axis.totalDbn().fill(x, y, weight);
    if (x < _axis.lowEdgeX()) { _axis.underflow().fill(x, weight); return; }
    if (x >= _axis.highEdgeX()) { _axis.overflow().fill(x, weight); return; }
    // Fill the normal bins
    HistoBin2D& b = binByCoord(x, y);
    b.fill(x, y, weight);
  }

  //TODO: Make this thing cached (is it needed?(possibly not))
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
/*
  TODO:
  /// Copy constructor with optional new path
  Histo2D::Histo2D(const Histo2D& h, const std::string& path)
    : AnalysisObject("Histo2D", (path.size() == 0) ? h.path() : path, h, h.title())
  {
    _axis = h._axis;
  }

  /// Constructor from a Scatter2D's binning, with optional new path
  Histo2D::Histo2D(const Scatter3D& s, const std::string& path)
    : AnalysisObject("Histo2D", (path.size() == 0) ? s.path() : path, s, s.title())
  {
    std::vector<HistoBin2D> bins;
    for (Scatter2D::Points::const_iterator p = s.points().begin(); p != s.points().end(); ++p) {
      bins.push_back(HistoBin2D(p->xMin(), p->xMax()));
    }
    _axis = Axis2D<HistoBin2D>(bins);
  }
*/
  ///////////////////////////////////////

/* TODO!!

  /// Divide two histograms
  Scatter3D operator / (const Histo2D& numer, const Histo2D& denom) {
    assert(numer._axis == denom._axis);
    Scatter2D tmp;
    for (size_t i = 0; i < numer.numBins(); ++i) {
      const HistoBin2D& b1 = numer.bin(i);
      const HistoBin2D& b2 = denom.bin(i);
      assert(fuzzyEquals(b1.focus(), b2.focus()));
      const double x = b1.focus().first;
      assert(fuzzyEquals(b1.xMin(), b2.xMin()));
      assert(fuzzyEquals(b1.xMax(), b2.xMax()));

      const double y = b1.focus().second;
      assert(fuzzyEquals(b1.yMin(), b2.yMin()));
      assert(fuzzyEquals(b1.yMax(), b2.yMax()));

      const double exminus = x - b1.xMin();
      const double explus = b1.xMax() - x;

      const double eyminus = y - b1.yMin();
      const double explus = b1.yMax() - y;

      assert(exminus >= 0);
      assert(explus >= 0);
      assert(eyminus >= 0);
      assert(explus >= 0);
      
      const double z = b1.height() / b2.height();
      const double ez = z * sqrt( sqr(b1.heightError()/b1.height()) + sqr(b2.heightError()/b2.height()) );
      tmp.addPoint(x, exminus, explus, y, eyminus, eyplus, z, ez, ez);
    }
    assert(tmp.numPoints() == numer.numBins());
    return tmp;
  }

*/
}
