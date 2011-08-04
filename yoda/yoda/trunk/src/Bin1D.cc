// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#include "YODA/Bin1D.h"

#include <cassert>
#include <cmath>
using namespace std;

namespace YODA {


  Bin1D::Bin1D(double lowedge, double highedge)
    : _edges( make_pair(lowedge, highedge) )
  {
    assert( _edges.second > _edges.first );
  }


  Bin1D::Bin1D(std::pair<double, double> edges)
    : _edges( edges )
  {
    assert( _edges.second >= _edges.first );
  }


  void Bin1D::reset () {
    _xdbn.reset();
  }


  double Bin1D::lowEdge() const {
    return _edges.first;
  }


  double Bin1D::highEdge() const {
    return _edges.second;
  }


  pair<double,double> Bin1D::edges() const {
    return _edges;
  }


  double Bin1D::width() const {
    return _edges.second - _edges.first;
  }


  double Bin1D::focus() const {
    if (_xdbn.sumW() != 0) {
      return xMean();
    } else {
      return midpoint();
    }
  }


  double Bin1D::midpoint() const {
    return ( _edges.second + _edges.first ) / 2;
  }


  double Bin1D::xMean() const {
    return _xdbn.mean();
  }


  double Bin1D::xVariance() const {
    return _xdbn.variance();
  }


  double Bin1D::xStdDev() const {
    return _xdbn.stdDev();
  }


  double Bin1D::xStdError() const {
    return _xdbn.stdErr();
  }


  unsigned long Bin1D::numEntries() const {
    return _xdbn.numEntries();
  }


  double Bin1D::sumW() const {
    return _xdbn.sumW();
  }


  double Bin1D::sumW2() const {
    return _xdbn.sumW2();
  }


  double Bin1D::sumWX() const {
    return _xdbn.sumWX();
  }


  double Bin1D::sumWX2() const {
    return _xdbn.sumWX2();
  }

  void Bin1D::setW(double sumW)             {_xdbn.setW(sumW);}
  void Bin1D::setW2(double sumW2)           {_xdbn.setW2(sumW2);}
  void Bin1D::setWX(double sumWX)           {_xdbn.setWX(sumWX);}
  void Bin1D::setWX2(double sumWX2)         {_xdbn.setWX2(sumWX2);}
  void Bin1D::setNumFills(double numFills)  {_xdbn.setNumFills(numFills);}

  Bin1D& Bin1D::add(const Bin1D& b) {
    assert(_edges == b._edges);
    _xdbn += b._xdbn;
    return *this;
  }


  Bin1D& Bin1D::subtract(const Bin1D& b) {
    assert(_edges == b._edges);
    _xdbn -= b._xdbn;
    return *this;
  }


  Bin1D& Bin1D::operator += (const Bin1D& b) {
    return add(b);
  }


  Bin1D& Bin1D::operator -= (const Bin1D& b) {
    return subtract(b);
  }


  Bin1D operator + (const Bin1D& a, const Bin1D& b) {
    Bin1D rtn = a;
    rtn += b;
    return rtn;
  }


  Bin1D operator - (const Bin1D& a, const Bin1D& b) {
    Bin1D rtn = a;
    rtn -= b;
    return rtn;
  }


}
