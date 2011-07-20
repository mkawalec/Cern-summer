// -*- C++ -*-
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetYODA.hh"

namespace Rivet {


  /// @brief MC validation analysis for higgs [-> tau tau] + jets events
  class MC_HJETS : public MC_JetAnalysis {
  public:

    /// Default constructor
    MC_HJETS()
      : MC_JetAnalysis("MC_HJETS", 4, "Jets")
    {
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      ZFinder hfinder(-3.5, 3.5, 25.0*GeV, TAU, 115.0*GeV, 125.0*GeV, 0.0, false, false);
      addProjection(hfinder, "Hfinder");
      FastJets jetpro(hfinder.remainingFinalState(), FastJets::KT, 0.7);
      addProjection(jetpro, "Jets");

      _h_H_mass = bookHisto1D("H_mass", 50, 119.7, 120.3);
      _h_H_pT = bookHisto1D("H_pT", logBinEdges(100, 1.0, 0.5*sqrtS()));
      _h_H_pT_peak = bookHisto1D("H_pT_peak", 25, 0.0, 25.0);
      _h_H_y = bookHisto1D("H_y", 40, -4.0, 4.0);
      _h_H_phi = bookHisto1D("H_phi", 25, 0.0, TWOPI);
      _h_H_jet1_deta = bookHisto1D("H_jet1_deta", 50, -5.0, 5.0);
      _h_H_jet1_dR = bookHisto1D("H_jet1_dR", 25, 0.5, 7.0);
      _h_lepton_pT = bookHisto1D("lepton_pT", logBinEdges(100, 10.0, 0.25*sqrtS()));
      _h_lepton_eta = bookHisto1D("lepton_eta", 40, -4.0, 4.0);

      MC_JetAnalysis::init();
    }



    /// Do the analysis
    void analyze(const Event & e) {
      const ZFinder& hfinder = applyProjection<ZFinder>(e, "Hfinder");
      if (hfinder.particles().size()!=1) {
        vetoEvent;
      }
      const double weight = e.weight();

      FourMomentum hmom(hfinder.particles()[0].momentum());
      _h_H_mass->fill(hmom.mass(),weight);
      _h_H_pT->fill(hmom.pT(),weight);
      _h_H_pT_peak->fill(hmom.pT(),weight);
      _h_H_y->fill(hmom.rapidity(),weight);
      _h_H_phi->fill(hmom.azimuthalAngle(),weight);
      foreach (const Particle& l, hfinder.constituentsFinalState().particles()) {
        _h_lepton_pT->fill(l.momentum().pT(), weight);
        _h_lepton_eta->fill(l.momentum().eta(), weight);
      }

      const FastJets& jetpro = applyProjection<FastJets>(e, "Jets");
      const Jets& jets = jetpro.jetsByPt(20.0*GeV);
      if (jets.size() > 0) {
        _h_H_jet1_deta->fill(hmom.eta()-jets[0].momentum().eta(), weight);
        _h_H_jet1_dR->fill(deltaR(hmom, jets[0].momentum()), weight);
      }

      MC_JetAnalysis::analyze(e);
    }


    /// Finalize
    void finalize() {
      scale(_h_H_mass, crossSection()/sumOfWeights());
      scale(_h_H_pT, crossSection()/sumOfWeights());
      scale(_h_H_pT_peak, crossSection()/sumOfWeights());
      scale(_h_H_y, crossSection()/sumOfWeights());
      scale(_h_H_phi, crossSection()/sumOfWeights());
      scale(_h_H_jet1_deta, crossSection()/sumOfWeights());
      scale(_h_H_jet1_dR, crossSection()/sumOfWeights());
      scale(_h_lepton_pT, crossSection()/sumOfWeights());
      scale(_h_lepton_eta, crossSection()/sumOfWeights());

      MC_JetAnalysis::finalize();
    }

    //@}


  private:

    /// @name Histograms
    //@{
    Histo1DPtr _h_H_mass;
    Histo1DPtr _h_H_pT;
    Histo1DPtr _h_H_pT_peak;
    Histo1DPtr _h_H_y;
    Histo1DPtr _h_H_phi;
    Histo1DPtr _h_H_jet1_deta;
    Histo1DPtr _h_H_jet1_dR;
    Histo1DPtr _h_lepton_pT;
    Histo1DPtr _h_lepton_eta;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_HJETS> plugin_MC_HJETS;

}
