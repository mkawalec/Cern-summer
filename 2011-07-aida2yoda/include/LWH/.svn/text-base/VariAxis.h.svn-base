// -*- C++ -*-
#ifndef LWH_VariAxis_H
#define LWH_VariAxis_H
//
// This is the declaration of the VariAxis class representing
//


#include <limits>
#include <cmath>
#include <algorithm>
#include <map>
#include "AIAxis.h"

namespace LWH {

using namespace AIDA;

/**
 * An VariAxis represents a binned histogram axis. A 1D Histogram would have
 * one VariAxis representing the X axis, while a 2D Histogram would have two
 * axes representing the X and Y VariAxis.
 */
class VariAxis: public IAxis {

public:

  /**
   * Standard constructor.
   */
  VariAxis(const std::vector<double> & edges) {
    for ( int i = 0, N = edges.size(); i < N; ++i ) binco[edges[i]] = 0;
    std::map<double,int>::iterator it = binco.begin();
    for ( int i = 0, N = edges.size(); i < N; ++i ) (it++)->second = i;
  }

  /**
   * Copy constructor.
   */
  VariAxis(const VariAxis & a)
    : IAxis(a), binco(a.binco) {}

  /// Destructor.
  virtual ~VariAxis() { }

  /**
   * Check if the IAxis has fixed binning, i.e. if all the bins have
   * the same width.  @return <code>true</code> if the binning is
   * fixed, <code>false</code> otherwise.
   *
   */
  bool isFixedBinning() const {return false; }

  /**
   * Get the lower edge of the IAxis.
   * @return The IAxis's lower edge.
   *
   */
  double lowerEdge() const {
    if ( binco.size() ) return binco.begin()->first;
    return 0;
  }

  /**
   * Get the upper edge of the IAxis.
   * @return The IAxis's upper edge.
   *
   */
  double upperEdge() const {
    if ( !binco.size() ) return 0;
    std::map<double,int>::const_iterator last = binco.end();
    return (--last)->first;
  }

  /**
   * The number of bins (excluding underflow and overflow) on the IAxis.
   * @return The IAxis's number of bins.
   *
   */
  int bins() const { return binco.size() - 1; }

  /**
   * Get the lower edge of the specified bin.
   * @param index The bin number: 0 to bins()-1 for the in-range bins
   * or OVERFLOW or UNDERFLOW.
   * @return The lower edge of the corresponding bin; for the
   * underflow bin this is <tt>Double.NEGATIVE_INFINITY</tt>.
   *
   */
  std::pair<double,double> binEdges(int index) const {
    std::pair<double,double> edges(0.0, 0.0);
    if ( !binco.size() ) return edges;
    std::map<double,int>::const_iterator lo = binco.end();
    std::map<double,int>::const_iterator up = binco.begin();
    if ( index >= 0 ) while ( index-- >= 0 && up != binco.end() ) lo = up++;
    edges.first = ( lo == binco.end() )? -std::numeric_limits<double>::max():
                                         lo->first;
    edges.second = ( up == binco.end() )? std::numeric_limits<double>::max():
                                         up->first;
    return edges;
  }

  /**
   * Get the lower edge of the specified bin.
   * @param index The bin number: 0 to bins()-1 for the in-range bins
   * or OVERFLOW or UNDERFLOW.
   * @return The lower edge of the corresponding bin; for the
   * underflow bin this is <tt>Double.NEGATIVE_INFINITY</tt>.
   *
   */
  double binLowerEdge(int index) const {
    return binEdges(index).first;
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
    return binEdges(index).second;
  }

  /**
   * Get the width of the specified bin.
   * @param index The bin number: 0 to bins()-1) for the in-range bins
   * or OVERFLOW or UNDERFLOW.
   * @return      The width of the corresponding bin.
   *
   */
  double binWidth(int index) const {
    std::pair<double,double> edges = binEdges(index);
    return edges.second - edges.first;
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
    std::map<double,int>::const_iterator up = binco.upper_bound(coord);
    if ( up == binco.begin() ) return UNDERFLOW_BIN;
    else if ( up == binco.end() ) return OVERFLOW_BIN;
    else return up->second - 1;
  }

  /**
   * Return the midpoint of the specified bin. No checking is
   * performed to ensure the argument is a valid bin.
   */
  double binMidPoint(int index) const {
    std::pair<double,double> edges = binEdges(index);
    return (edges.second + edges.first)/2.0;
  }

private:

  /**
   * A map relating the lower edge of a bin to the corresponding bin
   * number.
   */
  std::map<double,int> binco;

};

}

#endif /* LWH_VariAxis_H */
