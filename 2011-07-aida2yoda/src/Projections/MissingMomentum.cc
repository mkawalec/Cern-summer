// -*- C++ -*-
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {


  int MissingMomentum::compare(const Projection& p) const {
    return mkNamedPCmp(p, "VisibleFS");
  }


  void MissingMomentum::clear() {
    _momentum = FourMomentum();
    _set = 0.0;
  }


  void MissingMomentum::project(const Event& e) {
    clear();
    
    // Project into final state
    const FinalState& vfs = applyProjection<FinalState>(e, "VisibleFS");
    foreach (const Particle& p, vfs.particles()) {
      const FourMomentum& mom = p.momentum();
      _momentum += mom;
      _set += mom.Et();
    }
  }


}
