// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_Bin1D_h
#define YODA_Bin1D_h

#include "YODA/Bin.h"
#include "YODA/Dbn1D.h"
#include <string>
#include <utility>

namespace YODA {


  /// @brief Base class for bins in 1D normal and profile histograms.
  /// The lower bin edge is inclusive. This base class provides no fill
  /// method, since the signatures for standard and profile histos differ.
  class Bin1D : public Bin {
  public:

    /// @name Constructors, giving bin low and high edges.
    //@{
    Bin1D(double lowedge, double highedge);

    Bin1D(std::pair<double,double> edges);
    //@}


    /// @name Miscellaneous
    //@{

    /// Reset this bin
    virtual void reset();

    //@}


  public:

    /// @name X-axis info
    //@{
    /// Lower limit of the bin (inclusive).
    double lowEdge() const;
    double xMin() const { return lowEdge(); }

    /// Upper limit of the bin (exclusive).
    double highEdge() const;
    double xMax() const { return highEdge(); }

    /// Get the {low,high} edges as an STL @c pair.
    std::pair<double,double> edges() const;

    /// Separation of low and high edges, i.e. high-low.
    double width() const;

    /// The mean position in the bin, or the midpoint if that is not available.
    double focus() const;

    /// Geometric centre of the bin, i.e. high+low/2.0
    double midpoint() const;
    //@}


  public:

    /// @name X distribution statistics
    //@{

    /// Mean value of x-values in the bin.
    double xMean() const;

    /// The variance of x-values in the bin.
    double xVariance() const;

    /// The standard deviation (spread) of x-values in the bin.
    double xStdDev() const;

    /// The standard error on the bin focus.
    double xStdError() const;
    //@}


  public:

    /// @name Raw x distribution statistics
    //@{

    /// The number of entries
    unsigned long numEntries() const;

    /// The sum of weights
    double sumW() const;

    /// The sum of weights squared
    double sumW2() const;

    /// The sum of x*weight
    double sumWX() const;

    /// The sum of x^2 * weight
    double sumWX2() const;

    //@}


  public:

    /// @name Operators
    //@{

    /// Add two bins
    Bin1D& operator += (const Bin1D&);

    /// Subtract one bin from another
    Bin1D& operator -= (const Bin1D&);
    //@}


  protected:

    /// @name Named operators
    //@{

    /// Add two bins (internal, explicitly named version)
    Bin1D& add(const Bin1D&);

    /// Subtract one bin from another (internal, explicitly named version)
    Bin1D& subtract(const Bin1D&);
    //@}


  protected:

    /// The bin limits
    std::pair<double,double> _edges;

    // Distribution of weighted x values
    Dbn1D _xdbn;

  };


  /// Add two bins
  Bin1D operator + (const Bin1D& a, const Bin1D& b);

  /// Subtract one bin from another
  Bin1D operator - (const Bin1D& a, const Bin1D& b);


  /// Bin1Ds are compared for axis sorting by lower edge position
  /// @todo Check for overlaps somewhere... on Axis1D, I guess.
  inline bool operator<(const Bin1D& a, const Bin1D& b) {
    return b.edges().first > a.edges().first;
  }


}



#endif
