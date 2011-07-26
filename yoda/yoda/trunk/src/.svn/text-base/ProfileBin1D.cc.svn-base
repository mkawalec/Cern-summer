// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/ProfileBin1D.h"
#include <cassert>

namespace YODA {


  ProfileBin1D::ProfileBin1D(double lowedge, double highedge)
    : Bin1D(lowedge, highedge)
  { }


  ProfileBin1D::ProfileBin1D(std::pair<double,double> edges)
    : Bin1D(edges)
  { }


  void ProfileBin1D::fill(double x, double d, double w) {
    assert( _edges.first < _edges.second );
    assert( x >= _edges.first && x < _edges.second );
    _xdbn.fill(x, w);
    _ydbn.fill(d, w);
  }


  void ProfileBin1D::fillBin(double d, double w) {
    _xdbn.fill(midpoint(), w);
    _ydbn.fill(d, w);
  }


  void ProfileBin1D::reset() {
    Bin1D::reset();
    _ydbn.reset();
  }


  ProfileBin1D& ProfileBin1D::add(const ProfileBin1D& pb) {
    Bin1D::add(pb);
    _ydbn += pb._ydbn;
    return *this;
  }


  ProfileBin1D& ProfileBin1D::subtract(const ProfileBin1D& pb) {
    Bin1D::subtract(pb);
    _ydbn -= pb._ydbn;
    return *this;
  }


  ProfileBin1D operator + (const ProfileBin1D& a, const ProfileBin1D& b) {
    ProfileBin1D rtn(a);
    rtn += a;
    return rtn;
  }


  ProfileBin1D operator - (const ProfileBin1D& a, const ProfileBin1D& b) {
    ProfileBin1D rtn(a);
    rtn -= a;
    return rtn;
  }


}
