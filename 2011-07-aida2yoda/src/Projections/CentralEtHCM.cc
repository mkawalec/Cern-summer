// -*- C++ -*-
#include "Rivet/Rivet.hh"
#include "Rivet/Projections/CentralEtHCM.hh"
#include "Rivet/Cmp.hh"


namespace Rivet {

  int CentralEtHCM::compare(const Projection& p) const {
    return mkNamedPCmp(p, "FS");
  }


  void CentralEtHCM::project(const Event& e) {
    const FinalStateHCM& fs = applyProjection<FinalStateHCM>(e, "FS");
    _sumet = 0.0;
    for (ParticleVector::const_iterator p = fs.particles().begin(); p != fs.particles().end(); ++p) {
      /// @todo Can this extra rapidity cut be implemented so as to use the cached rapidity result?
      // Rapidity cut: |rapidity| < 0.5
      const FourMomentum p4 = p->momentum();
      if (fabs(p4.rapidity()) < 0.5) _sumet += p4.Et();
    }
  }

}
