// -*- C++ -*-
#ifndef RIVET_IsolationEstimators_HH
#define RIVET_IsolationEstimators_HH

#include "Rivet/Math/MathUtils.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Jet.hh"

#include <vector>
#include <typeinfo>

namespace Rivet {

  /// @cond ISOLATION_DETAILS

  template < typename T, typename C >
  class IsolationEstimator {

    public:

    virtual ~IsolationEstimator(){};

      virtual double estimate(const T & t, const C & c) const = 0;

      virtual int compare(const IsolationEstimator < T, C > *other) const = 0;

      virtual bool before(const IsolationEstimator * other) const {
        const std::type_info & thisid = typeid(*this);
        const std::type_info & otherid = typeid(*other);
        if (thisid == otherid) {
          return compare(other) < 0;
        } else {
          return thisid.before(otherid);
        }
      }

      bool operator < (const IsolationEstimator& other) const{
        return this->before(&other);
      }
  };


  // An estimator for the sum of the pt of the particles in collection C
  // being within radius from t
  template < class T, class C >
  class PtInConeEstimator : public IsolationEstimator < T, C > {
  public:
    PtInConeEstimator(double radius, double ptmin = 0.0)
      : _radius(radius), _ptmin(ptmin) { }

    virtual double estimate(const T & t, const C & c) const {
      double ptsum = 0;
      for (typename C::const_iterator ic = c.begin(); ic != c.end(); ++ic) {
        if (ic->momentum().pT() < _ptmin)
          continue;
        if (deltaR(t.momentum(), ic->momentum()) < _radius) {
          ptsum += ic->momentum().pT();
        }
      }
      return ptsum / t.momentum().pT();
    }

    virtual int compare(const IsolationEstimator < T, C > *other) const {
      const PtInConeEstimator *concreteother = dynamic_cast<const PtInConeEstimator*>(other);
      int ptmincmp = cmp(_ptmin, concreteother->getPtMin());
      if (ptmincmp != 0)
         return ptmincmp;
      int radcmp = cmp(_radius, concreteother->getRadius());
      if (radcmp != 0)
         return radcmp;
       return 0;
    }

    double radius() const {
      return _radius;
    }

    double ptMin() const {
      return _ptmin;
    }
  private:
    double _radius;
    double _ptmin;
  };


  // An estimator for the number of particles in collection C
  // being within radius from t
  template < class T, class C >
  class MultiplicityInConeEstimator : public IsolationEstimator < T, C > {
  public:
    MultiplicityInConeEstimator(double radius, double ptmin = 0.0)
      : _radius(radius), _ptmin(ptmin) {  }

    virtual double estimate(const T & t, const C & c) const {
      double npart = 0;
      for (typename C::const_iterator ic = c.begin(); ic != c.end(); ++ic) {
        if (ic->momentum().pT() < _ptmin)
          continue;
        if (deltaR(t.momentum(), ic->momentum()) < _radius) {
          npart++;
        }
      }
      return npart;
    }

    virtual int compare(const IsolationEstimator < T, C > *other) const {
      const MultiplicityInConeEstimator *concreteother = dynamic_cast < const MultiplicityInConeEstimator * >(other);
      int ptmincmp = cmp(_ptmin, concreteother->getPtMin());
      if (ptmincmp != 0)
         return ptmincmp;
      int radcmp = cmp(_radius, concreteother->getRadius());
      if (radcmp != 0)
         return radcmp;
       return 0;
    }

    double radius() const {
      return _radius;
    }

    double ptMin() const {
      return _ptmin;
    }

  private:
    double _radius;
    double _ptmin;
  };


  /// Typedefs
  typedef MultiplicityInConeEstimator < Jet, std::vector < Jet > >JetIsoEstimatorByMultiplicity;
  typedef MultiplicityInConeEstimator < Particle, std::vector < Jet > >ParticleFromJetIsoEstimatorByMultiplicity;
  typedef MultiplicityInConeEstimator < Particle, std::vector < Particle > >ParticleIsoEstimatorByMultiplicity;

  typedef PtInConeEstimator < Jet, std::vector < Jet > >JetIsoEstimatorByPt;
  typedef PtInConeEstimator < Particle, std::vector < Jet > >ParticleFromJetIsoEstimatorByPt;
  typedef PtInConeEstimator < Particle, std::vector < Particle > >ParticleIsoEstimatorByPt;
  template <typename TYPE1, typename TYPE2> struct isohelper {
            typedef IsolationEstimator<TYPE1, TYPE2> estimatorhelper;
  };


  /// @endcond

}

#endif
