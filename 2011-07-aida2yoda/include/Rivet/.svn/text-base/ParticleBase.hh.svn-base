#ifndef RIVET_ParticleBase_HH
#define RIVET_ParticleBase_HH

#include "Rivet/Rivet.hh"
#include "Rivet/Math/Vectors.hh"

namespace Rivet {


  /// @brief Base class for particle-like things like Particle and Jet
  class ParticleBase {
  public:

    ParticleBase() { }

    virtual ~ParticleBase() { }

    // virtual FourMomentum& momentum() = 0;

    virtual const FourMomentum& momentum() const = 0;


    /// Struct for sorting by increasing transverse momentum in STL set, sort, etc.
    struct byPTAscending {
      bool operator()(const ParticleBase& left, const ParticleBase& right) const {
        double pt2left = left.momentum().pT2();
        double pt2right = right.momentum().pT2();
        return pt2left < pt2right;
      }

      bool operator()(const ParticleBase* left, const ParticleBase* right) const {
        return (*this)(*left, *right);
      }
    };


    /// Struct for sorting by decreasing transverse momentum in STL set, sort etc.
    struct byPTDescending {
      bool operator()(const ParticleBase& left, const ParticleBase& right) const {
        return byPTAscending()(right, left);
      }

      bool operator()(const ParticleBase* left, const ParticleBase* right) const {
        return (*this)(*left, *right);
      }
    };


    /// Struct for sorting by increasing transverse energy
    struct byETAscending {
      bool operator()(const ParticleBase& left, const ParticleBase& right) const {
        double pt2left = left.momentum().Et2();
        double pt2right = right.momentum().Et2();
        return pt2left < pt2right;
      }

      bool operator()(const ParticleBase* left, const ParticleBase* right) const {
        return (*this)(*left, *right);
      }
    };


    /// Struct for sorting by decreasing transverse energy
    struct byETDescending {
      bool operator()(const ParticleBase& left, const ParticleBase& right) const {
        return byETAscending()(right, left);
      }

      bool operator()(const ParticleBase* left, const ParticleBase* right) const {
        return (*this)(*left, *right);
      }
    };


    /// Struct for sorting by increasing energy
    struct byEAscending {
      bool operator()(const ParticleBase& left, const ParticleBase& right) const {
        double pt2left = left.momentum().E();
        double pt2right = right.momentum().E();
        return pt2left < pt2right;
      }

      bool operator()(const ParticleBase* left, const ParticleBase* right) const {
        return (*this)(*left, *right);
      }
    };


    /// Struct for sorting by decreasing energy
    struct byEDescending {
      bool operator()(const ParticleBase& left, const ParticleBase& right) const {
        return byEAscending()(right, left);
      }

      bool operator()(const ParticleBase* left, const ParticleBase* right) const {
        return (*this)(*left, *right);
      }
    };


  };


}

#endif
