// -*- C++ -*-
#ifndef LWH_DataPoint_H
#define LWH_DataPoint_H
//
// This is the declaration of the DataPoint class representing
//


#include <limits>
#include <cmath>
#include <algorithm>
#include "AIDataPoint.h"
#include "Measurement.h"

namespace LWH {

using namespace AIDA;

/**
 * An DataPoint represents a binned histogram axis. A 1D Histogram would have
 * one DataPoint representing the X axis, while a 2D Histogram would have two
 * axes representing the X and Y DataPoint.
 */
class DataPoint: public IDataPoint {

public:

  /**
   * Construct a data point with a given number of dimensions.
   */
  DataPoint(int dim = 2)
    : m(dim) {}

  /**
   * Constructor taking a vector of measurements as argument.
   */
  DataPoint(const std::vector<Measurement> & vm)
    : m(vm) {}

  /**
   * Copy constructor.
   */
  DataPoint(const DataPoint & d)
    : IDataPoint(d), m(d.m) {}

  /**
   * Copy from any IDataPoint.
   */
  DataPoint(const IDataPoint & id)
    : m(id.dimension()) {
    for ( int i = 0, N = m.size(); i < N; ++i )
      m[i] = Measurement(id.coordinate(i)->value(),
			 id.coordinate(i)->errorPlus(),
			 id.coordinate(i)->errorMinus());
  }

  /**
   * Destructor.
   */
  virtual ~DataPoint() {}

  /**
   * Get the dimension of the IDataPoint, i.e. the number
   * of coordinates the point has.
   * @return The dimension.
   */
  int dimension() const {
    return m.size();
  }

  /**
   * Get the IMeasurement for a given coordinate.
   * @param coord The coordinate.
   * @return      The corresponding IMeasurement.
   */
  IMeasurement * coordinate(int coord) {
    return &(m[coord]);
  }

  /**
   * Get the IMeasurement for a given coordinate.
   * @param coord The coordinate.
   * @return      The corresponding IMeasurement.
   */
  const IMeasurement * coordinate(int coord) const {
    return &(m[coord]);
  }

  private:

  /**
   * The included measurements.
   */
  std::vector<Measurement> m;

};

}

#endif /* LWH_DataPoint_H */
