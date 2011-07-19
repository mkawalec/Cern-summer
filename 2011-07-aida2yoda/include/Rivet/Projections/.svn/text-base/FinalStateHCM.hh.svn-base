// -*- C++ -*-
#ifndef RIVET_FinalStateHCM_HH
#define RIVET_FinalStateHCM_HH

#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/DISKinematics.hh"

namespace Rivet {


  /// @brief Final state particles boosted to the hadronic center of mass system.
  ///
  /// NB. The DIS scattered lepton is not included in the final state particles.
  class FinalStateHCM: public FinalState {

  public:

    /// Constructor
    FinalStateHCM(const DISKinematics& kinematicsp)
    {
      setName("FinalStateHCM");
      addProjection(kinematicsp, "Kinematics");
    }

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new FinalStateHCM(*this);
    }

  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;
  };

}


#endif
