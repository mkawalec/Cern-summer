// -*- C++ -*-
#include "Rivet/Projections/ClusteredPhotons.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {


  int ClusteredPhotons::compare(const Projection& p) const {
    const PCmp fscmp = mkNamedPCmp(p, "Photons");
    if (fscmp != EQUIVALENT) return fscmp;

    const PCmp sigcmp = mkNamedPCmp(p, "Signal");
    if (sigcmp != EQUIVALENT) return sigcmp;

    const ClusteredPhotons& other = dynamic_cast<const ClusteredPhotons&>(p);
    int rcmp = cmp(_dRmax, other._dRmax);
    return rcmp;
  }


  void ClusteredPhotons::project(const Event& e) {
    _theParticles.clear();
    if (!_dRmax > 0.0) return;

    const FinalState& photons = applyProjection<FinalState>(e, "Photons");
    const FinalState& signal = applyProjection<FinalState>(e, "Signal");

    foreach (const Particle& p, photons.particles()) {
      bool clustered = false;
      foreach (const Particle& l, signal.particles()) {
        // Only cluster photons around *charged* signal particles
        if (PID::threeCharge(l.pdgId()) == 0) continue;
        // Geometrically match momentum vectors
        const FourMomentum p_l = l.momentum();
        const FourMomentum p_P = p.momentum();
        if (deltaR(p_l.pseudorapidity(), p_l.azimuthalAngle(),
                   p_P.pseudorapidity(), p_P.azimuthalAngle()) < _dRmax) {
          clustered = true;
        }
      }
      if (clustered) _theParticles.push_back(p);
    }
    getLog() << Log::DEBUG << name() << " found " << _theParticles.size()
             << " matching photons." << endl;
  }

}
