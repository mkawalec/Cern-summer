// -*- C++ -*-
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/InvMassFinalState.hh"
#include "Rivet/Projections/ClusteredPhotons.hh"
#include "Rivet/Projections/LeptonClusters.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {


  ZFinder::ZFinder(double etaMin, double etaMax,
                   double pTmin,
                   PdgId pid,
                   double m2_min, double m2_max,
                   double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS) {
    vector<pair<double, double> > etaRanges;
    etaRanges += std::make_pair(etaMin, etaMax);
    _init(etaRanges, pTmin, pid, m2_min, m2_max, dRmax, clusterPhotons, excludePhotonsFromRFS);
  }


  ZFinder::ZFinder(const std::vector<std::pair<double, double> >& etaRanges,
                   double pTmin,
                   PdgId pid,
                   double m2_min, const double m2_max,
                   double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS) {
    _init(etaRanges, pTmin, pid, m2_min, m2_max, dRmax, clusterPhotons, excludePhotonsFromRFS);
  }


  void ZFinder::_init(const std::vector<std::pair<double, double> >& etaRanges,
                      double pTmin,  PdgId pid,
                      double m2_min, double m2_max,
                      double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS)
  {
    setName("ZFinder");

    FinalState fs;
    IdentifiedFinalState bareleptons(fs);
    bareleptons.acceptIdPair(pid);
    LeptonClusters leptons(fs, bareleptons, dRmax,
                           clusterPhotons, excludePhotonsFromRFS,
                           etaRanges, pTmin);
    addProjection(leptons, "LeptonClusters");
    InvMassFinalState imfs(leptons, std::make_pair(pid, -pid), m2_min, m2_max);
    addProjection(imfs, "IMFS");

    VetoedFinalState remainingFS;
    remainingFS.addVetoOnThisFinalState(leptons.constituentsFinalState());
    addProjection(remainingFS, "RFS");
  }


  /////////////////////////////////////////////////////


  const FinalState& ZFinder::remainingFinalState() const
  {
    return getProjection<FinalState>("RFS");
  }


  const FinalState& ZFinder::constituentsFinalState() const
  {
    return getProjection<FinalState>("IMFS");
  }

  const FinalState& ZFinder::originalConstituentsFinalState() const
  {
    const LeptonClusters& leptons=getProjection<LeptonClusters>("LeptonClusters");
    return leptons.constituentsFinalState();
  }

  int ZFinder::compare(const Projection& p) const {
    //std::cout<<"Comparing ZFinder"<<std::endl;
    PCmp cmp = mkNamedPCmp(p, "IMFS");
    //std::cout<<"Result "<<(int)cmp<<std::endl;
    if (cmp != EQUIVALENT) return cmp;

    return EQUIVALENT;
  }


  void ZFinder::project(const Event& e) {
    _theParticles.clear();

    const FinalState& imfs=applyProjection<FinalState>(e, "IMFS");
    applyProjection<FinalState>(e, "RFS");
    if (imfs.particles().size() != 2) return;
    FourMomentum pZ = imfs.particles()[0].momentum() + imfs.particles()[1].momentum();
    const int z3charge = PID::threeCharge(imfs.particles()[0].pdgId()) + PID::threeCharge(imfs.particles()[1].pdgId());
    assert(z3charge == 0);

    stringstream msg;
    msg << "Z reconstructed from: " << endl
        << "   " << imfs.particles()[0].momentum() << " " << imfs.particles()[0].pdgId() << endl
        << " + " << imfs.particles()[1].momentum() << " " << imfs.particles()[1].pdgId() << endl;

    Particle Z;
    Z.setMomentum(pZ);
    _theParticles.push_back(Z);
    getLog() << Log::DEBUG << name() << " found one Z." << endl;
  }


}
