// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Cmp.hh"
#include <algorithm>

namespace Rivet {


  ChargedFinalState::ChargedFinalState(const FinalState& fsp) {
    setName("ChargedFinalState");
    addProjection(fsp, "FS");
  }


  ChargedFinalState::ChargedFinalState(double mineta, double maxeta, double minpt) {
    setName("ChargedFinalState");
    addProjection(FinalState(mineta, maxeta, minpt), "FS");
  }


  ChargedFinalState::ChargedFinalState(const vector<pair<double, double> >& etaRanges,
                                       double minpt) {
    setName("ChargedFinalState");
    addProjection(FinalState(etaRanges, minpt), "FS");
  }
  

  int ChargedFinalState::compare(const Projection& p) const {
    return mkNamedPCmp(p, "FS");
  }


  bool chargedParticleFilter(const Particle& p) {
    return PID::threeCharge(p.pdgId()) == 0;
  }


  void ChargedFinalState::project(const Event& e) {
    const FinalState& fs = applyProjection<FinalState>(e, "FS");
    _theParticles.clear();
    std::remove_copy_if(fs.particles().begin(), fs.particles().end(),
                        std::back_inserter(_theParticles), chargedParticleFilter);
    getLog() << Log::DEBUG << "Number of charged final-state particles = "
             << _theParticles.size() << endl;
    if (getLog().isActive(Log::TRACE)) {
      for (vector<Particle>::iterator p = _theParticles.begin(); p != _theParticles.end(); ++p) {
        getLog() << Log::TRACE << "Selected: " << p->pdgId()
                 << ", charge = " << PID::threeCharge(p->pdgId())/3.0 << endl;
      }
    }
  }


}
