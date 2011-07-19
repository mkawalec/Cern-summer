// -*- C++ -*-
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/TotalVisibleMomentum.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {


  int TotalVisibleMomentum::compare(const Projection& p) const {
    return mkNamedPCmp(p, "FS");
  }


  void TotalVisibleMomentum::project(const Event& e) {
    _momentum = FourMomentum();
    _set = 0.0;

    // Project into final state
    const FinalState& fs = applyProjection<FinalState>(e, "FS");
    foreach (const Particle& p, fs.particles()) {
      const FourMomentum& mom = p.momentum();
      _momentum += mom;
      _set += mom.Et();
    }
  }


}
