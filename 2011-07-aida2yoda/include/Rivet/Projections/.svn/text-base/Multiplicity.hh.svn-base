// -*- C++ -*-
#ifndef RIVET_Multiplicity_HH
#define RIVET_Multiplicity_HH

#include "Rivet/Projection.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"


namespace Rivet {

  /// @brief Count the final-state particles in an event.
  class Multiplicity : public Projection {
  public:

    /// Constructor. The provided FinalState projection must live throughout the run.
    Multiplicity(const FinalState& fsp)
      : _totalMult(0), _hadMult(0)
    {
      setName("Multiplicity");
      addProjection(fsp, "FS");
    }

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new Multiplicity(*this);
    }


  protected:

    /// Perform the projection on the Event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;


  public:

    /// @name Access the projected multiplicities.
    //@ {
    /// Total multiplicity
    unsigned int totalMultiplicity() const { return _totalMult; }

    /// Hadron multiplicity
    unsigned int hadronMultiplicity() const { return _hadMult; }
    //@ }

  private:

    /// Total multiplicity.
    unsigned int _totalMult;

    /// Hadronic multiplicity.
    unsigned int _hadMult;
  };

}

#endif
