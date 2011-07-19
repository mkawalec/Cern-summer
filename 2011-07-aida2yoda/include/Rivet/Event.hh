// -*- C++ -*-
#ifndef RIVET_Event_HH
#define RIVET_Event_HH

#include "Rivet/Rivet.hh"
#include "Rivet/Projection.hh"

namespace Rivet {


  /// Rivet wrapper for HepMC event and Projection references.
  ///
  /// Event is a concrete class representing an generated event in
  /// Rivet. It is constructed given a HepMC::GenEvent, a pointer to
  /// which is kept by the Event object throughout its lifetime. The user
  /// must therefore make sure that the corresponding HepMC::GenEvent
  /// will persist at least as long as the Event object.
  ///
  /// In addition to the HepMC::GenEvent object the Event also keeps
  /// track of all Projections object which have been applied to the
  /// Event so far.
  class Event {
  public:

    /// @name Standard constructors and destructors.
    //@{

    /// The default constructor.
    Event(const GenEvent& ge);

    /// The copy constructor.
    Event(const Event& e);

    /// The destructor
    ~Event();

    //@}


  public:

    /// Return the generated event obtained from an external event generator.
    const GenEvent& genEvent() const;

    /// The weight associated with the event.
    double weight() const {
      return _weight;
    }


  public:

    /// Add a projection \a p to this Event. If an equivalent Projection
    /// has been applied before, the Projection::project(const Event &)
    /// of \a p is not called and a reference to the previous equivalent
    /// projection is returned. If no previous Projection was found, the
    /// Projection::project(const Event &) of \a p is called and a
    /// reference to p is returned.
    template <typename PROJ>
    const PROJ& applyProjection(PROJ& p) const {
      const Projection* cpp(&p);
      std::set<const Projection*>::const_iterator old = _projections.find(cpp);
      if (old != _projections.end()) {
        const Projection& pRef = **old;
        return pcast<PROJ>(pRef);
      }
      // Add the projection via the Projection base class (only
      // possible because Event is a friend of Projection)
      Projection* pp = const_cast<Projection*>(cpp);
      pp->project(*this);
      _projections.insert(pp);
      return p;
    }


    template <typename PROJ>
    const PROJ& applyProjection(PROJ* pp) const {
      if (!pp) throw Error("Event::applyProjection(PROJ*): Projection pointer is null.");
      return applyProjection(*pp);
    }


  private:
    void _geNormAlignment();


    /// @brief The generated event, obtained from an external generator.
    /// Note that it is only externally accessible via a const reference.
    GenEvent const& _genEvent;

    GenEvent* _modGenEvent;

    /// The set of Projection objects applied so far.
    mutable std::set<ConstProjectionPtr> _projections;

    /// @brief The generation weight associated with the event.
    /// Usually 1.0. Only copied from the HepMC event once, at construction time.
    double _weight;

  };


}

#endif
