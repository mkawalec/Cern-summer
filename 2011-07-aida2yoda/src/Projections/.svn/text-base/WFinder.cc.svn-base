// -*- C++ -*-
#include "Rivet/Projections/WFinder.hh"
#include "Rivet/Projections/InvMassFinalState.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/MergedFinalState.hh"
#include "Rivet/Projections/LeptonClusters.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Cmp.hh"

namespace Rivet {


  WFinder::WFinder(double etaMin, double etaMax,
                   double pTmin,
                   PdgId pid,
                   double m2_min, double m2_max,
                   double missingET,
                   double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS) {
    vector<pair<double, double> > etaRanges;
    etaRanges += std::make_pair(etaMin, etaMax);
    _init(etaRanges, pTmin, pid, m2_min, m2_max, missingET,
          dRmax, clusterPhotons, excludePhotonsFromRFS);
  }


  WFinder::WFinder(const std::vector<std::pair<double, double> >& etaRanges,
                   double pTmin,
                   PdgId pid,
                   double m2_min, double m2_max,
                   double missingET,
                   double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS) {
    _init(etaRanges, pTmin, pid, m2_min, m2_max, missingET,
          dRmax, clusterPhotons, excludePhotonsFromRFS);
  }


  void WFinder::_init(const std::vector<std::pair<double, double> >& etaRanges,
                      double pTmin,
                      PdgId pid,
                      double m2_min, double m2_max,
                      double missingET,
                      double dRmax, bool clusterPhotons, bool excludePhotonsFromRFS) 
  {
    setName("WFinder");




    // Check that the arguments are legal
    assert(abs(pid) == ELECTRON || abs(pid) == MUON);
    PdgId nu_pid = abs(pid) + 1;
    assert(abs(nu_pid) == NU_E || abs(nu_pid) == NU_MU);

    // Don't make pT or eta cuts on the neutrino
    IdentifiedFinalState fs_nu;
    fs_nu.acceptNeutrinos();

    // lepton clusters
    FinalState fs;
    IdentifiedFinalState bareleptons(fs);
    bareleptons.acceptIdPair(pid);
    LeptonClusters leptons(fs, bareleptons, dRmax,
                           clusterPhotons, excludePhotonsFromRFS,
                           etaRanges, pTmin);
    addProjection(leptons, "LeptonClusters");


    // Make a merged final state projection for charged and neutral leptons
    MergedFinalState mergedFS(leptons, fs_nu);

    // Make and register an invariant mass final state for the W decay leptons
    vector<pair<PdgId, PdgId> > l_nu_ids;
    l_nu_ids += make_pair(abs(pid), -abs(nu_pid));
    l_nu_ids += make_pair(-abs(pid), abs(nu_pid));
    InvMassFinalState imfs(mergedFS, l_nu_ids, m2_min, m2_max, 80.403);
    addProjection(imfs, "IMFS");

    // Add MissingMomentum proj to calc MET
    MissingMomentum vismom(fs);
    addProjection(vismom, "MissingET");
    // Set ETmiss
    _etMiss = missingET;

    // FS for non-signal bits of the event
    VetoedFinalState remainingFS;
    remainingFS.addVetoOnThisFinalState(leptons.constituentsFinalState());
    remainingFS.addVetoOnThisFinalState(fs_nu);
    addProjection(remainingFS, "RFS");
  }


  /////////////////////////////////////////////////////


  const FinalState& WFinder::remainingFinalState() const {
    return getProjection<FinalState>("RFS");
  }


  Particle WFinder::constituentLepton() const {
    const InvMassFinalState& imfs = getProjection<InvMassFinalState>("IMFS");
    assert(imfs.particles().size()==2);

    Particle p1,p2;
    p1 = imfs.particles()[0];
    p2 = imfs.particles()[1];
    if (abs(p1.pdgId()) == ELECTRON || abs(p1.pdgId()) == MUON) {
      return p1;
    }
    else {
      return p2;
    }
  }


  Particle WFinder::constituentNeutrino() const {
    const InvMassFinalState& imfs = getProjection<InvMassFinalState>("IMFS");
    assert(imfs.particles().size()==2);

    Particle p1,p2;
    p1 = imfs.particles()[0];
    p2 = imfs.particles()[1];
    if (abs(p1.pdgId()) == ELECTRON || abs(p1.pdgId()) == MUON) {
      return p2;
    }
    else {
      return p1;
    }
  }


  const FinalState& WFinder::originalLeptonFinalState() const
  {
    const LeptonClusters& leptons=getProjection<LeptonClusters>("LeptonClusters");
    return leptons.constituentsFinalState();
  }


  int WFinder::compare(const Projection& p) const {
    PCmp cmp = mkNamedPCmp(p, "IMFS");
    if (cmp != EQUIVALENT) return cmp;

    return EQUIVALENT;
  }


  void WFinder::clear() {
    _theParticles.clear();
  }


  void WFinder::project(const Event& e) {
    clear();

    const InvMassFinalState& imfs = applyProjection<InvMassFinalState>(e, "IMFS");
    applyProjection<FinalState>(e, "RFS");
    if (imfs.particles().size() != 2) return;

    Particle p1,p2;
    p1 = imfs.particles()[0];
    p2 = imfs.particles()[1];

    FourMomentum pW = p1.momentum() + p2.momentum();
    const int w3charge = PID::threeCharge(p1) + PID::threeCharge(p2);
    assert(abs(w3charge) == 3);
    const int wcharge = w3charge/3;

    stringstream msg;
    string wsign = (wcharge == 1) ? "+" : "-";
    string wstr = "W" + wsign;
    msg << wstr << " reconstructed from: " << endl
        << "   " << p1.momentum() << " " << p1.pdgId() << endl
        << " + " << p2.momentum() << " " << p2.pdgId() << endl;

    // Check missing ET
    const MissingMomentum& vismom = applyProjection<MissingMomentum>(e, "MissingET");
    /// @todo Restrict missing momentum eta range? Use vectorET()?
    if (vismom.scalarET() < _etMiss) {
      getLog() << Log::DEBUG << "Not enough missing ET: " << vismom.scalarET()/GeV
               << " GeV vs. " << _etMiss/GeV << " GeV" << endl;
      return;
    }

    // Make W Particle and insert into particles list
    const PdgId wpid = (wcharge == 1) ? WPLUSBOSON : WMINUSBOSON;
    _theParticles.push_back(Particle(wpid, pW));
  }


}
