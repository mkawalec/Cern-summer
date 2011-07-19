// -*- C++ -*-
#include "Rivet/Projections/UnstableFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Cmp.hh"

#define IS_PARTON_PDGID(id) ( abs(id) <= 100 && abs(id) != 22 && (abs(id) < 11 || abs(id) > 18) )

namespace Rivet {


  int UnstableFinalState::compare(const Projection& p) const {
    const UnstableFinalState& other = dynamic_cast<const UnstableFinalState&>(p);
    return \
      cmp(_etamin, other._etamin) ||
      cmp(_etamax, other._etamax) ||
      cmp(_ptmin, other._ptmin);
  }


  void UnstableFinalState::project(const Event& e) {
    _theParticles.clear();

    foreach (GenParticle* p, Rivet::particles(e.genEvent())) {
      const int st = p->status();
      bool passed = \
        ( st == 1 || (st == 2 && abs(p->pdg_id()) != 22) ) &&
        !isZero(p->momentum().perp()) && p->momentum().perp() >= _ptmin &&
        p->momentum().eta() > _etamin && p->momentum().eta() < _etamax &&
        !IS_PARTON_PDGID(p->pdg_id());

      // DEBUGGING PRINTOUTS FOR HERWIG
      // if (p->status() == 2) {
      //   std::cout << "* "
      //             << "pid=" << p->pdg_id()
      //             << ", st=" << st
      //             << ", passed=" << std::boolalpha << passed
      //             << ", isparton=" << std::boolalpha << (IS_PARTON_PDGID(p->pdg_id())) << std::endl;
      // }
      // if (abs(p->pdg_id()) > 3000) {
      //   std::cout << "% "
      //             << "pid=" << p->pdg_id()
      //             << ", st=" << st
      //             << ", passed=" << std::boolalpha << passed
      //             << ", isparton=" << std::boolalpha << (IS_PARTON_PDGID(p->pdg_id())) << std::endl;
      // }

      // Avoid double counting by re-marking as unpassed if particle ID == parent ID
      const GenVertex* pv = p->production_vertex();
      const GenVertex* dv = p->end_vertex();
      if (passed && pv) {
        for (GenVertex::particles_in_const_iterator pp = pv->particles_in_const_begin() ;
             pp != pv->particles_in_const_end() ; ++pp) {
          if ( p->pdg_id() == (*pp)->pdg_id() ) {
            passed = false;
            break;
          }
        }
      }

      // Add to output particles collection
      if (passed) {
        _theParticles.push_back(Particle(*p));
      }

      // Log parents and children
      if (getLog().isActive(Log::TRACE)) {
        MSG_TRACE("ID = " << p->pdg_id()
                  << ", status = " << st
                  << ", pT = " << p->momentum().perp()
                  << ", eta = " << p->momentum().eta()
                  << ": result = " << std::boolalpha << passed);
        if (pv) {
          for (GenVertex::particles_in_const_iterator pp = pv->particles_in_const_begin() ;
               pp != pv->particles_in_const_end() ; ++pp) {
            MSG_TRACE("  parent ID = " << (*pp)->pdg_id());
          }
        }
        if (dv) {
          for (GenVertex::particles_out_const_iterator pp = dv->particles_out_const_begin() ;
               pp != dv->particles_out_const_end() ; ++pp) {
            MSG_TRACE("  child ID  = " << (*pp)->pdg_id());
          }
        }
      }
    }
    MSG_DEBUG("Number of final-state particles = " << _theParticles.size());
  }


}
