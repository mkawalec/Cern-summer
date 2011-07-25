// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_Histo2D_h
#define YODA_Histo2D_h

#include "YODA/AnalysisObject.h"
#include "YODA/HistoBin2D.h"
#include "YODA/Scatter3D.h"
#include "YODA/Axis2D.h"
#include "YODA/Exceptions.h"
#include <vector>
#include <string>
#include <map>

namespace YODA {


  /// Convenience typedef
  typedef Axis2D<HistoBin2D> Histo2DAxis;


  /// A  one-dimensional histogram.
  class Histo2D : public AnalysisObject {

  public:

    /// Convenience typedefs
    typedef Histo2DAxis Axis;
    typedef Axis::Bins Bins;


    /// @name Constructors
    //@{

    /// Constructor giving range and number of bins.
    /// @todo Remove binning enum stuff
    Histo2D(size_t nbinsX, double lowerX, double upperX,
            size_t nbinsY, double lowerY, double upperY,
            const std::string& path="", const std::string& title="")
      : AnalysisObject("Histo2D", path, title),
        _axis(nbinsX, lowerX, upperX,
              nbinsY, lowerY, upperY)
    { }

    /// @brief Constructor giving explicit bin edges.
    /// For n bins, binedges.size() == n+1, the last
    /// one being the upper bound of the last bin
    Histo2D(const std::pair<std::vector<double>, std::vector<double> >& binedges,
            const std::string& path="", const std::string& title="")
      : AnalysisObject("Histo2D", path, title),
        _axis(binedges)
    { }

    /// Copy constructor with optional new path
    Histo2D(const Histo2D& h, const std::string& path="");

    /// Constructor from a Scatter3D's binning, with optional new path
    Histo2D(const Scatter3D& s, const std::string& path="");


    //@}


  public:

    /// @name Persistency hooks
    //@{

    /// Get name of the analysis object type, for persisting
    std::string _aotype() const { return "Histo2D"; }

    /// Set the state of the histo object, for unpersisting
    /// @todo Need to set annotations (do that on AO), all-histo Dbns, and dbns for every bin. Delegate!
    // void _setstate() = 0;

    //@}


    /// @name Modifiers
    //@{

    /// Fill histo by value and weight
    void fill(double x, double weight=1.0);

    /// @brief Reset the histogram.
    /// Keep the binning but set all bin contents and related quantities to zero
    virtual void reset() {
      _axis.reset();
    }

    /// Rescale as if all fill weights had been different by factor @a scalefactor.
    void scaleW(double scalefactor) {
      _axis.scaleW(scalefactor);
    }

    //@}


  public:

    /// @name Bin accessors
    //@{

    /// Number of bins on this axis (not counting under/overflow)
    size_t numBinsX() const {
      return bins().at(0).size();
    }

    size_t numBinsY() const {
        return bins().size();
    }

    /// Low edge of this histo's axis
    double lowEdgeX() const {
      return _axis.lowEdgeX();
    }

    double lowEdgeY() const {
        return _axis.lowEdgeY();
    }

    /// High edge of this histo's axis
    double highEdgeX() const {
      return _axis.highEdgeX();
    }

    double highEdgeY() const {
        return _axis.highEdgeY();
    }

    /// Access the bin vector
    /// @todo Actually, it's a Histo
    Utils::sortedvector<Utils::sortedvector<YODA::HistoBin2D> >& bins() {
      return _axis.bins();
    }

    /// Access the bin vector (const version)
    const Utils::sortedvector<Utils::sortedvector<YODA::HistoBin2D> >& bins() const {
      return _axis.bins();
    }

    /// Access a bin by index (non-const version)
    HistoBin2D& bin(size_t indexX, size_t indexY) {
      return _axis.bins()[indexX][indexY];
    }

    /// Access a bin by index (const version)
    const HistoBin2D& bin(size_t indexX, size_t indexY) const {
      return _axis.bins()[indexX][indexY];
    }

    /// Access a bin by coordinate (non-const version)
    HistoBin2D& binByCoord(double x, double y) {
      return _axis.binByCoord(x, y);
    }

    /// Access a bin by coordinate (const version)
    const HistoBin2D& binByCoord(double x, double y) const {
      return _axis.binByCoord(x, y);
    }

    //@}


  public:

    /// @name Whole histo data
    //@{

    /// Get the total area of the histogram
    double integral(bool includeoverflows=true) const {
      return sumW(includeoverflows);
    }

    /// Get sum of weights in histo
    double sumW(bool includeoverflows=true) const;

    /// Get sum of squared weights in histo
    double sumW2(bool includeoverflows=true) const;

    /// Get the mean
    double mean(bool includeoverflows=true) const;

    /// Get the variance
    double variance(bool includeoverflows=true) const;

    /// Get the standard deviation
    double stdDev(bool includeoverflows=true) const {
      return std::sqrt(variance(includeoverflows));
    }

    //@}


  public:

    /// @name Adding and subtracting histograms
    //@{

    /// Add another histogram to this
    Histo2D& operator += (const Histo2D& toAdd) {
      _axis += toAdd._axis;
      return *this;
    }

    /// Subtract another histogram from this
    Histo2D& operator -= (const Histo2D& toSubtract) {
      _axis -= toSubtract._axis;
      return *this;
    }

    //@}


  private:

    /// @name Bin data
    //@{

    /// Definition of bin edges and contents
    Axis2D<HistoBin2D> _axis;

    //@}

  };


  /// @name Combining histos: global operators
  //@{

  /// Add two histograms
  inline Histo2D operator + (const Histo2D& first, const Histo2D& second) {
    Histo2D tmp = first;
    tmp += second;
    return tmp;
  }

  /// Subtract two histograms
  inline Histo2D operator - (const Histo2D& first, const Histo2D& second) {
    Histo2D tmp = first;
    tmp -= second;
    return tmp;
  }

  //@}


}

#endif
