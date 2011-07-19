// -*- C++ -*-
#ifndef RIVET_MathUtils_HH
#define RIVET_MathUtils_HH

#include "Rivet/Math/MathHeader.hh"
#include "Rivet/RivetBoost.hh"
#include <cassert>

namespace Rivet {


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
  inline bool inRange(NUM value, pair<NUM, NUM> lowhigh,
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
  inline bool inRange(int value, pair<int, int> lowhigh,
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

  /// A more efficient version of pow for raising numbers to integer powers.
  template <typename Num>
  inline Num intpow(Num val, unsigned int exp) {
    assert(exp >= 0);
    if (exp == 0) return (Num) 1;
    else if (exp == 1) return val;
    else return val * intpow(val, exp-1);
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
  inline vector<double> linspace(double start, double end, size_t nbins) {
    assert(end >= start);
    assert(nbins > 0);
    vector<double> rtn;
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
  inline vector<double> logspace(double start, double end, size_t nbins) {
    assert(end >= start);
    assert(start > 0);
    assert(nbins > 0);
    const double logstart = std::log(start);
    const double logend = std::log(end);
    const vector<double> logvals = linspace(logstart, logend, nbins);
    vector<double> rtn;
    foreach (double logval, logvals) {
      rtn.push_back(std::exp(logval));
    }
    assert(rtn.size() == nbins+1);
    return rtn;
  }


  /// @brief Return the bin index of the given value, @a val, given a vector of bin edges
  /// NB. The @a binedges vector must be sorted
  template <typename NUM>
  inline int index_between(const NUM& val, const vector<NUM>& binedges) {
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
  inline double mean(const vector<int>& sample) {
    double mean = 0.0;
    for (size_t i=0; i<sample.size(); ++i) {
      mean += sample[i];
    }
    return mean/sample.size();
  }

  // Calculate the error on the mean, assuming poissonian errors
  inline double mean_err(const vector<int>& sample) {
    double mean_e = 0.0;
    for (size_t i=0; i<sample.size(); ++i) {
      mean_e += sqrt(sample[i]);
    }
    return mean_e/sample.size();
  }

  /// Calculate the covariance (variance) between two samples
  inline double covariance(const vector<int>& sample1, const vector<int>& sample2) {
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

  /// Calculate the error on the covariance (variance) of two samples, assuming poissonian errors
  inline double covariance_err(const vector<int>& sample1, const vector<int>& sample2) {
    const double mean1 = mean(sample1);
    const double mean2 = mean(sample2);
    const double mean1_e = mean_err(sample1);
    const double mean2_e = mean_err(sample2);
    const int N = sample1.size();
    double cov_e = 0.0;
    for (int i = 0; i < N; i++) {
      const double cov_i = (sqrt(sample1[i]) - mean1_e)*(sample2[i] - mean2) +
        (sample1[i] - mean1)*(sqrt(sample2[i]) - mean2_e);
      cov_e += cov_i;
    }
    if (N > 1) return cov_e/(N-1);
    else return 0.0;
  }


  /// Calculate the correlation strength between two samples
  inline double correlation(const vector<int>& sample1, const vector<int>& sample2) {
    const double cov = covariance(sample1, sample2);
    const double var1 = covariance(sample1, sample1);
    const double var2 = covariance(sample2, sample2);
    const double correlation = cov/sqrt(var1*var2);
    const double corr_strength = correlation*sqrt(var2/var1);
    return corr_strength;
  }

  /// Calculate the error of the correlation strength between two samples assuming Poissonian errors
  inline double correlation_err(const vector<int>& sample1, const vector<int>& sample2) {
    const double cov = covariance(sample1, sample2);
    const double var1 = covariance(sample1, sample1);
    const double var2 = covariance(sample2, sample2);
    const double cov_e = covariance_err(sample1, sample2);
    const double var1_e = covariance_err(sample1, sample1);
    const double var2_e = covariance_err(sample2, sample2);

    // Calculate the correlation
    const double correlation = cov/sqrt(var1*var2);
    // Calculate the error on the correlation
    const double correlation_err = cov_e/sqrt(var1*var2) -
      cov/(2*pow(3./2., var1*var2)) * (var1_e * var2 + var1 * var2_e);


    // Calculate the error on the correlation strength
    const double corr_strength_err = correlation_err*sqrt(var2/var1) + 
      correlation/(2*sqrt(var2/var1)) * (var2_e/var1 - var2*var1_e/pow(2, var2));

    return corr_strength_err;
  }
  //@}


  /// @name Angle range mappings
  //@{

  /// Reduce any number to the range [-2PI, 2PI] by repeated addition or
  /// subtraction of 2PI as required. Used to normalise angular measures.
  inline double _mapAngleM2PITo2Pi(double angle) {
    double rtn = fmod(angle, TWOPI);
    if (isZero(rtn)) return 0;
    assert(rtn >= -TWOPI && rtn <= TWOPI);
    return rtn;
  }

  /// Map an angle into the range (-PI, PI].
  inline double mapAngleMPiToPi(double angle) {
    double rtn = _mapAngleM2PITo2Pi(angle);
    if (isZero(rtn)) return 0;
    rtn = (rtn >   PI ? rtn-TWOPI :
           rtn <= -PI ? rtn+TWOPI : rtn);
    assert(rtn > -PI && rtn <= PI);
    return rtn;
  }

  /// Map an angle into the range [0, 2PI).
  inline double mapAngle0To2Pi(double angle) {
    double rtn = _mapAngleM2PITo2Pi(angle);
    if (isZero(rtn)) return 0;
    if (rtn < 0) rtn += TWOPI;
    if (rtn == TWOPI) rtn = 0;
    assert(rtn >= 0 && rtn < TWOPI);
    return rtn;
  }

  /// Map an angle into the range [0, PI].
  inline double mapAngle0ToPi(double angle) {
    double rtn = fabs(mapAngleMPiToPi(angle));
    if (isZero(rtn)) return 0;
    assert(rtn > 0 && rtn <= PI);
    return rtn;
  }

  //@}


  /// @name Phase space measure helpers
  //@{

  /// Calculate the difference between two angles in radians,
  /// returning in the range [0, PI].
  inline double deltaPhi(double phi1, double phi2) {
    return mapAngle0ToPi(phi1 - phi2);
  }

  /// Calculate the difference between two pseudorapidities,
  /// returning the unsigned value.
  inline double deltaEta(double eta1, double eta2) {
    return fabs(eta1 - eta2);
  }

  /// Calculate the distance between two points in 2D rapidity-azimuthal
  /// ("\f$ \eta-\phi \f$") space. The phi values are given in radians.
  inline double deltaR(double rap1, double phi1, double rap2, double phi2) {
    const double dphi = deltaPhi(phi1, phi2);
    return sqrt( sqr(rap1-rap2) + sqr(dphi) );
  }

  /// Calculate a rapidity value from the supplied energy @a E and longitudinal momentum @a pz.
  inline double rapidity(double E, double pz) {
    if (isZero(E - pz)) {
      throw std::runtime_error("Divergent positive rapidity");
      return MAXDOUBLE;
    }
    if (isZero(E + pz)) {
      throw std::runtime_error("Divergent negative rapidity");
      return -MAXDOUBLE;
    }
    return 0.5*log((E+pz)/(E-pz));
  }

  //@}


}


#endif
