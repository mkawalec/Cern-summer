// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Projections/HadronicFinalState.hh"
#include "Rivet/Cmp.hh"
#include <algorithm>

namespace Rivet {


  int HadronicFinalState::compare(const Projection& p) const {
    return FinalState::compare(p);
  }


  bool hadronFilter(const Particle& p) {
    return ! PID::isHadron(p.pdgId());
  }


  void HadronicFinalState::project(const Event& e) {
    FinalState fsp = static_cast<FinalState>(*this);
    const FinalState& fs = applyProjection(e, fsp);
    _theParticles.clear();
    std::remove_copy_if(fs.particles().begin(), fs.particles().end(),
                        std::back_inserter(_theParticles), hadronFilter);
    getLog() << Log::DEBUG << "Number of hadronic final-state particles = "
             << _theParticles.size() << endl;
  }

}
