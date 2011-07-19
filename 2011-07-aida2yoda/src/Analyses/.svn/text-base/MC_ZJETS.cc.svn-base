// -*- C++ -*-
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/RivetAIDA.hh"

namespace Rivet {


  /// @brief MC validation analysis for Z + jets events
  class MC_ZJETS : public MC_JetAnalysis {
  public:

    /// Default constructor
    MC_ZJETS()
      : MC_JetAnalysis("MC_ZJETS", 4, "Jets")
    {
      setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    /// Book histograms
    void init() {
      ZFinder zfinder(-3.5, 3.5, 25.0*GeV, ELECTRON, 65.0*GeV, 115.0*GeV, 0.2, true, true);
      addProjection(zfinder, "ZFinder");
      FastJets jetpro(zfinder.remainingFinalState(), FastJets::KT, 0.7);
      addProjection(jetpro, "Jets");

      _h_Z_mass = bookHistogram1D("Z_mass", 50, 66.0, 116.0);
      _h_Z_pT = bookHistogram1D("Z_pT", logBinEdges(100, 1.0, 0.5*sqrtS()));
      _h_Z_pT_peak = bookHistogram1D("Z_pT_peak", 25, 0.0, 25.0);
      _h_Z_y = bookHistogram1D("Z_y", 40, -4.0, 4.0);
      _h_Z_phi = bookHistogram1D("Z_phi", 25, 0.0, TWOPI);
      _h_Z_jet1_deta = bookHistogram1D("Z_jet1_deta", 50, -5.0, 5.0);
      _h_Z_jet1_dR = bookHistogram1D("Z_jet1_dR", 25, 0.5, 7.0);
      _h_lepton_pT = bookHistogram1D("lepton_pT", logBinEdges(100, 10.0, 0.25*sqrtS()));
      _h_lepton_eta = bookHistogram1D("lepton_eta", 40, -4.0, 4.0);

      MC_JetAnalysis::init();
    }



    /// Do the analysis
    void analyze(const Event & e) {
      const ZFinder& zfinder = applyProjection<ZFinder>(e, "ZFinder");
      if (zfinder.particles().size()!=1) {
        vetoEvent;
      }
      const double weight = e.weight();

      FourMomentum zmom(zfinder.particles()[0].momentum());
      _h_Z_mass->fill(zmom.mass(),weight);
      _h_Z_pT->fill(zmom.pT(),weight);
      _h_Z_pT_peak->fill(zmom.pT(),weight);
      _h_Z_y->fill(zmom.rapidity(),weight);
      _h_Z_phi->fill(zmom.azimuthalAngle(),weight);
      foreach (const Particle& l, zfinder.constituentsFinalState().particles()) {
        _h_lepton_pT->fill(l.momentum().pT(), weight);
        _h_lepton_eta->fill(l.momentum().eta(), weight);
      }

      const FastJets& jetpro = applyProjection<FastJets>(e, "Jets");
      const Jets& jets = jetpro.jetsByPt(20.0*GeV);
      if (jets.size() > 0) {
        _h_Z_jet1_deta->fill(zmom.eta()-jets[0].momentum().eta(), weight);
        _h_Z_jet1_dR->fill(deltaR(zmom, jets[0].momentum()), weight);
      }

      MC_JetAnalysis::analyze(e);
    }


    /// Finalize
    void finalize() {
      scale(_h_Z_mass, crossSection()/sumOfWeights());
      scale(_h_Z_pT, crossSection()/sumOfWeights());
      scale(_h_Z_pT_peak, crossSection()/sumOfWeights());
      scale(_h_Z_y, crossSection()/sumOfWeights());
      scale(_h_Z_phi, crossSection()/sumOfWeights());
      scale(_h_Z_jet1_deta, crossSection()/sumOfWeights());
      scale(_h_Z_jet1_dR, crossSection()/sumOfWeights());
      scale(_h_lepton_pT, crossSection()/sumOfWeights());
      scale(_h_lepton_eta, crossSection()/sumOfWeights());

      MC_JetAnalysis::finalize();
    }

    //@}


  private:

    /// @name Histograms
    //@{
    AIDA::IHistogram1D * _h_Z_mass;
    AIDA::IHistogram1D * _h_Z_pT;
    AIDA::IHistogram1D * _h_Z_pT_peak;
    AIDA::IHistogram1D * _h_Z_y;
    AIDA::IHistogram1D * _h_Z_phi;
    AIDA::IHistogram1D * _h_Z_jet1_deta;
    AIDA::IHistogram1D * _h_Z_jet1_dR;
    AIDA::IHistogram1D * _h_lepton_pT;
    AIDA::IHistogram1D * _h_lepton_eta;
    //@}

  };



  // This global object acts as a hook for the plugin system
  AnalysisBuilder<MC_ZJETS> plugin_MC_ZJETS;

}
