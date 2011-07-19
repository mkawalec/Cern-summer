// -*- C++ -*-
#ifndef RIVET_TotalVisibleMomentum_HH
#define RIVET_TotalVisibleMomentum_HH

#include "Rivet/Rivet.hh"
#include "Rivet/Projection.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Particle.hh"
#include "Rivet/Event.hh"

namespace Rivet {


  /// @brief Get the total energy vector, allowing missing \f$ E_T \f$ etc. to be calculated.
  /// @deprecated This is confusing because the visibility is not automatic. Use MissingMomentum instead.
  class TotalVisibleMomentum : public Projection {

  public:

    /// Constructor. Make sure you supply an appropriately vetoed FS!
    TotalVisibleMomentum(const FinalState& fsp)
    {
      setName("TotalVisibleMomentum");
      addProjection(fsp, "FS");
      getLog() << Log::WARNING << "TotalVisibleMomentum projection is deprecated: "
               << "please use the MissingMomentum projection instead." << endl;
    }

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new TotalVisibleMomentum(*this);
    }


  public:
    /// The projected four-momentum vector
    FourMomentum& momentum() { return _momentum; }

    /// The projected four-momentum vector
    const FourMomentum& momentum() const { return _momentum; }

    /// The projected scalar transverse energy
    double scalarET() const { return _set; }


  protected:

    /// Apply the projection to the event.
    void project(const Event& e);

    /// Compare projections.
    int compare(const Projection& p) const;

  private:

    /// The total visible momentum
    FourMomentum _momentum;

    /// Scalar transverse energy
    double _set;

  };

}


#endif
