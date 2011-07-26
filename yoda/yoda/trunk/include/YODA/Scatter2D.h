// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_SCATTER2D_H
#define YODA_SCATTER2D_H

#include "YODA/AnalysisObject.h"
#include "YODA/Point2D.h"
#include "YODA/Utils/sortedvector.h"
#include <vector>
#include <set>
#include <string>
#include <utility>

namespace YODA {


  class Histo1D;
  class Profile1D;


  /// A very generic data type which is just a collection of 2D data points with errors
  class Scatter2D : public AnalysisObject {
  public:

    /// Type of the native Point2D collection
    typedef Utils::sortedvector<Point2D> Points;


    /// @name Constructors
    //@{

    Scatter2D(const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title)
    {  }


    Scatter2D(const Points& points,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title),
        _points(points)
    {  }

    /// @todo Add constructor from generic container/Range

    /// Values with no errors
    Scatter2D(const std::vector<double>& x, const std::vector<double>& y,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title)
    {
      assert(x.size() == y.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(x[i], y[i]);
      }
    }

    /// Values with symmetric errors on x and y
    Scatter2D(const std::vector<double>& x, const std::vector<double>& y,
              const std::vector<double>& ex, const std::vector<double>& ey,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title)
    {
      assert(x.size() == y.size() && x.size() == ex.size() && x.size() == ey.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(x[i], y[i], ex[i], ey[i]);
      }
    }

    /// Values with symmetric errors on x and asymmetric errors on y
    Scatter2D(const std::vector<double>& x, const std::vector<double>& y,
              const std::vector<double>& ex, const std::vector<std::pair<double,double> >& ey,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title)
    {
      assert(x.size() == y.size() && x.size() == ex.size() && x.size() == ey.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(Point2D(x[i], y[i], ex[i], ey[i]));
      }
    }

    /// Values with asymmetric errors on x and symmetric errors on y
    Scatter2D(const std::vector<double>& x, const std::vector<double>& y,
              const std::vector<std::pair<double,double> >& ex, const std::vector<double>& ey,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title)
    {
      assert(x.size() == y.size() && x.size() == ex.size() && x.size() == ey.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(Point2D(x[i], y[i], ex[i], ey[i]));
      }
    }

    /// Values with asymmetric errors on both x and y
    Scatter2D(const std::vector<double>& x, const std::vector<double>& y,
              const std::vector<std::pair<double,double> >& ex, const std::vector<std::pair<double,double> >& ey,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title)
    {
      assert(x.size() == y.size() && x.size() == ex.size() && x.size() == ey.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(Point2D(x[i], y[i], ex[i], ey[i]));
      }
    }

    /// Values with completely explicit asymmetric errors
    Scatter2D(const std::vector<double>& x, const std::vector<double>& y,
              const std::vector<double>& exminus,
              const std::vector<double>& explus,
              const std::vector<double>& eyminus,
              const std::vector<double>& eyplus,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter2D", path, title)
    {
      assert(x.size() == y.size() &&
             x.size() == exminus.size() && x.size() == explus.size() &&
             x.size() == eyminus.size() && x.size() == eyplus.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(Point2D(x[i], exminus[i], explus[i], y[i], eyminus[i], eyplus[i]));
      }
    }

    //@}


    /// Clear all points
    void reset() {
      _points.clear();
    }


    /// @name Persistency hooks
    //@{

    /// Set the state of the profile object, for unpersisting
    /// @todo Need to set annotations (do that on AO), all-histo Dbns, and dbns for every bin. Delegate!
    // void _setstate() = 0;

    //@}


    ///////////////////////////////////////////////////

    /// @name Point accessors
    //@{

    size_t numPoints() const {
      return _points.size();
    }


    const Points& points() const {
      return _points;
    }


    Point2D& point(size_t index) {
      assert(index < numPoints());
      return _points.at(index);
    }


    const Point2D& point(size_t index) const {
      assert(index < numPoints());
      return _points.at(index);
    }

    //@}


    /// @name Point adders
    //@{

    Scatter2D& addPoint(const Point2D& pt) {
      _points.insert(pt);
      return *this;
    }

    Scatter2D& addPoint(double x, double y) {
      _points.insert(Point2D(x, y));
      return *this;
    }

    Scatter2D& addPoint(double x, double y, double ex, double ey) {
      _points.insert(Point2D(x, y, ex, ey));
      return *this;
    }

    Scatter2D& addPoint(double x, double y, std::pair<double,double> ex, double ey) {
      _points.insert(Point2D(x, y, ex, ey));
      return *this;
    }

    Scatter2D& addPoint(double x, double y, double ex, std::pair<double,double> ey) {
      _points.insert(Point2D(x, y, ex, ey));
      return *this;
    }

    Scatter2D& addPoint(double x, double y, std::pair<double,double> ex, std::pair<double,double> ey) {
      _points.insert(Point2D(x, y, ex, ey));
      return *this;
    }

    Scatter2D& addPoint(double x, double exminus, double explus,
                        double y, double eyminus, double eyplus) {
      _points.insert(Point2D(x, exminus, explus, y, eyminus, eyplus));
      return *this;
    }

    Scatter2D& addPoints(Points pts) {
      foreach (const Point2D& pt, pts) {
        addPoint(pt);
      }
      return *this;
    }

    //@}


    /// @todo Better name?
    Scatter2D& combineWith(const Scatter2D& other) {
      addPoints(other.points());
      return *this;
    }


    /// @todo Better name?
    /// @todo Convert to accept a Range or generic
    Scatter2D& combineWith(const std::vector<Scatter2D>& others) {
      foreach (const Scatter2D& s, others) {
        combineWith(s);
      }
      return *this;
    }


  private:

    Points _points;

    std::string _myaotype;

  };



  inline Scatter2D combine(const Scatter2D& a, const Scatter2D& b) {
    Scatter2D rtn = a;
    rtn.combineWith(b);
    return rtn;
  }


  inline Scatter2D combine(const std::vector< Scatter2D >& scatters) {
    Scatter2D rtn;
    for (std::vector<Scatter2D>::const_iterator s = scatters.begin();
         s != scatters.end(); ++s) {
      rtn.combineWith(*s);
    }
    return rtn;
  }


  //////////////////////////////////


  /// @name Conversion functions from other data types
  //@{

  /// Make a Scatter2D representation of a Histo1D
  Scatter2D mkScatter(const Histo1D& h);

  /// Make a Scatter2D representation of a Profile1D
  Scatter2D mkScatter(const Profile1D& p);

  //@}


  /////////////////////////////////


  /// @name Combining scatters: global operators, assuming aligned points
  //@{

  /// Add two scatters
  inline Scatter2D operator + (const Scatter2D& first, const Scatter2D& second);

  /// Subtract two scatters
  inline Scatter2D operator - (const Scatter2D& first, const Scatter2D& second);

  /// Divide two scatters
  Scatter2D operator / (const Scatter2D& numer, const Scatter2D& denom);

  //@}


}

#endif
