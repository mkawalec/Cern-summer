// -*- C++ -*-
#ifndef LWH_Measurement_H
#define LWH_Measurement_H
//
// This is the declaration of the Measurement class representing
//


#include <limits>
#include <cmath>
#include <algorithm>
#include "AIMeasurement.h"

namespace LWH {

using namespace AIDA;

/**
 * Basic user-level interface class for holding a single "measurement"
 * with positive and negative errors (to allow for asymmetric errors).
 * "IMeasurement" = "value" + "errorPlus" - "errorMinus"
 */
class Measurement: public IMeasurement {

public:

  /**
   * Standard constructor.
   */
  Measurement(double v = 0.0, double ep = 0.0, double em = 0.0)
    : val(v), errp(ep), errm(em) {}

  /**
   * Copy constructor.
   */
  Measurement(const Measurement & m)
    :IMeasurement(m), val(m.val), errp(m.errp), errm(m.errm) {}

  /**
   * Destructor.
   */
  virtual ~Measurement() { /* nop */; }

  /**
   * Get the value of the Measurement.
   * @return The value of the Measurement.
   */
  double value() const {
    return val;
  }

  /**
   * Get the plus error of the IMeasurement.
   * @return The plus error.
   */
  double errorPlus() const {
    return errp;
  }

  /**
   * Get the minus error of the IMeasurement.
   * @return The minus error.
   */
  double errorMinus() const {
    return errm;
  }

  /**
   * Set the value of the IMeasurement.
   * @param v The new value of the IMeasurement.
   * @return false If the value cannot be set.
   */
  bool setValue(double v) {
    val = v;
    return true;
  }

  /**
   * Set the plus error of the IMeasurement.
   * @param ep The new plus error of the IMeasurement.
   * @return false If the error cannot be set or it is negative.
   */
  bool setErrorPlus(double ep) {
    errp = ep;
    return ep < 0.0;
  }

  /**
   * Set the minus error of the IMeasurement.
   * @param em The new minus error of the IMeasurement.
   * @return false If the error cannot be set or it is negative.
   */
  bool setErrorMinus(double em) {
    errm = em;
    return em < 0.0;
  }

private:

  /**
   * The value.
   */
  double val;

  /**
   * The plus error.
   */
  double errp;

  /**
   * The minus error.
   */
  double errm;

};

}

#endif /* LWH_Measurement_H */
