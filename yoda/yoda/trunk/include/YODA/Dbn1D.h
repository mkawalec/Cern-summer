// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_Dbn1D_h
#define YODA_Dbn1D_h

#include "YODA/Exceptions.h"

namespace YODA {


  /// @brief A 1D distribution This class is used internally by YODA to
  /// centralise the calculation of statistics of unbounded, unbinned sampled
  /// distributions. Each distribution fill contributes a weight, \f$ w \f$, and
  /// a value, \f$ x \f$. By storing the total number of fills (ignoring
  /// weights), \f$ \sum w \f$, \f$ \sum w^2 \f$, \f$ \sum wx \f$,
  /// and \f$ \sum wx^2 \f$, the Dbn1D can calculate the mean and spread
  /// (\f$ \sigma^2 \f$, \f$ \sigma \f$ and \f$ \hat{\sigma} \f$) of the
  /// sampled distribution. It is used to provide this information in bins
  /// and for the "hidden" \f$ y \f$ distribution in profile histogram bins.
  class Dbn1D {
  public:

    /// Constructor.
    Dbn1D() {
      reset();
    }


    /// @name Modifiers
    //@{

    /// @brief Contribute a sample at @a val with weight @a weight.
    /// @todo Be careful about negative weights.
    void fill(double val, double weight=1.0);

    /// Reset the internal counters.
    void reset();

    /// Rescale as if all fill weights had been different by factor @a scalefactor.
    void scaleW(double scalefactor) {
      const double sf = scalefactor;
      const double sf2 = sf*sf;
      _sumW *= sf;
      _sumW2 *= sf2;
      _sumWX *= sf;
      _sumWX2 *= sf2;
    }

    /// Rescale the edges
    void scaleX(double factor) {
        _sumWX *= factor;
        _sumWX2 *= factor*factor;
    }

    //@}


  public:

    /// @name High-level info
    //@{

    // bool isUnfilled() const {
    //   return (numEntries() == 0);
    // }

    // bool isEmpty() const {
    //   return (sumW() == 0)
    // }

    //@}


    /// @name Distribution statistics
    //@{

    /// Weighted mean, \f$ \bar{x} \f$, of distribution.
    double mean() const;

    /// Weighted variance, \f$ \sigma^2 \f$, of distribution.
    double variance() const;

    /// Weighted standard deviation, \f$ \sigma \f$, of distribution.
    double stdDev() const;

    /// Weighted standard error, \f$ \sim \sigma/\sqrt{N-1} \f$, of distribution.
    double stdErr() const;

    //@}


    /// @name Raw distribution running sums
    //@{

    /// Number of entries (number of times @c fill was called, ignoring weights)
    unsigned long numEntries() const;

    /// Effective number of entries \f$ = (\sum w)^2 / \sum w^2 \f$
    double effNumEntries() const;

    /// The sum of weights
    double sumW() const;

    /// The sum of weights squared
    double sumW2() const;

    /// The sum of x*weight
    double sumWX() const;

    /// The sum of x^2 * weight
    double sumWX2() const;

    //@}

    /// Setters
    void setW(double sumW);
    void setW2(double sumW2);
    void setWX(double sumWX);
    void setWX2(double sumWX2);
    void setNumFills(double numFills);


  public:

    /// Add two dbns
    Dbn1D& operator += (const Dbn1D&);

    /// Subtract one dbn from another
    Dbn1D& operator -= (const Dbn1D&);


  protected:

    /// Add two dbns (internal, explicitly named version)
    Dbn1D& add(const Dbn1D&);

    /// Subtract one dbn from another (internal, explicitly named version)
    Dbn1D& subtract(const Dbn1D&);


  private:

    unsigned long _numFills;
    double _sumW;
    double _sumW2;
    double _sumWX;
    double _sumWX2;

  };


  /// Add two dbns
  Dbn1D operator + (const Dbn1D& a, const Dbn1D& b);

  /// Subtract one dbn from another
  Dbn1D operator - (const Dbn1D& a, const Dbn1D& b);


}

#endif
