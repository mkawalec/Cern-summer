// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/HistoBin2D.h"

#include <cassert>
using namespace std;

namespace YODA {


  //TODO: Implement a unified instantiation scheme
  HistoBin2D::HistoBin2D(double lowEdgeX, double highEdgeX,
                         double lowEdgeY, double highEdgeY)
    : Bin2D(lowEdgeX, lowEdgeY, highEdgeX, highEdgeY)
  { }


  HistoBin2D::HistoBin2D(std::vector<std::pair<std::pair<double,double>, std::pair<double,double> > >& edges)
    : Bin2D(edges)
  { }

  HistoBin2D::HistoBin2D() 
    : Bin2D()
  { }

  void HistoBin2D::fill(double x, double y, double w) {
    _dbn.fill(x,y,w);
  }

  void HistoBin2D::fill(std::pair<double,double> coords, double weight) {
    _dbn.fill(coords.first, coords.second, weight);
  }


  void HistoBin2D::fillBin(double weight) {
    _dbn.fill(midpoint(), weight);
  }


  HistoBin2D& HistoBin2D::add(const HistoBin2D& hb) {
    Bin2D::add(hb);
    return *this;
  }


  HistoBin2D& HistoBin2D::substract(const HistoBin2D& hb) {
    Bin2D::substract(hb);
    return *this;
  }


  HistoBin2D& HistoBin2D::operator += (const HistoBin2D& toAdd) {
    return add(toAdd);
  }


  HistoBin2D& HistoBin2D::operator -= (const HistoBin2D& toSubstract) {
    return substract(toSubstract);
  }


  HistoBin2D operator + (const HistoBin2D& a, const HistoBin2D& b) {
    HistoBin2D rtn(a);
    rtn += a;
    return rtn;
  }


  HistoBin2D operator - (const HistoBin2D& a, const HistoBin2D& b) {
    HistoBin2D rtn(a);
    rtn -= a;
    return rtn;
  }


}
