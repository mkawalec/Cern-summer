// -*- C++ -*-
#ifndef LWH_Axis_H
#define LWH_Axis_H
//
// This is the declaration of the Axis class representing
//


#include <limits>
#include <cmath>
#include <algorithm>
#include "AIAxis.h"

namespace LWH {

using namespace AIDA;

/**
 * An Axis represents a binned histogram axis. A 1D Histogram would have
 * one Axis representing the X axis, while a 2D Histogram would have two
 * axes representing the X and Y Axis.
 */
class Axis: public IAxis {

public:

  /**
   * Standard constructor.
   */
  Axis(int n, double lo, double up)
    : lower(lo), upper(up), nbins(n) {}

  /**
   * Copy constructor.
   */
  Axis(const Axis & a)
    : IAxis(a), lower(a.lower), upper(a.upper), nbins(a.nbins) {}

  /// Destructor.
  virtual ~Axis() { }

  /**
   * Check if the IAxis has fixed binning, i.e. if all the bins have
   * the same width.  @return <code>true</code> if the binning is
   * fixed, <code>false</code> otherwise.
   *
   */
  bool isFixedBinning() const {return true; }

  /**
   * Get the lower edge of the IAxis.
   * @return The IAxis's lower edge.
   *
   */
  double lowerEdge() const { return lower; }

  /**
   * Get the upper edge of the IAxis.
   * @return The IAxis's upper edge.
   *
   */
  double upperEdge() const { return upper; }

  /**
   * The number of bins (excluding underflow and overflow) on the IAxis.
   * @return The IAxis's number of bins.
   *
   */
  int bins() const { return nbins; }

  /**
   * Get the lower edge of the specified bin.
   * @param index The bin number: 0 to bins()-1 for the in-range bins
   * or OVERFLOW or UNDERFLOW.
   * @return The lower edge of the corresponding bin; for the
   * underflow bin this is <tt>Double.NEGATIVE_INFINITY</tt>.
   *
   */
  double binLowerEdge(int index) const {
    return index < 0? -std::numeric_limits<double>::max():
      lower + double(std::min(index, nbins))*binWidth(0);
  }

  /**
   * Get the upper edge of the specified bin.
   * @param index The bin number: 0 to bins()-1 for the in-range bins
   * or OVERFLOW or UNDERFLOW.
   * @return The upper edge of the corresponding bin; for the overflow
   * bin this is <tt>Double.POSITIVE_INFINITY</tt>.
   *
   */
  double binUpperEdge(int index) const {
    return index >= nbins? std::numeric_limits<double>::max():
      lower + double(std::max(index, -1) + 1)*binWidth(0);
  }

  /**
   * Get the width of the specified bin.
   * The argument gives the bin number: 0 to bins()-1) for the in-range bins
   * or OVERFLOW or UNDERFLOW.
   * @return      The width of the corresponding bin.
   *
   */
  double binWidth(int) const {
    return (upper - lower)/double(nbins);
  }

  /**
   * Convert a coordinate on the axis to a bin number.  If the
   * coordinate is less than the lowerEdge UNDERFLOW is returned; if
   * the coordinate is greater or equal to the upperEdge OVERFLOW is
   * returned.
   * @param coord The coordinate to be converted.
   * @return      The corresponding bin number.
   *
   */
  int coordToIndex(double coord) const {
    if ( coord >= upper ) return OVERFLOW_BIN;
    else if ( coord < lower ) return UNDERFLOW_BIN;
    else return int((coord - lower)/binWidth(0));
  }

  /**
   * Return the midpoint of the specified bin. No checking is
   * performed to ensure the argument is a valid bin.
   */
  double binMidPoint(int index) const {
    return lower + (double(index) + 0.5)*binWidth(0);
  }

private:

  /** The lower edge. */
  double lower;

  /** The upper edge. */
  double upper;

  /** The number of bins. */
  int nbins;

};

}

#endif /* LWH_Axis_H */
