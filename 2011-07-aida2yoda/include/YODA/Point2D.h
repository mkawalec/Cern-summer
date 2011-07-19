// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_POINT2D_H
#define YODA_POINT2D_H

#include "YODA/Exceptions.h"
#include "YODA/Utils/MathUtils.h"
#include <utility>

namespace YODA {


  /// A 2D data point to be contained in a Scatter2D
  class Point2D {
  public:

    typedef std::pair<double,double> ValuePair;


    /// @name Constructors
    //@{

    // Default constructor
    Point2D() {  }


    /// Values with optional symmetric errors
    Point2D(double x, double y, double ex=0.0, double ey=0.0)
      : _x(x), _y(y)
    {
      _ex = std::make_pair(ex, ex);
      _ey = std::make_pair(ey, ey);
    }


    /// Values with explicit asymmetric errors
    Point2D(double x, double y,
            double exminus,
            double explus,
            double eyminus,
            double eyplus)
      : _x(x), _y(y)
    {
      _ex = std::make_pair(exminus, explus);
      _ey = std::make_pair(eyplus, eyplus);
    }


    /// Values with symmetric errors on x and asymmetric errors on y
    Point2D(double x, double y, double ex, const std::pair<double,double>& ey)
      : _x(x), _y(y), _ey(ey)
    {
      _ex = std::make_pair(ex, ex);
    }


    /// Values with asymmetric errors on x and symmetric errors on y
    Point2D(double x, double y, const std::pair<double,double>& ex, double ey)
      : _x(x), _y(y), _ex(ex)
    {
      _ey = std::make_pair(ey, ey);
    }


    /// Values with asymmetric errors on both x and y
    Point2D(double x, double y, const std::pair<double,double>& ex, const std::pair<double,double>& ey)
      : _x(x), _y(y), _ex(ex), _ey(ey)
    {
    }

    //@}


  public:

    /// @name Value and error accessors
    //@{

    /// Get x value
    double x() const { return _x; }

    /// Set x value
    void setX(double x) { _x = x; }

    /// Get y value
    double y() const { return _y; }

    /// Set y value
    void setY(double y) { _y = y; }

    //@}


    /// @name x error accessors
    //@{

    /// Get x-error values
    const std::pair<double,double>& xErrs() const {
      return _ex;
    }

    /// Get negative x-error value
    const double xErrMinus() const {
      return _ex.first;
    }

    /// Get positive x-error value
    const double xErrPlus() const {
      return _ex.second;
    }

    /// Get average x-error value
    double xErrAvg() const {
      return (_ex.first + _ex.second)/2.0;
    }

    /// Set symmetric x error
    void setXErr(double ex) {
      _ex.first = ex;
      _ex.second = ex;
    }

    /// Set asymmetric x error
    void setXErr(std::pair<double,double> ex) {
      _ex = ex;
    }

    /// Set asymmetric x error
    void setXErr(double exminus, double explus) {
      _ex.first = exminus;
      _ex.second = explus;
    }

    /// Get value minus negative x-error
    const double xMin() const {
      return _x - _ex.first;
    }

    /// Get value plus positive x-error
    const double xMax() const {
      return _x + _ex.second;
    }

    //@}


    /// @name y error accessors
    //@{

    /// Get y-error values
    const std::pair<double,double>& yErrs() const {
      return _ey;
    }

    /// Get negative y-error value
    const double yErrMinus() const {
      return _ey.first;
    }

    /// Get positive y-error value
    const double yErrPlus() const {
      return _ey.second;
    }

    /// Get average y-error value
    double yErrAvg() const {
      return (_ey.first + _ey.second)/2.0;
    }

    /// Set symmetric y error
    void setYErr(double ey) {
      _ey.first = ey;
      _ey.second = ey;
    }

    /// Set asymmetric y error
    void setYErr(std::pair<double,double> ey) {
      _ey = ey;
    }

    /// Set asymmetric y error
    void setYErr(double eyminus, double eyplus) {
      _ey.first = eyminus;
      _ey.second = eyplus;
    }

    /// Get value minus negative y-error
    const double yMin() const {
      return _y - _ey.first;
    }

    /// Get value plus positive y-error
    const double yMax() const {
      return _y + _ey.second;
    }

    //@}


  protected:

    /// @name Value and error variables
    //@{

    double _x;
    double _y;
    std::pair<double,double> _ex;
    std::pair<double,double> _ey;

    //@}

  };



  /// @name Comparison operators
  //@{

  /// Equality test of x characteristics only
  inline bool operator==(const YODA::Point2D& a, const YODA::Point2D& b) {
    const bool same_val = YODA::fuzzyEquals(a.x(), b.x());
    const bool same_eminus = YODA::fuzzyEquals(a.xErrMinus(), b.xErrMinus());
    const bool same_eplus = YODA::fuzzyEquals(a.xErrPlus(), b.xErrPlus());
    return same_val && same_eminus && same_eplus;
  }

  /// Equality test of x characteristics only
  inline bool operator!=(const YODA::Point2D& a, const YODA::Point2D& b) {
    return !(a == b);
  }

  /// Less-than operator used to sort bins by x-ordering
  inline bool operator<(const YODA::Point2D& a, const YODA::Point2D& b) {
    if (!YODA::fuzzyEquals(a.x(), b.x())) {
      return a.x() < b.x();
    }
    if (!YODA::fuzzyEquals(a.xErrMinus(), b.xErrMinus())) {
      return a.xErrMinus() < b.xErrMinus();
    }
    if (!YODA::fuzzyEquals(a.xErrPlus(), b.xErrPlus())) {
      return a.xErrPlus() < b.xErrPlus();
    }
    return false;
  }

  /// Less-than-or-equals operator used to sort bins by x-ordering
  inline bool operator<=(const YODA::Point2D& a, const YODA::Point2D& b) {
    if (a == b) return true;
    return a < b;
  }

  /// Greater-than operator used to sort bins by x-ordering
  inline bool operator>(const YODA::Point2D& a, const YODA::Point2D& b) {
    return !(a <= b);
  }

  /// Greater-than-or-equals operator used to sort bins by x-ordering
  inline bool operator>=(const YODA::Point2D& a, const YODA::Point2D& b) {
    return !(a < b);
  }

  //@}


}

#endif
