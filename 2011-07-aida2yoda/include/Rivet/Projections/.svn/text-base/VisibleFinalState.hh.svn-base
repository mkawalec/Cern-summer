// -*- C++ -*-
#ifndef RIVET_VisibleFinalState_HH
#define RIVET_VisibleFinalState_HH

#include "Rivet/Tools/Logging.hh"
#include "Rivet/Rivet.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"

namespace Rivet {


  /// @brief Final state modifier excluding particles which are not experimentally visible
  class VisibleFinalState : public FinalState {
  public:

    /// @name Constructors
    //@{

    /// Default constructor.
    VisibleFinalState();

    /// Constructor with min and max pseudorapidity \f$ \eta \f$ and min \f$ p_T \f$ (in GeV).
    VisibleFinalState(double mineta = -MAXRAPIDITY,
                      double maxeta =  MAXRAPIDITY,
                      double minpt  =  0.0*GeV);

    /// Constructor with specific FinalState.
    VisibleFinalState(const FinalState& fsp);

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new VisibleFinalState(*this);
    }

    //@}


  protected:

    /// Apply the projection on the supplied event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;

  };


}

#endif
