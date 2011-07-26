// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/Profile1D.h"
#include "YODA/Histo1D.h"
#include "YODA/Scatter2D.h"

#include <cmath>
#include <iostream>

using namespace std;

namespace YODA {


  typedef vector<ProfileBin1D> Bins;


  void Profile1D::fill(double x, double y, double weight) {
    /// @todo Fill the underflow and overflow nicely
    ProfileBin1D& b = binByCoord(x);
    b.fill(x, y, weight);
  }


  double Profile1D::sumW(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().sumW();
    double sumw = 0;
    for (Bins::const_iterator b = bins().begin(); b != bins().end(); ++b) {
      sumw += b->sumW();
    }
    return sumw;
  }


  double Profile1D::sumW2(bool includeoverflows) const {
    if (includeoverflows) return _axis.totalDbn().sumW2();
    double sumw2 = 0;
    for (Bins::const_iterator b = bins().begin(); b != bins().end(); ++b) {
      sumw2 += b->sumW2();
    }
    return sumw2;
  }


  ////////////////////////////////////////


  /// Copy constructor with optional new path
  Profile1D::Profile1D(const Profile1D& p, const std::string& path)
    : AnalysisObject("Profile1D", (path.size() == 0) ? p.path() : path, p, p.title())
  {
    _axis = p._axis;
  }


  /// Constructor from a Scatter2D's binning, with optional new path
  Profile1D::Profile1D(const Scatter2D& s, const std::string& path)
    : AnalysisObject("Profile1D", (path.size() == 0) ? s.path() : path, s, s.title())
  {
    std::vector<ProfileBin1D> bins;
    for (Scatter2D::Points::const_iterator p = s.points().begin(); p != s.points().end(); ++p) {
      bins.push_back(ProfileBin1D(p->xMin(), p->xMax()));
    }
    _axis = Profile1DAxis(bins);
  }


  /// Constructor from a Histo1D's binning, with optional new path
  Profile1D::Profile1D(const Histo1D& h, const std::string& path)
    : AnalysisObject("Profile1D", (path.size() == 0) ? h.path() : path, h, h.title())
  {
    Bins bins;
    for (Histo1D::Bins::const_iterator b = h.bins().begin(); b != h.bins().end(); ++b) {
      bins.insert(ProfileBin1D(b->xMin(), b->xMax()));
    }
    _axis = Profile1DAxis(bins);

  }


  ////////////////////////////////////////


  /// Divide two profile histograms
  Scatter2D operator / (const Profile1D& numer, const Profile1D& denom) {
    //assert(numer._axis == denom._axis);
    Scatter2D tmp;
    for (size_t i = 0; i < numer.numBins(); ++i) {
      const ProfileBin1D& b1 = numer.bin(i);
      const ProfileBin1D& b2 = denom.bin(i);
      assert(fuzzyEquals(b1.focus(), b2.focus()));
      const double x = b1.focus();
      assert(fuzzyEquals(b1.xMin(), b2.xMin()));
      assert(fuzzyEquals(b1.xMax(), b2.xMax()));
      const double exminus = x - b1.xMin();
      const double explus = b1.xMax() - x;
      assert(exminus >= 0);
      assert(explus >= 0);
      //
      const double y = b1.mean() / b2.mean();
      const double ey = y * sqrt( sqr(b1.stdErr()/b1.mean()) + sqr(b2.stdErr()/b2.mean()) );
      tmp.addPoint(x, exminus, explus, y, ey, ey);
    }
    assert(tmp.numPoints() == numer.numBins());
    return tmp;
  }


}
