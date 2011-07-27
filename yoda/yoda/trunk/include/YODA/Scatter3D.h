// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_SCATTER3D_H
#define YODA_SCATTER3D_H

#include "YODA/AnalysisObject.h"
#include "YODA/Point3D.h"
#include "YODA/Utils/sortedvector.h"
#include <vector>
#include <set>
#include <string>
#include <utility>

namespace YODA {


  class Histo3D;


  /// A very generic data type which is just a collection of 3D data points with errors
  class Scatter3D : public AnalysisObject {
  public:

    /// Type of the native Point3D collection
    typedef Utils::sortedvector<Point3D> Points;


    /// @name Constructors
    //@{

    Scatter3D(const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter3D", path, title)
    {  }


    Scatter3D(const Points& points,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter3D", path, title),
        _points(points)
    {  }


    /// Values with asymmetric errors on both x and y
    Scatter3D(const std::vector<double>& x, const std::vector<double>& y, const std::vector<double>& z,
              const std::vector<std::pair<double,double> >& ex, const std::vector<std::pair<double,double> >& ey, const std::vector<std::pair<double,double> >& ez,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter3D", path, title)
    {
      assert(x.size() == y.size() && x.size() == ex.size() && x.size() == ey.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(Point3D(x[i], y[i], z[i], ex[i], ey[i], ez[i]));
      }
    }

    /// Values with no errors:
    Scatter3D(const std::vector<double>& x, const std::vector<double>& y, const std::vector<double>& z,
              const std::string& path="", const std::string& title="") {
        std::vector<std::pair<double,double> > null;
        null.resize(x.size());

        for(unsigned int i=0; i < null.size(); i++) null[i] = std::make_pair(0.0, 0.0);
        Scatter3D(x, y, z, null, null, null, path, title);
    }

    /// Values with completely explicit asymmetric errors
    Scatter3D(const std::vector<double>& x, const std::vector<double>& y, const std::vector<double> z,
              const std::vector<double>& exminus,
              const std::vector<double>& explus,
              const std::vector<double>& eyminus,
              const std::vector<double>& eyplus,
              const std::vector<double>& ezminus,
              const std::vector<double>& ezplus,
              const std::string& path="", const std::string& title="")
      : AnalysisObject("Scatter3D", path, title)
    {
      assert(x.size() == y.size() == z.size() &&
             x.size() == exminus.size() && x.size() == explus.size() &&
             y.size() == eyminus.size() && y.size() == eyplus.size() &&
             z.size() == ezminus.size() && z.size() == ezplus.size());
      for (size_t i = 0; i < x.size(); ++i) {
        addPoint(Point3D(x[i], exminus[i], explus[i], y[i], eyminus[i], eyplus[i], z[i], ezminus[i], ezplus[i]));
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


    Point3D& point(size_t index) {
      assert(index < numPoints());
      return _points.at(index);
    }


    const Point3D& point(size_t index) const {
      assert(index < numPoints());
      return _points.at(index);
    }

    //@}


    /// @name Point adders
    //@{

    Scatter3D& addPoint(const Point3D& pt) {
      _points.insert(pt);
      return *this;
    }

    Scatter3D& addPoint(double x, double y, double z) {
      _points.insert(Point3D(x, y, z));
      return *this;
    }

    Scatter3D& addPoint(double x, double y, double z, 
                        std::pair<double,double> ex, std::pair<double,double> ey, std::pair<double,double> ez) {
      _points.insert(Point3D(x, y, z, ex, ey, ez));
      return *this;
    }

    Scatter3D& addPoint(double x, double exminus, double explus,
                        double y, double eyminus, double eyplus,
                        double z, double ezminus, double ezplus) {
      _points.insert(Point3D(x, exminus, explus, y, eyminus, eyplus, z, ezminus, ezplus));
      return *this;
    }

    Scatter3D& addPoints(Points pts) {
      foreach (const Point3D& pt, pts) {
        addPoint(pt);
      }
      return *this;
    }

    //@}


    /// @todo Better name?
    Scatter3D& combineWith(const Scatter3D& other) {
      addPoints(other.points());
      return *this;
    }


    /// @todo Better name?
    /// @todo Convert to accept a Range or generic
    Scatter3D& combineWith(const std::vector<Scatter3D>& others) {
      foreach (const Scatter3D& s, others) {
        combineWith(s);
      }
      return *this;
    }


  private:

    Points _points;

    std::string _myaotype;

  };



  inline Scatter3D combine(const Scatter3D& a, const Scatter3D& b) {
    Scatter3D rtn = a;
    rtn.combineWith(b);
    return rtn;
  }


  inline Scatter3D combine(const std::vector< Scatter3D >& scatters) {
    Scatter3D rtn;
    for (std::vector<Scatter3D>::const_iterator s = scatters.begin();
         s != scatters.end(); ++s) {
      rtn.combineWith(*s);
    }
    return rtn;
  }


  //////////////////////////////////


  /// @name Conversion functions from other data types
  //@{

  /// Make a Scatter3D representation of a Histo1D
  Scatter3D mkScatter(const Histo3D& h);

  //@}


}

#endif
