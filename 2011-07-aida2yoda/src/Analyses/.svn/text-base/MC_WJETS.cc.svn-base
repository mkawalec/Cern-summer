// -*- C++ -*-
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/WFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetYODA.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"

namespace Rivet {


  /// @brief MC validation analysis for W + jets events
  class MC_WJETS : public MC_JetAnalysis {
  public:

    /// Default constructor
    MC_WJETS()
      : MC_JetAnalysis("MC_WJETS", 4, "Jets")
    {
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      WFinder wfinder(-3.5, 3.5, 25.0*GeV, ELECTRON, 60.0*GeV, 100.0*GeV, 25.0*GeV, 0.2);
      addProjection(wfinder, "WFinder");
      FastJets jetpro(wfinder.remainingFinalState(), FastJets::KT, 0.7);
      addProjection(jetpro, "Jets");

      _h_W_mass = bookHisto1D("W_mass", 50, 55.0, 105.0);
      _h_W_pT = bookHisto1D("W_pT", logBinEdges(100, 1.0, 0.5*sqrtS()));
      _h_W_pT_peak = bookHisto1D("W_pT_peak", 25, 0.0, 25.0);
      _h_W_y = bookHisto1D("W_y", 40, -4.0, 4.0);
      _h_W_phi = bookHisto1D("W_phi", 25, 0.0, TWOPI);
      _h_W_jet1_deta = bookHisto1D("W_jet1_deta", 50, -5.0, 5.0);
      _h_W_jet1_dR = bookHisto1D("W_jet1_dR", 25, 0.5, 7.0);
      _h_Wplus_pT = bookHisto1D("Wplus_pT", logBinEdges(25, 10.0, 0.5*sqrtS()));
      _h_Wminus_pT = bookHisto1D("Wminus_pT", logBinEdges(25, 10.0, 0.5*sqrtS()));
      _h_lepton_pT = bookHisto1D("lepton_pT", logBinEdges(100, 10.0, 0.25*sqrtS()));
      _h_lepton_eta = bookHisto1D("lepton_eta", 40, -4.0, 4.0);
      _htmp_dsigminus_deta = bookHisto1D("lepton_dsigminus_deta", 20, 0.0, 4.0);
      _htmp_dsigplus_deta  = bookHisto1D("lepton_dsigplus_deta", 20, 0.0, 4.0);

      MC_JetAnalysis::init();
    }



    /// Do the analysis
    void analyze(const Event & e) {
      const WFinder& wfinder = applyProjection<WFinder>(e, "WFinder");
      if (wfinder.particles().size() != 1) {
        vetoEvent;
      }
      const double weight = e.weight();

      double charge3_x_eta = 0;
      int charge3 = 0;
      FourMomentum emom;
      FourMomentum wmom(wfinder.particles().front().momentum());
      _h_W_mass->fill(wmom.mass(), weight);
      _h_W_pT->fill(wmom.pT(), weight);
      _h_W_pT_peak->fill(wmom.pT(), weight);
      _h_W_y->fill(wmom.rapidity(), weight);
      _h_W_phi->fill(wmom.azimuthalAngle(), weight);
      Particle l=wfinder.constituentLepton();
      _h_lepton_pT->fill(l.momentum().pT(), weight);
      _h_lepton_eta->fill(l.momentum().eta(), weight);
      if (PID::threeCharge(l.pdgId()) != 0) {
        emom = l.momentum();
        charge3_x_eta = PID::threeCharge(l.pdgId()) * emom.eta();
        charge3 = PID::threeCharge(l.pdgId());
      }
      assert(charge3_x_eta != 0);
      assert(charge3!=0);
      if (emom.Et() > 30/GeV) {
        if (charge3_x_eta < 0) {
          _htmp_dsigminus_deta->fill(emom.eta(), weight);
        } else {
          _htmp_dsigplus_deta->fill(emom.eta(), weight);
        }
      }
      if (charge3 < 0) {
        _h_Wminus_pT->fill(wmom.pT(), weight);
      } else {
        _h_Wplus_pT->fill(wmom.pT(), weight);
      }

      const FastJets& jetpro = applyProjection<FastJets>(e, "Jets");
      const Jets& jets = jetpro.jetsByPt(20.0*GeV);
      if (jets.size() > 0) {
        _h_W_jet1_deta->fill(wmom.eta()-jets[0].momentum().eta(), weight);
        _h_W_jet1_dR->fill(deltaR(wmom, jets[0].momentum()), weight);
      }

      MC_JetAnalysis::analyze(e);
    }


    /// Finalize
    void finalize() {
      scale(_h_W_mass, crossSection()/sumOfWeights());
      scale(_h_W_pT, crossSection()/sumOfWeights());
      scale(_h_W_pT_peak, crossSection()/sumOfWeights());
      scale(_h_W_y, crossSection()/sumOfWeights());
      scale(_h_W_phi, crossSection()/sumOfWeights());
      scale(_h_W_jet1_deta, crossSection()/sumOfWeights());
      scale(_h_W_jet1_dR, crossSection()/sumOfWeights());
      scale(_h_lepton_pT, crossSection()/sumOfWeights());
      scale(_h_lepton_eta, crossSection()/sumOfWeights());

      // Construct asymmetry: (dsig+/deta - dsig-/deta) / (dsig+/deta + dsig-/deta) for each Et region
      // \todo YODA
      // AIDA::IHistogramFactory& hf = histogramFactory();
      // IHistogram1D* numtmp = hf.subtract("/numtmp", *_htmp_dsigplus_deta, *_htmp_dsigminus_deta);
      // IHistogram1D* dentmp = hf.add("/dentmp", *_htmp_dsigplus_deta, *_htmp_dsigminus_deta);
      // assert(numtmp && dentmp);
      // hf.divide(histoDir() + "/W_chargeasymm_eta", *numtmp, *dentmp);
      // hf.destroy(numtmp);
      // hf.destroy(dentmp);
      // hf.destroy(_htmp_dsigminus_deta);
      // hf.destroy(_htmp_dsigplus_deta);

      // // W charge asymmetry vs. pTW: dsig+/dpT / dsig-/dpT
      // hf.divide(histoDir() + "/W_chargeasymm_pT", *_h_Wplus_pT, *_h_Wminus_pT);
      scale(_h_Wplus_pT, crossSection()/sumOfWeights());
      scale(_h_Wminus_pT, crossSection()/sumOfWeights());

      MC_JetAnalysis::finalize();
    }

    //@}


  private:

    /// @name Histograms
    //@{
    Histo1DPtr _h_W_mass;
    Histo1DPtr _h_W_pT;
    Histo1DPtr _h_W_pT_peak;
    Histo1DPtr _h_W_y;
    Histo1DPtr _h_W_phi;
    Histo1DPtr _h_W_jet1_deta;
    Histo1DPtr _h_W_jet1_dR;
    Histo1DPtr _h_Wplus_pT;
    Histo1DPtr _h_Wminus_pT;
    Histo1DPtr _h_lepton_pT;
    Histo1DPtr _h_lepton_eta;

    Histo1DPtr _htmp_dsigminus_deta;
    Histo1DPtr _htmp_dsigplus_deta;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_WJETS> plugin_MC_WJETS;

}
