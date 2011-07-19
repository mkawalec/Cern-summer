// -*- C++ -*-
#ifndef RIVET_UnstableFinalState_HH
#define RIVET_UnstableFinalState_HH

#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"

namespace Rivet {


  /// @brief Project out all physical-but-decayed particles in an event.
  class UnstableFinalState : public FinalState {
  public:

    /// @name Standard constructors and destructors.
    //@{
    /// The default constructor. May specify the minimum and maximum
    /// pseudorapidity \f$ \eta \f$ and the min \f$ p_T \f$ (in GeV).
    UnstableFinalState(double mineta = -MAXRAPIDITY,
                       double maxeta =  MAXRAPIDITY,
                       double minpt  =  0.0*GeV)
      : _etamin(mineta), _etamax(maxeta), _ptmin(minpt)
    {
      setName("UnstableFinalState");
      // addCut("eta", MORE_EQ, mineta);
      // addCut("eta", LESS_EQ, maxeta);
      // addCut("pT",  MORE_EQ, minpt);
    }


    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new UnstableFinalState(*this);
    }
    //@}

    /// Access the projected final-state particles.
    virtual const ParticleVector& particles() const { return _theParticles; }

    /// Is this final state empty?
    virtual bool empty() const { return _theParticles.empty(); }

    /// @deprecated Is this final state empty?
    virtual bool isEmpty() const { return _theParticles.empty(); }


  protected:

    /// Apply the projection to the event.
    virtual void project(const Event& e);

    /// Compare projections.
    virtual int compare(const Projection& p) const;


  protected:

    /// The minimum allowed pseudorapidity.
    double _etamin;

    /// The maximum allowed pseudorapidity.
    double _etamax;

    /// The minimum allowed transverse momentum.
    double _ptmin;

    /// The final-state particles.
    ParticleVector _theParticles;

  };


}


#endif
