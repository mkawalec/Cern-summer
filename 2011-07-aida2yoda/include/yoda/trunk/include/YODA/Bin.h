// -*- C++ -*-
//
// This file is part of YODA -- Yet more Objects for Data Analysis
// Copyright (C) 2008-2011 The YODA collaboration (see AUTHORS for details)
//
#ifndef YODA_Bin_h
#define YODA_Bin_h

#include <string>
#include <utility>

namespace YODA {


  /// @brief Base class for bins in 1D and 2D histograms.
  /// This base class only provides very basic functionality for fill
  /// weight statistics access, as 1D/2D and basic/profile histos have
  /// quite difference implementations.
  class Bin {

  public:

    /// @name Miscellaneous
    //@{

    /// Reset this bin
    virtual void reset() = 0;

    //@}


  public:

    /// @name Fill statistics
    //@{

    /// The number of entries
    virtual unsigned long numEntries() const = 0;

    /// The sum of weights
    virtual double sumW() const = 0;

    /// The sum of weights squared
    virtual double sumW2() const = 0;

    //@}

  };


}



#endif
