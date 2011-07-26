// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_ProfileBin1D_h
#define YODA_ProfileBin1D_h

#include "YODA/Bin1D.h"
#include "YODA/Exceptions.h"

namespace YODA {


  /// A Bin in a 1D profile histogram.
  class ProfileBin1D : public Bin1D {

    /// Profile1D is a friend to add/subtract bins
    friend class Profile1D;


  public:

    /// @name Constructors
    //@{

    /// Constructor giving bin low and high edges.
    ProfileBin1D(double lowedge, double highedge);

    /// Constructor giving bin low and high edges as a pair.
    ProfileBin1D(std::pair<double,double> edges);

    //@}


    /// @name Modifiers
    //@{

    /// Fill histo by value and weight.
    void fill(double x, double d, double weight=1.0);

    /// Fill histo with @a weight at bin midpoint.
    void fillBin(double d, double weight=1.0);

    /// Reset the bin.
    void reset();

    /// Rescale as if all fill weights had been different by factor @a scalefactor.
    void scaleW(double scalefactor) {
      _xdbn.scaleW(scalefactor);
      _ydbn.scaleW(scalefactor);
    }

    //@}


  public:

    /// @name Bin content info
    //@{

    double mean() const {
      return _ydbn.mean();
    }

    double stdDev() const {
      return _ydbn.stdDev();
    }

    double variance() const {
      return _ydbn.variance();
    }

    double stdErr() const {
      return _ydbn.stdErr();
    }

    //@}


  public:

    /// Add two bins (for use by Profile1D).
    ProfileBin1D& operator += (const ProfileBin1D& toAdd) {
      return add(toAdd);
    }

    /// Subtract two bins
    ProfileBin1D& operator -= (const ProfileBin1D& toSubtract) {
      return subtract(toSubtract);
    }


  protected:

    /// Add two bins (internal, explicitly named version)
    ProfileBin1D& add(const ProfileBin1D&);

    /// Subtract one bin from another (internal, explicitly named version)
    ProfileBin1D& subtract(const ProfileBin1D&);


  public:

    /// The sum of y*weight
    double sumWY() const {
      return _ydbn.sumWX();
    }

    /// The sum of y^2 * weight
    double sumWY2() const {
      return _ydbn.sumWX2();
    }


  private:

    // Distribution of weighted data values
    Dbn1D _ydbn;


  };


  ProfileBin1D operator + (const ProfileBin1D& a, const ProfileBin1D& b);

  ProfileBin1D operator - (const ProfileBin1D& a, const ProfileBin1D& b);

}

#endif
