// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/MergedFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Cmp.hh"
#include <algorithm>

namespace Rivet {


  int MergedFinalState::compare(const Projection& p) const {
    /// @todo: Currently A+B is not recognised to be the same as B+A.
    return mkNamedPCmp(p, "FSA") || mkNamedPCmp(p, "FSB");
  }


  void MergedFinalState::project(const Event& e) {
    const FinalState& fsa = applyProjection<FinalState>(e, "FSA");
    const FinalState& fsb = applyProjection<FinalState>(e, "FSB");
    _theParticles.clear();
    foreach (const Particle& pa, fsa.particles()){
      _theParticles.push_back(pa);
    }
    foreach (const Particle& pb, fsb.particles()){
      const GenParticle* originalb = &(pb.genParticle());
      bool notfound = true;
      foreach (const Particle& pa, fsa.particles()){
        const GenParticle* originala = &(pa.genParticle());
        if (originala == originalb) {
          notfound = false;
          break;
        }
      }
      if (notfound) {
        _theParticles.push_back(pb);
      }
    }
    getLog() << Log::DEBUG << "Number of particles in the two final states to be merged: = \n"
             << "   1st final state = " << fsa.particles().size() << endl
             << "   2nd final state = " << fsb.particles().size() << endl;
    getLog() << Log::DEBUG << "Number of merged final-state particles = "
             << _theParticles.size() << endl;
  }


}
