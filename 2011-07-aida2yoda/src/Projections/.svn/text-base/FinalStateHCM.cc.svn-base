// -*- C++ -*-
#include "Rivet/Projections/FinalStateHCM.hh"
#include "Rivet/Cmp.hh"


namespace Rivet {


  int FinalStateHCM::compare(const Projection& p) const {
    return mkNamedPCmp(p, "Kinematics");
  }


  void FinalStateHCM::project(const Event& e) {
    const DISKinematics& diskin = applyProjection<DISKinematics>(e, "Kinematics");
    const LorentzTransform hcmboost = diskin.boostHCM();
    const DISLepton& dislep = diskin.applyProjection<DISLepton>(e, "Lepton");
    const GenParticle& dislepGP = dislep.out().genParticle();
    const FinalState& fs = dislep.applyProjection<FinalState>(e, "FS");

    // Fill the particle list with all particles _other_ than the DIS scattered
    // lepton, with momenta boosted into the HCM frame.
    _theParticles.clear();
    _theParticles.reserve(fs.particles().size());
    for (ParticleVector::const_iterator p = fs.particles().begin(); p != fs.particles().end(); ++p) {
      const GenParticle& loopGP = p->genParticle();
      if (&loopGP != &dislepGP) { //< Ensure that we skip the DIS lepton
        Particle temp = *p;
        const FourMomentum hcmMom = hcmboost.transform(temp.momentum());
        temp.setMomentum(hcmMom);
        _theParticles.push_back(temp);
      }
    }
  }


}
