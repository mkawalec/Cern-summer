#include "Rivet/Event.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/BeamConstraint.hh"
#include "HepMC/GenEvent.h"

namespace Rivet {


  void _geRot180x(GenEvent& ge) {
    for (HepMC::GenEvent::particle_iterator ip = ge.particles_begin(); ip != ge.particles_end(); ++ip) {
      const HepMC::FourVector& mom = (*ip)->momentum();
      (*ip)->set_momentum(HepMC::FourVector(mom.px(), -mom.py(), -mom.pz(), mom.e()));
    }
    for (HepMC::GenEvent::vertex_iterator iv = ge.vertices_begin(); iv != ge.vertices_end(); ++iv) {
      const HepMC::FourVector& pos = (*iv)->position();
      (*iv)->set_position(HepMC::FourVector(pos.x(), -pos.y(), -pos.z(), pos.t()));
    }
  }


  // Convert the GenEvent to use conventional alignment
  // (proton or electron on +ve z-axis?)
  // For example, FHerwig only produces DIS events in the
  // unconventional orientation and has to be corrected
  void Event::_geNormAlignment() {
    if (!_genEvent.valid_beam_particles()) return;
    typedef pair<HepMC::GenParticle*, HepMC::GenParticle*> GPPair;
    GPPair bps = _genEvent.beam_particles();
    //const PdgIdPair beamids = make_pdgid_pair(bps.first->pdg_id(), bps.second->pdg_id());
    //Log::getLog("Rivet.Event") << Log::TRACE << "Beam IDs: " << beamids << endl;
    const HepMC::GenParticle* plusgp = 0;
    bool rot = false;

    // Rotate e+- p and ppbar to put p along +z
    /// @todo e+ e- convention? B-factories different from LEP?
    // if (compatible(beamids, make_pdgid_pair(ELECTRON, PROTON)) ||
    //     compatible(beamids, make_pdgid_pair(POSITRON, PROTON)) ||
    //     compatible(beamids, make_pdgid_pair(ANTIPROTON, PROTON)) ) {
    //   Log::getLog("Rivet.Event") << Log::TRACE << "May need to rotate event..." << endl;
    if (bps.first->pdg_id() != PROTON || bps.second->pdg_id() != PROTON) {
      if (bps.first->pdg_id() == PROTON) {
        plusgp = bps.first;
      } else if (bps.second->pdg_id() == PROTON) {
        plusgp = bps.second;
      }
      if (plusgp && plusgp->momentum().pz() < 0) {
        rot = true;
      }
    }

    // Do the rotation
    if (rot) {
      if (Log::getLog("Rivet.Event").isActive(Log::TRACE)) {
        Log::getLog("Rivet.Event") << Log::TRACE << "Rotating event" << endl;
        Log::getLog("Rivet.Event") << Log::TRACE << "Before rotation: "
                                   << bps.first->pdg_id() << "@pz=" << bps.first->momentum().pz()/GeV << ", "
                                   << bps.second->pdg_id() << "@pz=" << bps.second->momentum().pz()/GeV << endl;
      }
      if (!_modGenEvent) _modGenEvent = new GenEvent(_genEvent);
      _geRot180x(*_modGenEvent);
    }
  }


  Event::Event(const GenEvent& ge)
    : _genEvent(ge), _modGenEvent(NULL), _weight(1.0)
  {
    // Set the weight if there is one, otherwise default to 1.0
    if (!_genEvent.weights().empty()) {
      _weight = ge.weights()[0];
    }

    // Use Rivet's preferred units if possible
    #ifdef HEPMC_HAS_UNITS
    if (_genEvent.momentum_unit()!=HepMC::Units::GEV ||
        _genEvent.length_unit()!=HepMC::Units::MM) {
      if (!_modGenEvent) _modGenEvent = new GenEvent(ge);
      _modGenEvent->use_units(HepMC::Units::GEV, HepMC::Units::MM);
    }
    #endif
 
    // Use the conventional alignment
    _geNormAlignment();

    // Debug printout to check that copying/magling has worked
    //_genEvent.print();
  }


  Event::Event(const Event& e)
    : _genEvent(e._genEvent), _modGenEvent(e._modGenEvent),
      _weight(e._weight)
  {
    //
  }


  Event::~Event() {
    if (_modGenEvent) delete _modGenEvent;
  }

  const GenEvent& Event::genEvent() const {
    if (_modGenEvent) return *_modGenEvent;
    return _genEvent;
  }


}
