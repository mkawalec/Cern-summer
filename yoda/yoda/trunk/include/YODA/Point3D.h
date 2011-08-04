// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_POINT3D_H
#define YODA_POINT3D_H

#include "YODA/Exceptions.h"
#include "YODA/Utils/MathUtils.h"
#include <utility>

namespace YODA {


  /// A 3D data point to be contained in a Scatter3D
  class Point3D {
  public:

    typedef std::pair<double,double> ValuePair;


    /// @name Constructors
    //@{

    // Default constructor
    Point3D() {  }


    /// Values with optional symmetric errors
    Point3D(double x, double y, double z, double ex=0.0, double ey=0.0, double ez=0.0)
      : _x(x), _y(y), _z(z)
    {
      _ex = std::make_pair(ex, ex);
      _ey = std::make_pair(ey, ey);
      _ez = std::make_pair(ez, ez);
    }


    /// Values with explicit asymmetric errors
    Point3D(double x, double y, double z,
            double exminus,
            double explus,
            double eyminus,
            double eyplus,
            double ezminus,
            double ezplus)
      : _x(x), _y(y), _z(z)
    {
      _ex = std::make_pair(exminus, explus);
      _ey = std::make_pair(eyminus, eyplus);
      _ez = std::make_pair(ezminus, ezplus);
    }
    
    /// Assymetric Errors given as vectors:
    Point3D(const double& x, 
            const double& y, 
            const double& z,
            const std::pair<double,double>& ex,
            const std::pair<double,double>& ey,
            const std::pair<double,double>& ez) {
        Point3D(x, y, z, ex.first, ex.second, ey.first, ey.second, ez.first, ez.second);
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

    /// Get z value
    double z() const { return _z;}

    /// Set z value
    void setZ(double z) { _z = z;}
    //@}

    ///Scaling
    void scale(double scaleX, double scaleY, double scaleZ) {
        setX(x()*scaleX);
        setY(y()*scaleY);
        setZ(z()*scaleZ);

        setXErr(xErrMinus()*scaleX, xErrPlus()*scaleX);
        setYErr(yErrMinus()*scaleY, yErrPlus()*scaleY);
        setZErr(zErrMinus()*scaleZ, zErrPlus()*scaleZ);
    }
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

    /// @name z error accessors
    //@{

    /// Get z-error values
    const std::pair<double,double>& zErrs() const {
      return _ez;
    }

    /// Get negative z-error value
    const double zErrMinus() const {
      return _ez.first;
    }

    /// Get positive z-error value
    const double zErrPlus() const {
      return _ez.second;
    }

    /// Get average z-error value
    double zErrAvg() const {
      return (_ez.first + _ez.second)/2.0;
    }

    /// Set szmmetric z error
    void setZErr(double ez) {
      _ez.first = ez;
      _ez.second = ez;
    }

    /// Set aszmmetric z error
    void setZErr(std::pair<double,double> ez) {
      _ez = ez;
    }

    /// Set aszmmetric z error
    void setZErr(double ezminus, double ezplus) {
      _ez.first = ezminus;
      _ez.second = ezplus;
    }

    /// Get value minus negative z-error
    const double zMin() const {
      return _z - _ez.first;
    }

    /// Get value plus positive z-error
    const double zMax() const {
      return _z + _ez.second;
    }

    //@}

  protected:

    /// @name Value and error variables
    //@{

    double _x;
    double _y;
    double _z;
    std::pair<double,double> _ex;
    std::pair<double,double> _ey;
    std::pair<double,double> _ez;

    //@}

  };



  /// @name Comparison operators
  //@{

  /// Equality operator
  inline bool operator==(const  Point3D& a, const YODA::Point3D& b) {
    const bool same_val =  fuzzyEquals(a.x(), b.x()) && fuzzyEquals(a.y(), b.y());
    const bool same_eminus =  fuzzyEquals(a.xErrMinus(), b.xErrMinus()) && 
                              fuzzyEquals(a.yErrMinus(), b.yErrMinus());
    const bool same_eplus =  fuzzyEquals(a.xErrPlus(), b.xErrPlus()) &&
                             fuzzyEquals(a.yErrPlus(), b.yErrPlus());
    return same_val && same_eminus && same_eplus;
  }

  /// Inequality operator
  inline bool operator!=(const  Point3D& a, const YODA::Point3D& b) {
    return !(a == b);
  }

  /// Less-than operator used to sort bins by x-first ordering
  inline bool operator<(const  Point3D& a, const YODA::Point3D& b) {
    if (! fuzzyEquals(a.x(), b.x())) {
      return a.x() < b.x();
    }
    if(!fuzzyEquals(a.y(), b.y())) {
      return a.y() < b.y();
    }
    if (! fuzzyEquals(a.xErrMinus(), b.xErrMinus())) {
      return a.xErrMinus() < b.xErrMinus();
    }
    if(!fuzzyEquals(a.yErrMinus(), b.yErrMinus())) {
      return a.yErrMinus() < b.yErrMinus();
    }
    if (! fuzzyEquals(a.xErrPlus(), b.xErrPlus())) {
      return a.xErrPlus() < b.xErrPlus();
    }
    if(!fuzzyEquals(a.yErrPlus(), b.yErrPlus())) {
      return a.yErrPlus() < b.yErrPlus();
    }
    return false;
  }

  /// Less-than-or-equals operator
  inline bool operator<=(const  Point3D& a, const YODA::Point3D& b) {
    if (a == b) return true;
    return a < b;
  }

  /// Greater-than operator
  inline bool operator>(const  Point3D& a, const YODA::Point3D& b) {
    return !(a <= b);
  }

  /// Greater-than-or-equals operator
  inline bool operator>=(const  Point3D& a, const YODA::Point3D& b) {
    return !(a < b);
  }

  //@}


}

#endif
