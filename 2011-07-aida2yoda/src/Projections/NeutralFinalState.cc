// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/NeutralFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Cmp.hh"
#include <algorithm>

namespace Rivet {


  int NeutralFinalState::compare(const Projection& p) const {
    const NeutralFinalState& other = dynamic_cast<const NeutralFinalState&>(p);
    return mkNamedPCmp(other, "FS") || cmp(_Etmin, other._Etmin);
  }


  void NeutralFinalState::project(const Event& e) {
    const FinalState& fs = applyProjection<FinalState>(e, "FS");
    _theParticles.clear();
    foreach (const Particle& p, fs.particles()){
      if ((PID::threeCharge(p.pdgId()) == 0) && (p.momentum().Et() > _Etmin)) {
        _theParticles.push_back(p);
        if (getLog().isActive(Log::TRACE)) {
          getLog() << Log::TRACE
                   << "Selected: ID = " << p.pdgId()
                   << ", Et = " << p.momentum().Et()
                   << ", eta = " << p.momentum().eta()
                   << ", charge = " << PID::threeCharge(p.pdgId())/3.0 << endl;
        }
      }
    }
    getLog() << Log::DEBUG << "Number of neutral final-state particles = "
             << _theParticles.size() << endl;
  }


}
