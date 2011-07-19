// -*- C++ -*-
#include "Rivet/Projections/LeptonClusters.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {

  const FinalState& LeptonClusters::constituentsFinalState() const
  {
    return getProjection<FinalState>("Constituents");
  }


  int LeptonClusters::compare(const Projection& p) const {
    // Compare the two as final states (for pT and eta cuts)
    const LeptonClusters& other = dynamic_cast<const LeptonClusters&>(p);
    int fscmp = FinalState::compare(other);
    if (fscmp != EQUIVALENT) return fscmp;

    fscmp = mkNamedPCmp(p, "Constituents");
    return fscmp;
  }


  void LeptonClusters::project(const Event& e) {
    _theParticles.clear();

    const LeptonClustersConstituents& constituents =
        applyProjection<LeptonClustersConstituents>(e, "Constituents");

    foreach (const Particle& p, constituents.clusteredLeptons()) {
      if (accept(p)) {
        _theParticles.push_back(p);
      }
    }
  }



  int LeptonClustersConstituents::compare(const Projection& p) const {
    const PCmp fscmp = mkNamedPCmp(p, "Photons");
    if (fscmp != EQUIVALENT) return fscmp;

    const PCmp sigcmp = mkNamedPCmp(p, "Signal");
    if (sigcmp != EQUIVALENT) return sigcmp;

    const LeptonClustersConstituents& other = dynamic_cast<const LeptonClustersConstituents&>(p);
    return (cmp(_dRmax, other._dRmax) || cmp(_cluster, other._cluster) ||
            cmp(_track, other._track));
  }


  void LeptonClustersConstituents::project(const Event& e) {
    _theParticles.clear();
    _clusteredLeptons.clear();

    const FinalState& signal = applyProjection<FinalState>(e, "Signal");
    ParticleVector bareleptons=signal.particles();
    if (bareleptons.size()==0) return;

    for (size_t i=0; i<bareleptons.size(); ++i) {
      _theParticles.push_back(bareleptons[i]);
      _clusteredLeptons.push_back(Particle(bareleptons[i]));
    }

    const FinalState& photons = applyProjection<FinalState>(e, "Photons");
    foreach (const Particle& p, photons.particles()) {
      const FourMomentum p_P = p.momentum();
      double dRmin=_dRmax;
      int idx=-1;
      for (size_t i=0; i<bareleptons.size(); ++i) {
        FourMomentum p_l = bareleptons[i].momentum();
        // Only cluster photons around *charged* signal particles
        if (PID::threeCharge(bareleptons[i].pdgId()) == 0) continue;
        // Geometrically match momentum vectors
        double dR=deltaR(p_l, p_P);
        if (dR < dRmin) {
          dRmin=dR;
          idx=i;
        }
      }
      if (idx>-1) {
        if (_cluster) _clusteredLeptons[idx].setMomentum(_clusteredLeptons[idx].momentum()+p_P);
        if (_track) _theParticles.push_back(p);
      }
    }
  }

}
