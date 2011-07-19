// -*- C++ -*-
#ifndef RIVET_InvMassFinalState_HH
#define RIVET_InvMassFinalState_HH

#include "Rivet/Projections/FinalState.hh"

namespace Rivet {


  /// @brief Identify particles which can be paired to fit within a given invariant mass window
  class InvMassFinalState : public FinalState {
  public:

    // Constructor for a single inv-mass pair
    InvMassFinalState(const FinalState& fsp,
                      const std::pair<PdgId, PdgId>& idpair, // pair of decay products
                      double minmass, // min inv mass
                      double maxmass, // max inv mass
                      double masstarget=-1.0);


    InvMassFinalState(const FinalState& fsp,
                      const std::vector<std::pair<PdgId, PdgId> >& idpairs,  // vector of pairs of decay products
                      double minmass, // min inv mass
                      double maxmass, // max inv mass
                      double masstarget=-1.0);


    /// Clone on the heap.
    virtual const Projection* clone() const {
    	return new InvMassFinalState(*this);
    }


  public:

    /// Constituent pairs
    const std::vector<std::pair<Particle, Particle> >& particlePairs() const;


  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;


  private:

    /// IDs of the decay products
    std::vector<PdgIdPair> _decayids;

    /// Constituent pairs
    std::vector<std::pair<Particle, Particle> > _particlePairs;

    /// Min inv mass
    double _minmass;

    /// Max inv mass
    double _maxmass;

    /// Target mass if only one pair should be returned
    double _masstarget;

  };


}


#endif
