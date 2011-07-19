// -*- C++ -*-
#ifndef RIVET_IdentifiedFinalState_HH
#define RIVET_IdentifiedFinalState_HH

#include "Rivet/Tools/Logging.hh"
#include "Rivet/Rivet.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/FinalState.hh"

namespace Rivet {


  /// @brief Produce a final state which only contains specified particle IDs.
  class IdentifiedFinalState : public FinalState {
  public:

    /// @name Constructors
    //@{

    /// Constructor with specific FinalState.
    IdentifiedFinalState(const FinalState& fsp);

    /// Constructor with a single eta range argument.
    IdentifiedFinalState(double etamin=-MAXRAPIDITY,
                         double etamax=MAXRAPIDITY,
                         double ptMin=0.0*GeV);

    /// Constructor which allows to specify multiple eta ranges
    /// and the min \f$ p_T \f$.
    IdentifiedFinalState(const vector<pair<double, double> >& etaRanges,
                         double ptMin=0.0*GeV);

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new IdentifiedFinalState(*this);
    }
    //@}


  public:

    /// Get the list of particle IDs to accept.
    const set<PdgId>& acceptedIds() const {
      return _pids;
    }

    /// Add an accepted particle ID.
    IdentifiedFinalState& acceptId(PdgId pid) {
      _pids.insert(pid);
      return *this;
    }

    /// Add a set of accepted particle IDs.
    IdentifiedFinalState& acceptIds(const vector<PdgId>& pids) {
      foreach (const PdgId pid, pids) {
        _pids.insert(pid);
      }
      return *this;
    }

    /// Add an accepted particle ID and its antiparticle.
    IdentifiedFinalState& acceptIdPair(PdgId pid) {
      _pids.insert(pid);
      _pids.insert(-pid);
      return *this;
    }

    /// Add a set of accepted particle IDs and their antiparticles.
    IdentifiedFinalState& acceptIdPairs(const vector<PdgId>& pids) {
      foreach (const PdgId pid, pids) {
        _pids.insert(pid);
        _pids.insert(-pid);
      }
      return *this;
    }

    /// Accept all neutrinos (convenience method).
    IdentifiedFinalState& acceptNeutrinos() {
      acceptIdPair(NU_E);
      acceptIdPair(NU_MU);
      acceptIdPair(NU_TAU);
      return *this;
    }

    /// Accept all charged leptons (convenience method).
    IdentifiedFinalState& acceptChLeptons() {
      acceptIdPair(ELECTRON);
      acceptIdPair(MUON);
      acceptIdPair(TAU);
      return *this;
    }

    /// Reset the list of particle IDs to accept.
    void reset() {
      _pids.clear();
    }


  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;


  private:

    /// The final-state particles.
    set<PdgId> _pids;

  };


}


#endif
