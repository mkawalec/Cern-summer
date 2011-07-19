// -*- C++ -*-
#ifndef RIVET_Jet_HH
#define RIVET_Jet_HH

#include "Rivet/Rivet.hh"
#include <numeric>

namespace Rivet {


  /// @brief A minimal class representing a jet of particles.
  class Jet : public ParticleBase {
  public:

    /// Constructor.
    Jet();

    /// Define a Jet::iterator via a typedef.
    typedef vector<FourMomentum>::iterator iterator;

    /// Define a Jet::const_iterator via a typedef.
    typedef vector<FourMomentum>::const_iterator const_iterator;

    /// Get a begin iterator over the particle/track four-momenta in this jet.
    iterator begin() {
      return _particles.begin();
    }

    /// Get an end iterator over the particle/track four-momenta in this jet.
    iterator end() {
      return _particles.end();
    }

    /// Get a const begin iterator over the particle/track four-momenta in this jet.
    const_iterator begin() const {
      return _particles.begin();
    }

    /// Get a const end iterator over the particle/track four-momenta in this jet.
    const_iterator end() const {
      return _particles.end();
    }

    /// Get the track momenta in this jet.
    vector<FourMomentum>& momenta() {
      return _particles;
    }

    /// Get the track momenta in this jet (const version).
    const vector<FourMomentum>& momenta() const {
      return _particles;
    }

    /// Get the Rivet::Particles (full information) in this jet
    vector<Particle>& particles() {
      return _fullParticles;
    }

    /// Get the Rivet::Particles (full information) in this jet (const version)
    const vector<Particle>& particles() const {
      return _fullParticles;
    }

    /// Number of particles (tracks) in this jet.
    size_t size() const {
      return _particles.size();
    }

    /// Set the particles/tracks collection.
    Jet& setParticles(const vector<FourMomentum>& particles);

    /// Add a particle/track to this jet.
    Jet& addParticle(const FourMomentum& particle);

    /// Add a particle/track to this jet.
    Jet& addParticle(const Particle& particle);

    /// Check whether this jet contains a particular particle.
    bool containsParticle(const Particle& particle) const;

    /// Check whether this jet contains a certain particle type.
    bool containsParticleId(PdgId pid) const;

    /// Check whether this jet contains at least one of certain particle types.
    bool containsParticleId(const vector<PdgId>& pids) const;

    /// Check whether this jet contains a charm-flavoured hadron (or decay products from one).
    bool containsCharm() const;

    /// Check whether this jet contains a bottom-flavoured hadron (or decay products from one).
    bool containsBottom() const;

    /// Reset this jet as empty.
    Jet& clear();

    /// Get the average \f$ \eta \f$ for this jet, with the average weighted
    /// by the \f$ p_T \f$ values of the constituent tracks. (caches)
    double ptWeightedEta() const;

    /// Get the average \f$ \phi \f$ for this jet, with the average weighted
    /// by the \f$ p_T \f$ values of the constituent tracks. (caches)
    double ptWeightedPhi() const;

    /// Get the unweighted average \f$ \eta \f$ for this jet. (caches)
    double eta() const;

    /// Get the unweighted average \f$ \phi \f$ for this jet. (caches)
    double phi() const;

    /// Get equivalent single momentum four-vector. (caches)
    const FourMomentum& momentum() const;

    // /// Get equivalent single momentum four-vector. (caches)
    // FourMomentum& momentum();



  public:

    /// Get the total energy of this jet.
    double totalEnergy() const;

    /// Get the energy carried in this jet by neutral particles.
    double neutralEnergy() const;

    /// Get the energy carried in this jet by hadrons.
    double hadronicEnergy() const;

    /// Get the sum of the \f$ p_T \f$ values of the constituent tracks. (caches)
    double ptSum() const;

    /// Get the sum of the \f$ E_T \f$ values of the constituent tracks. (caches)
    double EtSum() const;


  private:

    /// @brief Clear the internal cached values.
    /// Const because cache variables are mutable.
    void _resetCaches() const;

    /// @brief Calculate cached equivalent momentum vector.
    /// Const because cache variables are mutable.
    void _calcMomVector() const;

    /// Internal caching method to calculate the average \f$ \eta \f$ and
    /// \f$ \phi \f$ for this jet, weighted by the \f$ p_T \f$ values of the
    /// constituent tracks.
    /// Const because cache variables are mutable.
    void _calcPtAvgs() const;


  private:

    /// The particle tracks.
    std::vector<FourMomentum> _particles;

    /// Full particle information including tracks, ID etc
    ParticleVector _fullParticles;

    /// Cached values of the \f$ p_T \f$-weighted \f$ \bar{\phi} \f$ and \f$ \bar{\eta} \f$.
    mutable double _ptWeightedPhi, _ptWeightedEta;
    mutable bool _okPtWeightedPhi, _okPtWeightedEta;

    /// Cached effective jet 4-vector
    mutable FourMomentum _momentum;
    mutable bool _okMomentum;

  };


  /// Typedef for a collection of Jet objects.
  typedef std::vector<Jet> Jets;


  /// @name Jet comparison functions for STL sorting
  //@{

  /// @brief Compare jets by \f$ p_\perp \f$ (descending - usual sorting for HEP)
  /// Use this so that highest \f$ p_\perp \f$ is at the front of the list
  inline bool cmpJetsByPt(const Jet& a, const Jet& b) {
    return a.ptSum() > b.ptSum();
  }
  /// @brief Compare jets by \f$ p_\perp \f$ (ascending)
  /// Use this so that lowest \f$ p_\perp \f$ is at the front of the list
  inline bool cmpJetsByAscPt(const Jet& a, const Jet& b) {
    return a.ptSum() < b.ptSum();
  }

  /// @brief Compare jets by descending momentum, \f$ p \f$
  inline bool cmpJetsByP(const Jet& a, const Jet& b) {
    return a.momentum().vector3().mod() > b.momentum().vector3().mod();
  }
  /// @brief Compare jets by ascending momentum, \f$ p \f$
  inline bool cmpJetsByAscP(const Jet& a, const Jet& b) {
    return a.momentum().vector3().mod() < b.momentum().vector3().mod();
  }

  // @brief Compare jets by \f$ E_\perp \f$ (descending - usual sorting for HEP)
  /// Use this so that highest \f$ E_\perp \f$ is at the front of the list
  inline bool cmpJetsByEt(const Jet& a, const Jet& b) {
    return a.EtSum() > b.EtSum();
  }
  // @brief Compare jets by \f$ E_\perp \f$ (ascending)
  /// Use this so that lowest \f$ E_\perp \f$ is at the front of the list
  inline bool cmpJetsByEtDesc(const Jet& a, const Jet& b) {
    return a.EtSum() < b.EtSum();
  }

  /// @brief Compare jets by \f$ E \f$ (descending - usual sorting for HEP)
  /// Use this so that highest \f$ E \f$ is at the front of the list
  inline bool cmpJetsByE(const Jet& a, const Jet& b) {
    return a.momentum().E() > b.momentum().E();
  }
  /// @brief Compare jets by \f$ E \f$ (ascending)
  /// Use this so that lowest \f$ E \f$ is at the front of the list
  inline bool cmpJetsByAscE(const Jet& a, const Jet& b) {
    return a.momentum().E() < b.momentum().E();
  }

  /// @brief Compare jets by \f$ \eta \f$ (descending)
  /// Use this so that highest \f$ \eta \f$ is at the front of the list
  inline bool cmpJetsByDescPseudorapidity(const Jet& a, const Jet& b) {
    return a.momentum().pseudorapidity() > b.momentum().pseudorapidity();
  }
  /// @brief Compare jets by \f$ \eta \f$ (ascending)
  /// Use this so that lowest \f$ \eta \f$ is at the front of the list
  inline bool cmpJetsByAscPseudorapidity(const Jet& a, const Jet& b) {
    return a.momentum().pseudorapidity() < b.momentum().pseudorapidity();
  }

  /// @brief Compare jets by \f$ |\eta| \f$ (descending)
  /// Use this so that highest \f$ |\eta| \f$ is at the front of the list
  inline bool cmpJetsByDescAbsPseudorapidity(const Jet& a, const Jet& b) {
    return fabs(a.momentum().pseudorapidity()) > fabs(b.momentum().pseudorapidity());
  }
  /// @brief Compare jets by \f$ |\eta| \f$ (ascending)
  /// Use this so that lowest \f$ |\eta| \f$ is at the front of the list
  inline bool cmpJetsByAscAbsPseudorapidity(const Jet& a, const Jet& b) {
    return fabs(a.momentum().pseudorapidity()) < fabs(b.momentum().pseudorapidity());
  }

  /// @brief Compare jets by \f$ y \f$ (descending)
  /// Use this so that highest \f$ y \f$ is at the front of the list
  inline bool cmpJetsByDescRapidity(const Jet& a, const Jet& b) {
    return a.momentum().rapidity() > b.momentum().rapidity();
  }
  /// @brief Compare jets by \f$ y \f$ (ascending)
  /// Use this so that lowest \f$ y \f$ is at the front of the list
  inline bool cmpJetsByAscRapidity(const Jet& a, const Jet& b) {
    return a.momentum().rapidity() < b.momentum().rapidity();
  }

  /// @brief Compare jets by \f$ |y| \f$ (descending)
  /// Use this so that highest \f$ |y| \f$ is at the front of the list
  inline bool cmpJetsByDescAbsRapidity(const Jet& a, const Jet& b) {
    return fabs(a.momentum().rapidity()) > fabs(b.momentum().rapidity());
  }
  /// @brief Compare jets by \f$ |y| \f$ (ascending)
  /// Use this so that lowest \f$ |y| \f$ is at the front of the list
  inline bool cmpJetsByAscAbsRapidity(const Jet& a, const Jet& b) {
    return fabs(a.momentum().rapidity()) < fabs(b.momentum().rapidity());
  }

  //@}

  inline double deltaR(const Jet& j1, const Jet& j2,
                       RapScheme scheme = PSEUDORAPIDITY) {
    return deltaR(j1.momentum(), j2.momentum(), scheme);
  }

  inline double deltaR(const Jet& j, const Particle& p,
                       RapScheme scheme = PSEUDORAPIDITY) {
    return deltaR(j.momentum(), p.momentum(), scheme);
  }

  inline double deltaR(const Particle& p, const Jet& j,
                       RapScheme scheme = PSEUDORAPIDITY) {
    return deltaR(p.momentum(), j.momentum(), scheme);
  }

  inline double deltaR(const Jet& j, const FourMomentum& v,
                       RapScheme scheme = PSEUDORAPIDITY) {
    return deltaR(j.momentum(), v, scheme);
  }

  inline double deltaR(const Jet& j, const FourVector& v,
                       RapScheme scheme = PSEUDORAPIDITY) {
    return deltaR(j.momentum(), v, scheme);
  }

  inline double deltaR(const Jet& j, const Vector3& v) {
    return deltaR(j.momentum(), v);
  }

  inline double deltaR(const Jet& j, double eta, double phi) {
    return deltaR(j.momentum(), eta, phi);
  }

  inline double deltaR(const FourMomentum& v, const Jet& j,
                       RapScheme scheme = PSEUDORAPIDITY) {
    return deltaR(v, j.momentum(), scheme);
  }

  inline double deltaR(const FourVector& v, const Jet& j,
                       RapScheme scheme = PSEUDORAPIDITY) {
    return deltaR(v, j.momentum(), scheme);
  }

  inline double deltaR(const Vector3& v, const Jet& j) {
    return deltaR(v, j.momentum());
  }

  inline double deltaR(double eta, double phi, const Jet& j) {
    return deltaR(eta, phi, j.momentum());
  }


  inline double deltaPhi(const Jet& j1, const Jet& j2) {
    return deltaPhi(j1.momentum(), j2.momentum());
  }

  inline double deltaPhi(const Jet& j, const Particle& p) {
    return deltaPhi(j.momentum(), p.momentum());
  }

  inline double deltaPhi(const Particle& p, const Jet& j) {
    return deltaPhi(p.momentum(), j.momentum());
  }

  inline double deltaPhi(const Jet& j, const FourMomentum& v) {
    return deltaPhi(j.momentum(), v);
  }

  inline double deltaPhi(const Jet& j, const FourVector& v) {
    return deltaPhi(j.momentum(), v);
  }

  inline double deltaPhi(const Jet& j, const Vector3& v) {
    return deltaPhi(j.momentum(), v);
  }

  inline double deltaPhi(const Jet& j, double phi) {
    return deltaPhi(j.momentum(), phi);
  }

  inline double deltaPhi(const FourMomentum& v, const Jet& j) {
    return deltaPhi(v, j.momentum());
  }

  inline double deltaPhi(const FourVector& v, const Jet& j) {
    return deltaPhi(v, j.momentum());
  }

  inline double deltaPhi(const Vector3& v, const Jet& j) {
    return deltaPhi(v, j.momentum());
  }

  inline double deltaPhi(double phi, const Jet& j) {
    return deltaPhi(phi, j.momentum());
  }


  inline double deltaEta(const Jet& j1, const Jet& j2) {
    return deltaEta(j1.momentum(), j2.momentum());
  }

  inline double deltaEta(const Jet& j, const Particle& p) {
    return deltaEta(j.momentum(), p.momentum());
  }

  inline double deltaEta(const Particle& p, const Jet& j) {
    return deltaEta(p.momentum(), j.momentum());
  }

  inline double deltaEta(const Jet& j, const FourMomentum& v) {
    return deltaEta(j.momentum(), v);
  }

  inline double deltaEta(const Jet& j, const FourVector& v) {
    return deltaEta(j.momentum(), v);
  }

  inline double deltaEta(const Jet& j, const Vector3& v) {
    return deltaEta(j.momentum(), v);
  }

  inline double deltaEta(const Jet& j, double eta) {
    return deltaEta(j.momentum(), eta);
  }

  inline double deltaEta(const FourMomentum& v, const Jet& j) {
    return deltaEta(v, j.momentum());
  }

  inline double deltaEta(const FourVector& v, const Jet& j) {
    return deltaEta(v, j.momentum());
  }

  inline double deltaEta(const Vector3& v, const Jet& j) {
    return deltaEta(v, j.momentum());
  }

  inline double deltaEta(double eta, const Jet& j) {
    return deltaEta(eta, j.momentum());
  }

}

#endif
