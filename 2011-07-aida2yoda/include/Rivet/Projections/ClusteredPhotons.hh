// -*- C++ -*-
#ifndef RIVET_ClusteredPhotons_HH
#define RIVET_ClusteredPhotons_HH

#include "Rivet/Tools/Logging.hh"
#include "Rivet/Rivet.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"

namespace Rivet {


  /// @brief Find final state photons which in a cone around any particle in the "signal" final state
  class ClusteredPhotons : public FinalState {
  public:

    /// @name Constructors
    //@{
    /// Constructor with the two final states, and the maximum separation in dR
    /// for clustered photons
    ClusteredPhotons(const FinalState& fs, const FinalState& signal, double dRmax)
      : _dRmax(dRmax)
    {
      setName("ClusteredPhotons");
      IdentifiedFinalState photonfs(fs);
      photonfs.acceptId(PHOTON);
      addProjection(photonfs, "Photons");
      addProjection(signal, "Signal");
    }


    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new ClusteredPhotons(*this);
    }
    //@}


  public:

  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;


  private:

    /// maximum cone radius to find photons in
    double _dRmax;

  };


}


#endif
