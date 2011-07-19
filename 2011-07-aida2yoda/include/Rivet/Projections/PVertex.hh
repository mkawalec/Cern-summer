// -*- C++ -*-
#ifndef RIVET_PVertex_HH
#define RIVET_PVertex_HH

#include "Rivet/Projection.hh"
#include "Rivet/Event.hh"
#include "Rivet/Particle.hh"

namespace Rivet {


  /// @brief Get the position of the primary vertex of an event.
  ///
  /// HepMC doesn't reliably return the signal process vertex, so
  /// we have to use the "decay vertex" of the beam particles.
  /// This gives the right position, within experimental resolution,
  /// but ISR effects can mean that the actual vertex is not right.
  /// Hence, we don't expose the HepMC GenVertex directly - if it were
  /// available, people might try to e.g. look at the \f$ p_T \f$
  /// of the vertex children, which would be extremely unreliable.
  ///
  /// @deprecated This should hardly ever be required for MC studies, and is not necessarily reliable!
  class PVertex : public Projection {
  public:

    /// @name Standard constructors and destructors.
    //@{

    /// The default constructor.
    PVertex()
      : _thePVertex(0)
    {
      setName("PVertex");
    }

    /// Clone on the heap.
    virtual const Projection* clone() const {
      return new PVertex(*this);
    }
    //@}


    /// Get the primary vertex position.
    const Vector3 position() const {
      if (_thePVertex != 0) return Vector3(_thePVertex->position());
      return Vector3(0,0,0);
    }


  protected:

    /// Do the projection.
    void project(const Event& e);


    /// Compare projections.
    int compare(const Projection& UNUSED(p)) const {
      return EQUIVALENT;
    }


  private:

    /// The Primary Vertex in the current collision.
    GenVertex* _thePVertex;

  };

}

#endif
