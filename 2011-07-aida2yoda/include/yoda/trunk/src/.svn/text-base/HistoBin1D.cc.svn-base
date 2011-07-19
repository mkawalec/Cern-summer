// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/HistoBin1D.h"

#include <cassert>
#include <cmath>
using namespace std;

namespace YODA {


  HistoBin1D::HistoBin1D(double low, double high)
    : Bin1D(low, high)
  { }


  HistoBin1D::HistoBin1D(std::pair<double, double> edges)
    : Bin1D(edges)
  { }


  void HistoBin1D::fill(double x, double w) {
    assert( _edges.first < _edges.second );
    assert( x >= _edges.first && x < _edges.second );
    _xdbn.fill(x, w);
  }


  void HistoBin1D::fillBin(double weight) {
    _xdbn.fill(midpoint(), weight);
  }


  double HistoBin1D::area() const
  {
    return sumW();
  }


  double HistoBin1D::height() const
  {
    return area() / width();
  }


  double HistoBin1D::areaError() const
  {
    return sqrt( sumW2() );
  }


  double HistoBin1D::heightError() const
  {
    return areaError() / width();
  }


  HistoBin1D& HistoBin1D::add(const HistoBin1D& hb) {
    Bin1D::add(hb);
    return *this;
  }


  HistoBin1D& HistoBin1D::subtract(const HistoBin1D& hb) {
    Bin1D::subtract(hb);
    return *this;
  }


  HistoBin1D& HistoBin1D::operator += (const HistoBin1D& toAdd) {
    return add(toAdd);
  }


  HistoBin1D& HistoBin1D::operator -= (const HistoBin1D& toSubtract) {
    return subtract(toSubtract);
  }


  HistoBin1D operator + (const HistoBin1D& a, const HistoBin1D& b) {
    HistoBin1D rtn(a);
    rtn += a;
    return rtn;
  }


  HistoBin1D operator - (const HistoBin1D& a, const HistoBin1D& b) {
    HistoBin1D rtn(a);
    rtn -= a;
    return rtn;
  }


}
