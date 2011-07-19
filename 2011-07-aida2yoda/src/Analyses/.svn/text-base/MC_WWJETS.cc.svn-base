// -*- C++ -*-
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/WFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include "Rivet/RivetAIDA.hh"

namespace Rivet {

  /// @brief MC validation analysis for W^+[enu]W^-[munu] + jets events
  class MC_WWJETS : public MC_JetAnalysis {
  public:

    /// Default constructor
    MC_WWJETS()
      : MC_JetAnalysis("MC_WWJETS", 4, "Jets")
    {
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      WFinder wenufinder(-3.5, 3.5, 25.0*GeV, ELECTRON, 60.0*GeV, 100.0*GeV, 25.0*GeV, 0.2);
      addProjection(wenufinder, "WenuFinder");
      WFinder wmnufinder(-3.5, 3.5, 25.0*GeV, MUON, 60.0*GeV, 100.0*GeV, 25.0*GeV, 0.2);
      addProjection(wmnufinder, "WmnuFinder");
      VetoedFinalState jetinput;
      jetinput
        .addVetoOnThisFinalState(wenufinder.originalLeptonFinalState())
        .addVetoOnThisFinalState(wmnufinder.originalLeptonFinalState());
      FastJets jetpro(jetinput, FastJets::KT, 0.7);
      addProjection(jetpro, "Jets");

      // properties of the pair momentum
      _h_WW_pT = bookHistogram1D("WW_pT", logBinEdges(100, 1.0, 0.5*sqrtS()));
      _h_WW_pT_peak = bookHistogram1D("WW_pT_peak", 25, 0.0, 25.0);
      _h_WW_eta = bookHistogram1D("WW_eta", 40, -7.0, 7.0);
      _h_WW_phi = bookHistogram1D("WW_phi", 25, 0.0, TWOPI);
      _h_WW_m = bookHistogram1D("WW_m", logBinEdges(100, 150.0, 180.0+0.25*sqrtS()));

      // correlations between the WW
      _h_WW_dphi = bookHistogram1D("WW_dphi", 25, 0.0, PI);  /// @todo non-linear?
      _h_WW_deta = bookHistogram1D("WW_deta", 25, -7.0, 7.0);
      _h_WW_dR = bookHistogram1D("WW_dR", 25, 0.5, 7.0);
      _h_WW_dpT = bookHistogram1D("WW_dpT", logBinEdges(100, 1.0, 0.5*sqrtS()));
      _h_WW_costheta_planes = bookHistogram1D("WW_costheta_planes", 25, -1.0, 1.0);

      /// @todo fuer WW: missing ET

      // properties of the W bosons
      _h_W_pT = bookHistogram1D("W_pT", logBinEdges(100, 10.0, 0.25*sqrtS()));
      _h_W_eta = bookHistogram1D("W_eta", 70, -7.0, 7.0);

      // properties of the leptons
      _h_Wl_pT = bookHistogram1D("Wl_pT", logBinEdges(100, 30.0, 0.1
                                                      *sqrtS()));
      _h_Wl_eta = bookHistogram1D("Wl_eta", 40, -3.5, 3.5);

      // correlations between the opposite charge leptons
      _h_WeWm_dphi = bookHistogram1D("WeWm_dphi", 25, 0.0, PI);
      _h_WeWm_deta = bookHistogram1D("WeWm_deta", 25, -5.0, 5.0);
      _h_WeWm_dR = bookHistogram1D("WeWm_dR", 25, 0.5, 5.0);
      _h_WeWm_m = bookHistogram1D("WeWm_m", 100, 0.0, 300.0);

      // correlations with jets
      _h_WW_jet1_deta = bookHistogram1D("WW_jet1_deta", 70, -7.0, 7.0);
      _h_WW_jet1_dR = bookHistogram1D("WW_jet1_dR", 25, 1.5, 7.0);
      _h_We_jet1_dR = bookHistogram1D("We_jet1_dR", 25, 0.0, 7.0);

      // global stuff
      _h_HT = bookHistogram1D("HT", logBinEdges(100, 100.0, 0.5*sqrtS()));
      _h_jets_dphi_12 = bookHistogram1D("jets_dphi_12", 25, 0.0, PI);
      _h_jets_m_12 = bookHistogram1D("jets_m_12", logBinEdges(100, 1.0, 0.25*sqrtS()));

      MC_JetAnalysis::init();
    }



    /// Do the analysis
    void analyze(const Event & e) {
      const double weight = e.weight();

      const WFinder& wenufinder = applyProjection<WFinder>(e, "WenuFinder");
      if (wenufinder.particles().size()!=1) {
        vetoEvent;
      }

      const WFinder& wmnufinder = applyProjection<WFinder>(e, "WmnuFinder");
      if (wmnufinder.particles().size()!=1) {
        vetoEvent;
      }

      FourMomentum wenu(wenufinder.particles()[0].momentum());
      FourMomentum wmnu(wmnufinder.particles()[0].momentum());
      FourMomentum ww(wenu+wmnu);
      // find leptons
      FourMomentum ep=wenufinder.constituentLepton().momentum();
      FourMomentum enu=wenufinder.constituentNeutrino().momentum();
      FourMomentum mm=wmnufinder.constituentLepton().momentum();
      FourMomentum mnu=wmnufinder.constituentNeutrino().momentum();

      _h_WW_pT->fill(ww.pT(),weight);
      _h_WW_pT_peak->fill(ww.pT(),weight);
      _h_WW_eta->fill(ww.eta(),weight);
      _h_WW_phi->fill(ww.azimuthalAngle(),weight);
      double mww2=ww.mass2();
      if (mww2>0.0) _h_WW_m->fill(sqrt(mww2), weight);

      _h_WW_dphi->fill(mapAngle0ToPi(wenu.phi()-wmnu.phi()), weight);
      _h_WW_deta->fill(wenu.eta()-wmnu.eta(), weight);
      _h_WW_dR->fill(deltaR(wenu,wmnu), weight);
      _h_WW_dpT->fill(fabs(wenu.pT()-wmnu.pT()), weight);

      Vector3 crossWenu = ep.vector3().cross(enu.vector3());
      Vector3 crossWmnu = mm.vector3().cross(mnu.vector3());
      double costheta = crossWenu.dot(crossWmnu)/crossWenu.mod()/crossWmnu.mod();
      _h_WW_costheta_planes->fill(costheta, weight);

      _h_W_pT->fill(wenu.pT(),weight);
      _h_W_pT->fill(wmnu.pT(),weight);
      _h_W_eta->fill(wenu.eta(),weight);
      _h_W_eta->fill(wmnu.eta(),weight);

      _h_Wl_pT->fill(ep.pT(), weight);
      _h_Wl_pT->fill(mm.pT(), weight);
      _h_Wl_eta->fill(ep.eta(), weight);
      _h_Wl_eta->fill(mm.eta(), weight);

      _h_WeWm_dphi->fill(mapAngle0ToPi(ep.phi()-mm.phi()), weight);
      _h_WeWm_deta->fill(ep.eta()-mm.eta(), weight);
      _h_WeWm_dR->fill(deltaR(ep,mm), weight);
      double m2=FourMomentum(ep+mm).mass2();
      if (m2 < 0) m2 = 0.0;
      _h_WeWm_m->fill(sqrt(m2), weight);

      const FastJets& jetpro = applyProjection<FastJets>(e, "Jets");
      const Jets& jets = jetpro.jetsByPt(20.0*GeV);
      if (jets.size() > 0) {
        _h_WW_jet1_deta->fill(ww.eta()-jets[0].momentum().eta(), weight);
        _h_WW_jet1_dR->fill(deltaR(ww, jets[0].momentum()), weight);
        _h_We_jet1_dR->fill(deltaR(ep, jets[0].momentum()), weight);
      }

      double HT=ep.pT()+mm.pT()+FourMomentum(enu+mnu).pT();
      foreach (const Jet& jet, jets) {
        HT+=jet.momentum().pT();
      }
      if (HT>0.0) _h_HT->fill(HT, weight);

      if (jets.size()>1) {
        FourMomentum jet1(jets[0].momentum());
        FourMomentum jet2(jets[1].momentum());
        _h_jets_dphi_12->fill(mapAngle0ToPi(jet1.phi()-jet2.phi()), weight);
        _h_jets_m_12->fill(FourMomentum(jet1+jet2).mass(), weight);
      }

      MC_JetAnalysis::analyze(e);
    }


    /// Finalize
    void finalize() {
      double norm=crossSection()/sumOfWeights();
      scale(_h_WW_pT, norm);
      scale(_h_WW_pT_peak, norm);
      scale(_h_WW_eta, norm);
      scale(_h_WW_phi, norm);
      scale(_h_WW_m, norm);
      scale(_h_WW_dphi, norm);
      scale(_h_WW_deta, norm);
      scale(_h_WW_dR, norm);
      scale(_h_WW_dpT, norm);
      scale(_h_WW_costheta_planes, norm);
      scale(_h_W_pT, norm);
      scale(_h_W_eta, norm);
      scale(_h_Wl_pT, norm);
      scale(_h_Wl_eta, norm);
      scale(_h_WeWm_dphi, norm);
      scale(_h_WeWm_deta, norm);
      scale(_h_WeWm_dR, norm);
      scale(_h_WeWm_m, norm);
      scale(_h_WW_jet1_deta, norm);
      scale(_h_WW_jet1_dR, norm);
      scale(_h_We_jet1_dR, norm);
      scale(_h_jets_dphi_12, norm);
      scale(_h_jets_m_12, norm);
      scale(_h_HT, norm);

      MC_JetAnalysis::finalize();
    }

    //@}


  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D * _h_WW_pT;
    AIDA::IHistogram1D * _h_WW_pT_peak;
    AIDA::IHistogram1D * _h_WW_eta;
    AIDA::IHistogram1D * _h_WW_phi;
    AIDA::IHistogram1D * _h_WW_m;
    AIDA::IHistogram1D * _h_WW_dphi;
    AIDA::IHistogram1D * _h_WW_deta;
    AIDA::IHistogram1D * _h_WW_dR;
    AIDA::IHistogram1D * _h_WW_dpT;
    AIDA::IHistogram1D * _h_WW_costheta_planes;
    AIDA::IHistogram1D * _h_W_pT;
    AIDA::IHistogram1D * _h_W_eta;
    AIDA::IHistogram1D * _h_Wl_pT;
    AIDA::IHistogram1D * _h_Wl_eta;
    AIDA::IHistogram1D * _h_WeWm_dphi;
    AIDA::IHistogram1D * _h_WeWm_deta;
    AIDA::IHistogram1D * _h_WeWm_dR;
    AIDA::IHistogram1D * _h_WeWm_m;
    AIDA::IHistogram1D * _h_WW_jet1_deta;
    AIDA::IHistogram1D * _h_WW_jet1_dR;
    AIDA::IHistogram1D * _h_We_jet1_dR;
    AIDA::IHistogram1D * _h_jets_dphi_12;
    AIDA::IHistogram1D * _h_jets_m_12;
    AIDA::IHistogram1D * _h_HT;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_WWJETS> plugin_MC_WWJETS;

}
