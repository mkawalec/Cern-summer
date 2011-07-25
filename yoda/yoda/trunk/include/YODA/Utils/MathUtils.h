// -*- C++ -*-
#ifndef YODA_MathUtils_H
#define YODA_MathUtils_H

#include <YODA/Config/BuildConfig.h>

#include <stdexcept>
#include <string>
#include <ostream>
#include <sstream>
#include <iostream>
#include <cmath>
#include <map>
#include <vector>
#include <utility>
#include <algorithm>
#include <numeric>
#include <cassert>
#include <limits>

namespace YODA {


  const double MAXDOUBLE = std::numeric_limits<double>::max();
  const double MAXINT = std::numeric_limits<int>::max();

  /// A pre-defined value of \f$ \pi \f$.
  const double PI = M_PI;

  /// A pre-defined value of \f$ 2\pi \f$.
  const double TWOPI = 2*M_PI;

  /// A pre-defined value of \f$ \pi/2 \f$.
  const double HALFPI = M_PI_2;

  /// Enum for signs of numbers.
  enum Sign { MINUS = -1, ZERO = 0, PLUS = 1 };


  /// @name Comparison functions for safe floating point equality tests
  //@{

  /// Compare a floating point number to zero with a degree
  /// of fuzziness expressed by the absolute @a tolerance parameter.
  inline bool isZero(double val, double tolerance=1E-8) {
    return (fabs(val) < tolerance);
  }

  /// Compare an integral-type number to zero. Since there is no
  /// risk of floating point error, this function just exists in
  /// case @c isZero is accidentally used on an integer type, to avoid
  /// implicit type conversion. The @a tolerance parameter is ignored.
  inline bool isZero(long val, double UNUSED(tolerance)=1E-8) {
    return val == 0;
  }


  /// @brief Compare two floating point numbers for equality with a degree of fuzziness
  /// The @a tolerance parameter is fractional.
  inline bool fuzzyEquals(double a, double b, double tolerance=1E-5) {
    const double absavg = fabs(a + b)/2.0;
    const double absdiff = fabs(a - b);
    const bool rtn = (absavg == 0.0 && absdiff == 0.0) || absdiff < tolerance*absavg;
    return rtn;
  }

  /// @brief Compare two integral-type numbers for equality with a degree of fuzziness.
  /// Since there is no risk of floating point error with integral types,
  /// this function just exists in case @c fuzzyEquals is accidentally
  /// used on an integer type, to avoid implicit type conversion. The @a
  /// tolerance parameter is ignored, even if it would have an
  /// absolute magnitude greater than 1.
  inline bool fuzzyEquals(long a, long b, double UNUSED(tolerance)=1E-5) {
    return a == b;
  }


  /// @brief Compare two floating point numbers for >= with a degree of fuzziness
  /// The @a tolerance parameter on the equality test is as for @c fuzzyEquals.
  inline bool fuzzyGtrEquals(double a, double b, double tolerance=1E-5) {
    return a > b || fuzzyEquals(a, b, tolerance);
  }

  /// @brief Compare two integral-type numbers for >= with a degree of fuzziness.
  /// Since there is no risk of floating point error with integral types,
  /// this function just exists in case @c fuzzyGtrEquals is accidentally
  /// used on an integer type, to avoid implicit type conversion. The @a
  /// tolerance parameter is ignored, even if it would have an
  /// absolute magnitude greater than 1.
  inline bool fuzzyGtrEquals(long a, long b, double UNUSED(tolerance)=1E-5) {
    return a >= b;
  }


  /// @brief Compare two floating point numbers for <= with a degree of fuzziness
  /// The @a tolerance parameter on the equality test is as for @c fuzzyEquals.
  inline bool fuzzyLessEquals(double a, double b, double tolerance=1E-5) {
    return a < b || fuzzyEquals(a, b, tolerance);
  }

  /// @brief Compare two integral-type numbers for <= with a degree of fuzziness.
  /// Since there is no risk of floating point error with integral types,
  /// this function just exists in case @c fuzzyLessEquals is accidentally
  /// used on an integer type, to avoid implicit type conversion. The @a
  /// tolerance parameter is ignored, even if it would have an
  /// absolute magnitude greater than 1.
  inline bool fuzzyLessEquals(long a, long b, double UNUSED(tolerance)=1E-5) {
    return a <= b;
  }

  /// @brief Returns a number floored at the nth decimal place.
  inline double approx(double a, int n = 5) {
    int roundTo = pow(10,n);
    a *= roundTo;
    a = floor(a);
    return a/roundTo;
  }
  //@}


  /// @name Ranges and intervals
  //@{

  /// Represents whether an interval is open (non-inclusive) or closed
  /// (inclusive). For example, the interval \f$ [0, \pi) \f$ is closed (an inclusive
  /// boundary) at 0, and open (a non-inclusive boundary) at \f$ \pi \f$.
  enum RangeBoundary { OPEN=0, SOFT=0, CLOSED=1, HARD=1 };


  /// @brief Determine if @a value is in the range @a low to @a high, for floating point numbers
  /// Interval boundary types are defined by @a lowbound and @a highbound.
  /// @todo Optimise to one-line at compile time?
  template<typename NUM>
  inline bool inRange(NUM value, NUM low, NUM high,
                      RangeBoundary lowbound=CLOSED, RangeBoundary highbound=OPEN) {
    if (lowbound == OPEN && highbound == OPEN) {
      return (value > low && value < high);
    } else if (lowbound == OPEN && highbound == CLOSED) {
      return (value > low && (value < high || fuzzyEquals(value, high)));
    } else if (lowbound == CLOSED && highbound == OPEN) {
      return ((value > low || fuzzyEquals(value, low)) && value < high);
    } else { // if (lowbound == CLOSED && highbound == CLOSED) {
      return ((value > low || fuzzyEquals(value, low)) && (value < high || fuzzyEquals(value, high)));
    }
  }

  /// Alternative version of inRange for doubles, which accepts a pair for the range arguments.
  template<typename NUM>
  inline bool inRange(NUM value, std::pair<NUM, NUM> lowhigh,
                      RangeBoundary lowbound=CLOSED, RangeBoundary highbound=OPEN) {
    return inRange(value, lowhigh.first, lowhigh.second, lowbound, highbound);
  }


  /// @brief Determine if @a value is in the range @a low to @a high, for integer types
  /// Interval boundary types are defined by @a lowbound and @a highbound.
  /// @todo Optimise to one-line at compile time?
  inline bool inRange(int value, int low, int high,
                      RangeBoundary lowbound=CLOSED, RangeBoundary highbound=CLOSED) {
    if (lowbound == OPEN && highbound == OPEN) {
      return (value > low && value < high);
    } else if (lowbound == OPEN && highbound == CLOSED) {
      return (value > low && value <= high);
    } else if (lowbound == CLOSED && highbound == OPEN) {
      return (value >= low && value < high);
    } else { // if (lowbound == CLOSED && highbound == CLOSED) {
      return (value >= low && value <= high);
    }
  }

  /// Alternative version of @c inRange for ints, which accepts a pair for the range arguments.
  inline bool inRange(int value, std::pair<int, int> lowhigh,
                      RangeBoundary lowbound=CLOSED, RangeBoundary highbound=OPEN) {
    return inRange(value, lowhigh.first, lowhigh.second, lowbound, highbound);
  }

  //@}


  /// @name Miscellaneous numerical helpers
  //@{

  /// Named number-type squaring operation.
  template <typename NUM>
  inline NUM sqr(NUM a) {
    return a*a;
  }

  /// Named number-type addition in quadrature operation.
  template <typename Num>
  inline Num add_quad(Num a, Num b) {
    return sqrt(a*a + b*b);
  }

  /// Named number-type addition in quadrature operation.
  template <typename Num>
  inline Num add_quad(Num a, Num b, Num c) {
    return sqrt(a*a + b*b + c*c);
  }

  /// Find the sign of a number
  inline int sign(double val) {
    if (isZero(val)) return ZERO;
    const int valsign = (val > 0) ? PLUS : MINUS;
    return valsign;
  }

  /// Find the sign of a number
  inline int sign(int val) {
    if (val == 0) return ZERO;
    return (val > 0) ? PLUS : MINUS;
  }

  /// Find the sign of a number
  inline int sign(long val) {
    if (val == 0) return ZERO;
    return (val > 0) ? PLUS : MINUS;
  }

  //@}


  /// @name Binning helper functions
  //@{

  /// Make a list of @a nbins + 1 values equally spaced between @a start and @a end inclusive.
  inline std::vector<double> linspace(double start, double end, size_t nbins) {
    assert(end >= start);
    assert(nbins > 0);
    std::vector<double> rtn;
    const double interval = (end-start)/static_cast<double>(nbins);
    double edge = start;
    while (inRange(edge, start, end, CLOSED, CLOSED)) {
      rtn.push_back(edge);
      edge += interval;
    }
    assert(rtn.size() == nbins+1);
    return rtn;
  }


  /// Make a list of @a nbins + 1 values exponentially spaced between @a start and @a end inclusive.
  inline std::vector<double> logspace(double start, double end, size_t nbins) {
    assert(end >= start);
    assert(start > 0);
    assert(nbins > 0);
    const double logstart = std::log(start);
    const double logend = std::log(end);
    const std::vector<double> logvals = linspace(logstart, logend, nbins);
    std::vector<double> rtn;
    for (size_t i = 1; i < logvals.size(); ++i) {
      rtn.push_back(std::exp(logvals[i]));
    }
    assert(rtn.size() == nbins+1);
    return rtn;
  }


  /// @brief Return the bin index of the given value, @a val, given a vector of bin edges
  /// NB. The @a binedges vector must be sorted
  template <typename NUM>
  inline int index_between(const NUM& val, const std::vector<NUM>& binedges) {
    if (!inRange(val, binedges.front(), binedges.back())) return -1; //< Out of histo range
    int index = -1;
    for (size_t i = 1; i < binedges.size(); ++i) {
      if (val < binedges[i]) {
        index = i-1;
        break;
      }
    }
    assert(inRange(index, -1, binedges.size()-1));
    return index;
  }

  //@}


  /// @name Statistics functions
  //@{

  /// Calculate the mean of a sample
  inline double mean(const std::vector<int>& sample) {
    double mean = 0.0;
    for (size_t i=0; i<sample.size(); ++i) {
      mean += sample[i];
    }
    return mean/sample.size();
  }


  /// Calculate the covariance (variance) between two samples
  inline double covariance(const std::vector<int>& sample1, const std::vector<int>& sample2) {
    const double mean1 = mean(sample1);
    const double mean2 = mean(sample2);
    const int N = sample1.size();
    double cov = 0.0;
    for (int i = 0; i < N; i++) {
      const double cov_i = (sample1[i] - mean1)*(sample2[i] - mean2);
      cov += cov_i;
    }
    if (N > 1) return cov/(N-1);
    else return 0.0;
  }


  /// Calculate the correlation strength between two samples
  inline double correlation(const std::vector<int>& sample1, const std::vector<int>& sample2) {
    const double cov = covariance(sample1, sample2);
    const double var1 = covariance(sample1, sample1);
    const double var2 = covariance(sample2, sample2);
    const double correlation = cov/sqrt(var1*var2);
    const double corr_strength = correlation*sqrt(var2/var1);
    return corr_strength;
  }

  //@}


}

#endif
