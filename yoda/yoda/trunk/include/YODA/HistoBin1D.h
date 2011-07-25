// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_HistoBin1D_h
#define YODA_HistoBin1D_h

#include "YODA/Bin1D.h"
#include "YODA/Exceptions.h"

namespace YODA {


  /// @brief A Bin in a 1D histogram
  class HistoBin1D : public Bin1D {

  public:

    /// @name Constructor giving bin low and high edges.
    //@{
    HistoBin1D(double lowedge, double highedge);
    HistoBin1D(std::pair<double,double> edges);
    //@}


  public:

    /// @name Modifiers
    //@{

    /// @brief Fill this bin with weight @a weight at position @a coord.
    void fill(double coord, double weight=1.0);

    /// @brief Fill this bin with weight @a weight.
    void fillBin(double weight=1.0);

    /// Reset this bin
    void reset() {
      Bin1D::reset();
    }

    /// Rescale as if all fill weights had been different by factor @a scalefactor.
    void scaleW(double scalefactor) {
      _xdbn.scaleW(scalefactor);
    }

    //@}


  public:

    /// @name Bin content info
    //@{
    /// The area is the sum of weights in the bin, i.e. the
    /// width of the bin has no influence on this figure.
    double area() const;

    /// The height is defined as area/width.
    double height() const;
    //@}

    /// @name Error info
    //@{

    /// Error computed using binomial statistics on the sum of bin weights,
    /// i.e. err_area = sqrt{sum{weights}}
    double areaError() const;

    /// As for the height vs. area, the height error includes a scaling factor
    /// of the bin width, i.e. err_height = sqrt{sum{weights}} / width.
    double heightError() const;

    //@}


  public:

    /// Add two bins (for use by Histo1D).
    HistoBin1D& operator += (const HistoBin1D&);

    /// Subtract two bins
    HistoBin1D& operator -= (const HistoBin1D&);


  protected:

    /// Add two bins (internal, explicitly named version)
    HistoBin1D& add(const HistoBin1D&);

    /// Subtract one bin from another (internal, explicitly named version)
    HistoBin1D& subtract(const HistoBin1D&);

  };


  /// Add two bins
  HistoBin1D operator + (const HistoBin1D& a, const HistoBin1D& b);

  /// Subtract two bins
  HistoBin1D operator - (const HistoBin1D& a, const HistoBin1D& b);


}

#endif
